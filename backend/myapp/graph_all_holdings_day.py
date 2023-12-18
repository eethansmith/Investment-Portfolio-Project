import json
from django.http import JsonResponse
from django.conf import settings
from pathlib import Path
import yfinance as yf
import pytz
from datetime import datetime, timedelta
from collections import defaultdict

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

def get_all_holdings_day(request):
    json_file_path = Path(settings.BASE_DIR) / 'data' / 'investments_data.json'

    with open(json_file_path, 'r') as file:
        transactions_data = json.load(file)

    # Get a list of unique tickers
    tickers = set(t['Ticker Symbol'] for t in transactions_data)

    # Aggregated data for all stocks
    aggregated_data = defaultdict(lambda: {"total_value": 0, "value_paid": 0})

    # Store previous day's closing value
    total_value_paid = 0

    for ticker in tickers:
        shares_held = get_current_shares_held(ticker)

        if shares_held <= 0:
            continue

        stock = yf.Ticker(ticker)
        today = datetime.now(tz=timezone).date()

        # Find most recent market day with data
        for i in range(7):
            check_day = today - timedelta(days=i)
            day_data = stock.history(period='1d', interval='1m', start=check_day, end=check_day + timedelta(days=1))
            prev_day_data = stock.history(period="2d", interval="1d")
            if not day_data.empty and len(prev_day_data) >= 2:
                previous_close = prev_day_data['Close'].iloc[-2]
                total_value_paid += previous_close * shares_held
                break

        if day_data.empty or len(prev_day_data) < 2:
            continue  # Skip if no data available

        for time, row in day_data.iterrows():
            # Add the value of this stock to the aggregated data
            aggregated_data[time]["total_value"] += row['Close'] * shares_held
            aggregated_data[time]["value_paid"] = total_value_paid

    # Convert aggregated data to a list format suitable for JsonResponse
    historical_values = [{"date": time.tz_convert(timezone).strftime('%Y-%m-%d %H:%M:%S'),
                          "total_value": data["total_value"],
                          "value_paid": data["value_paid"]}
                         for time, data in aggregated_data.items()]

    return JsonResponse(historical_values, safe=False)