import json
from django.http import JsonResponse
from django.conf import settings
from pathlib import Path
import yfinance as yf

def get_stock_holdings_day(request):
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

        holdings[ticker] += shares if transaction_type == "BUY" else -shares

    # Filter out stocks where holdings are zero or negative
    holdings = {k: v for k, v in holdings.items() if v > 0}

    # Fetch live data for remaining stocks
    live_data = {}
    for ticker, shares in holdings.items():
        try:
            stock = yf.Ticker(ticker)
            stock_info = stock.info

            # Determine the correct fields based on the ticker
            name_field = "longName" if ticker == "VUAG.L" else "shortName"
            price_field = "previousClose" if ticker == "VUAG.L" else "currentPrice"

            # Fetch the relevant data
            name = stock_info.get(name_field)
            current_price = stock_info.get(price_field) or stock_info.get("previousClose")
            average_cost = stock_info.get("previousClose")
            total_investment = average_cost * shares
            current_value = shares * current_price if current_price is not None else None
            value_held = round((shares * current_price if current_price is not None else None),2)

            profit_loss_percentage = round((((current_value - total_investment) / total_investment * 100) if current_value is not None else None),2)


            live_data[ticker] = {
                "ticker": ticker,
                "name": name,
                "shares_held": round(shares,4),
                "current_price": current_price,
                "value_held": value_held,
                "profit_loss_percentage": profit_loss_percentage
            }
        except Exception as e:
            print(f"Error fetching data for {ticker}: {e}")
            live_data[ticker] = {
                "ticker": ticker,
                "error": str(e)
        }
    
    sorting_data = sorted(live_data.items(), key=lambda x: x[1].get('value_held', 0), reverse=True)
    live_data = {k: v for k, v in sorting_data}

    return JsonResponse(live_data)