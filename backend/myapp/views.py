import json
from django.http import JsonResponse
from django.conf import settings
from pathlib import Path
from rest_framework import viewsets
import yfinance as yf


def load_transactions(request):
    json_file_path = Path(settings.BASE_DIR) / 'data' / 'investments_data.json'
    with open(json_file_path, 'r') as file:
        data = json.load(file)
    return JsonResponse(data, safe=False)

def get_stock_holdings(request):
    # Define the path to the JSON file
    json_file_path = Path(settings.BASE_DIR) / 'data' / 'investments_data.json'


    # Open the JSON file and load its content
    with open(json_file_path, 'r') as file:
        transactions_data = json.load(file)

    # Process transactions to determine current holdings
    holdings = {}
    for transaction in transactions_data:
        ticker = transaction["Ticker Symbol"]
        shares = float(transaction["No. of Shares"])
        transaction_type = transaction["Transaction Type"]

        if ticker not in holdings:
            holdings[ticker] = 0.0

        if transaction_type == "BUY":
            holdings[ticker] += shares
        elif transaction_type == "SELL":
            holdings[ticker] -= shares

    # Filter out stocks where holdings are zero or negative
    holdings = {k: v for k, v in holdings.items() if v > 0}

    # Fetch live data for remaining stocks
    live_data = {}
    for ticker, shares in holdings.items():
        try:
            stock = yf.Ticker(ticker)
            stock_info = stock.info
            live_data[ticker] = {
                "ticker": ticker,
                "shares_held": shares,
                "current_price": stock_info.get("regularMarketPrice"),
                # Include other live data as needed
            }
        except Exception as e:
            print(f"Error fetching data for {ticker}: {e}")
            # Optionally, handle the error in the response
            live_data[ticker] = {
                "ticker": ticker,
                "error": str(e)
            }
            
    return JsonResponse(live_data)