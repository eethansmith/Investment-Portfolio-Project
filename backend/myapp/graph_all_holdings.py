import json
import holidays
from pathlib import Path
from datetime import datetime, timedelta
from django.conf import settings
import pytz
import yfinance as yf
from django.core.cache import cache
from django.http import JsonResponse
from django.utils.timezone import make_aware

# Set your timezone, e.g., 'EST'
timezone = pytz.timezone('EST')

def load_transactions():
    json_file_path = Path(settings.BASE_DIR) / 'data' / 'investments_data.json'
    try:
        with open(json_file_path, 'r') as file:
            return json.load(file)
    except Exception as e:
        print(f"Error loading transactions: {e}")
        return []

def calculate_holdings_over_period(days):
    transactions_data = load_transactions()
    end_date = make_aware(datetime.now(), timezone)
    start_date = end_date - timedelta(days=days)
    current_holdings = {}
    daily_holdings = {end_date: {}}

    # Calculate current holdings
    for transaction in transactions_data:
        ticker = transaction["Ticker Symbol"]
        shares = float(transaction["No. of Shares"])
        transaction_type = transaction["Transaction Type"]
        transaction_date = make_aware(datetime.strptime(transaction["Date"], '%d-%m-%Y'), timezone)
        if transaction_date <= end_date:
            current_holdings.setdefault(ticker, 0)
            current_holdings[ticker] += shares if transaction_type == "BUY" else -shares

    # Calculate daily holdings
    for single_date in reversed([start_date + timedelta(n) for n in range(days)]):
        daily_holdings[single_date] = current_holdings.copy()
        for transaction in transactions_data:
            transaction_date = make_aware(datetime.strptime(transaction["Date"], '%d-%m-%Y'), timezone)
            if start_date < transaction_date <= single_date:
                ticker = transaction["Ticker Symbol"]
                shares = float(transaction["No. of Shares"])
                transaction_type = transaction["Transaction Type"]
                if transaction_type == "BUY":
                    daily_holdings[single_date][ticker] -= shares
                elif transaction_type == "SELL":
                    daily_holdings[single_date][ticker] += shares

    return daily_holdings

def fetch_historical_prices_with_cache(ticker, start_date, end_date):
    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')
    cache_key = f"{ticker}_{start_date_str}_{end_date_str}".replace(' ', '_').replace(':', '')

    cached_data = cache.get(cache_key)
    if cached_data is not None:
        return cached_data

    try:
        stock = yf.Ticker(ticker)
        historical_data = stock.history(start=start_date_str, end=end_date_str)
        price_data = historical_data['Close']
        if price_data.empty:
            raise ValueError(f"No data for {ticker} from {start_date_str} to {end_date_str}")
        cache.set(cache_key, price_data, timeout=86400)  # Cache for 1 day
        return price_data
    except Exception as e:
        print(f"Error fetching historical data for {ticker}: {e}")
        return None

def is_market_open(date):
    # Check if the date is a weekend
    if date.weekday() >= 5:
        return False

    # Check for market holidays
    us_holidays = holidays.US(years=date.year)
    if date in us_holidays:
        return False

    return True

def calculate_portfolio_value_over_period(days):
    daily_holdings = calculate_holdings_over_period(days)
    portfolio_value = {}
    interval = '1d'

    if days <= 7:
        interval = '1h'  # hourly data for up to 7 days
    elif days == 1:
        interval = '1m'  # minute data for a single day

    for single_date in daily_holdings:
        if not is_market_open(single_date):
            continue

        daily_value = 0
        for ticker, shares in daily_holdings[single_date].items():
            if shares > 0:
                price_data = fetch_historical_prices_with_cache(ticker, single_date, single_date + timedelta(days=1))
                if price_data is not None:
                    # Find the price for the specific part of the day
                    price = price_data.get(single_date.strftime('%Y-%m-%d'))
                    if price is not None:
                        daily_value += price * shares

        if daily_value > 0:
            portfolio_value[single_date] = daily_value

    return dict(sorted(portfolio_value.items()))

def get_portfolio_value(request, days):
    try:
        days = int(days)
    except ValueError:
        return JsonResponse({"error": "Invalid number of days provided."}, status=400)

    portfolio_values = calculate_portfolio_value_over_period(days)
    formatted_data = [{"date": date.strftime('%Y-%m-%d'), "value": value} for date, value in portfolio_values.items()]
    return JsonResponse(formatted_data, safe=False)
