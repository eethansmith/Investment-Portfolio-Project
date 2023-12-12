import json
from django.http import JsonResponse
from django.conf import settings
from pathlib import Path
import yfinance as yf
import pytz
from datetime import datetime, timedelta

# Your timezone, for example, 'UTC'
timezone = pytz.timezone('EST')

def get_stock_history(request, ticker):
    if not ticker:
        return JsonResponse({"error": "Ticker symbol is required."}, status=400)

    stock = yf.Ticker(ticker)
    # Fetch data for the last 24 hours with granular intervals (e.g., 5 minutes)
    end_date = datetime.now(tz=timezone)
    start_date = end_date - timedelta(days=1)
    historical_prices = stock.history(start=start_date.strftime('%Y-%m-%d'), end=end_date.strftime('%Y-%m-%d'), interval="5m")

    # Fetch the previous day's closing price
    previous_day_data = stock.history(period="2d", interval="1d")
    if len(previous_day_data) < 2:
        return JsonResponse({"error": "Previous day's data not available"}, status=404)
    previous_close = previous_day_data['Close'].iloc[-2]

    # Convert data to the desired timezone and format for response
    historical_values = [{
        "datetime": date.tz_convert(timezone).strftime('%Y-%m-%d %H:%M:%S'),
        "value": row['Close'],
        "value_paid": previous_close
    } for date, row in historical_prices.iterrows()]

    return JsonResponse(historical_values, safe=False)
