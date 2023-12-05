import json
from django.http import JsonResponse
from django.conf import settings
from pathlib import Path
import yfinance as yf
import pytz
from datetime import datetime

# Your timezone, for example, 'UTC'
timezone = pytz.timezone('EST')

def get_stock_history(request, ticker):
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

    # Sort transactions by date
    transactions.sort(key=lambda x: datetime.strptime(x["Date"], '%d-%m-%Y'))

    # Get the first purchase date and last sale/current date
    start_date = datetime.strptime(transactions[0]["Date"], '%d-%m-%Y')
    end_date = datetime.now()

    stock = yf.Ticker(ticker)
    historical_prices = stock.history(start=start_date.strftime('%Y-%m-%d'), end=end_date.strftime('%Y-%m-%d'))

    historical_values = []
    current_shares = 0
    current_average_cost_per_share = 0

    for date, row in historical_prices.iterrows():
        date = date.to_pydatetime().replace(tzinfo=None)
        # Accumulate shares up to the current date
        for transaction in transactions:
            transaction_date = datetime.strptime(transaction["Date"], '%d-%m-%Y')
            if transaction_date <= date:
                shares = float(transaction["No. of Shares"])
                if transaction["Transaction Type"] == "BUY":
                    current_shares += shares
                    current_average_cost_per_share = float(transaction["Average Cost per Share USD"])
                elif transaction["Transaction Type"] == "SELL":
                    current_shares -= shares
                    
        # Calculate value for the current date
        stock_worth = current_shares * row['Close']
        stock_paid = current_average_cost_per_share * current_shares
        historical_values.append({
            "date": date.strftime('%Y-%m-%d'), 
            "stock_worth": stock_worth,
            "stock_paid": stock_paid})

    return JsonResponse(historical_values, safe=False)
