import json
from django.http import JsonResponse
from django.conf import settings
from pathlib import Path
import yfinance as yf
import pytz
from datetime import datetime, timedelta

# Your timezone, for example, 'UTC'
timezone = pytz.timezone('EST')

def get_current_shares_held(ticker):
    if not ticker:
        return JsonResponse({"error": "Ticker symbol is required."}, status=400)

    # Define the path to the JSON file
    json_file_path = Path(settings.BASE_DIR) / 'data' / 'investments_data.json'

    # Open the JSON file and load its content
    with open(json_file_path, 'r') as file:
        transactions_data = json.load(file)

    transactions = [t for t in transactions_data if t['Ticker Symbol'] == ticker]

    if not transactions:
        return JsonResponse({"error": "No transactions found for given ticker."}, status=404)

    current_shares = 0.0

    # Calculate the current number of shares held
    for transaction in transactions:
        shares = float(transaction["No. of Shares"])
        if transaction["Transaction Type"] == "BUY":
            current_shares += shares
        elif transaction["Transaction Type"] == "SELL":
            current_shares -= shares

    return current_shares

def get_stock_history_day(request, ticker):
    if not ticker:
        return JsonResponse({"error": "Ticker symbol is required."}, status=400)

    stock = yf.Ticker(ticker)
    today = datetime.now(tz=timezone).date()

    # Initialize variable to hold historical prices
    historical_prices = None

    # Loop to find the most recent market day with data
    for i in range(7):  # Check up to a week back
        check_day = today - timedelta(days=i)
        day_data = stock.history(period='1d', interval='1m', start=check_day, end=check_day + timedelta(days=1))
        
        if not day_data.empty:
            historical_prices = day_data
            break

    if historical_prices is None:
        return JsonResponse({"error": "No recent market data available."}, status=404)

    shares_held = get_current_shares_held(ticker)
    current_open_time = historical_prices.index[0]

    # Fetch the previous day's closing price
    previous_day_data = stock.history(period="2d", interval="1d")
    if len(previous_day_data) < 2:
        return JsonResponse({"error": "Previous day's data not available"}, status=404)
    previous_close = previous_day_data['Close'].iloc[-2]
    previous_close_paid = shares_held * previous_close

    # Add previous day's close as the first data point
    adjusted_close_time = current_open_time - timedelta(minutes=1)
    adjusted_close_time_str = adjusted_close_time.tz_convert(timezone).strftime('%Y-%m-%d %H:%M:%S')

    historical_values = [{
        "date": adjusted_close_time_str,
        "value": previous_close * shares_held,
        "value_paid": previous_close_paid
    }]

    # Add rest of the historical values
    historical_values.extend([{
        "date": date.tz_convert(timezone).strftime('%Y-%m-%d %H:%M:%S'),
        "value": row['Close'] * shares_held,
        "value_paid": previous_close_paid
    } for date, row in historical_prices.iterrows()])

    return JsonResponse(historical_values, safe=False)