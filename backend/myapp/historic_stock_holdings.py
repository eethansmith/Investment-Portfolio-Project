import json
import yfinance as yf
from django.http import JsonResponse
from django.conf import settings
from pathlib import Path

def get_historic_stock_holdings(request):
    json_file_path = Path(settings.BASE_DIR) / 'data' / 'investments_data.json'

    with open(json_file_path, 'r') as file:
        transactions_data = json.load(file)

    historic_holdings = {}
    known_unlisted_stocks = {
        "TWTR": "Twitter",
        "CCIV": "Churchill Capital IV",
        "NK": "NantKwest",
        "FTOC": "FTAC Olympus Acquisition"
    }

    for transaction in transactions_data:
        ticker = transaction["Ticker Symbol"]
        shares = float(transaction["No. of Shares"])
        transaction_type = transaction["Transaction Type"]
        transaction_value = float(transaction["Transaction Valuation USD"])
        
        if ticker not in historic_holdings:
            historic_holdings[ticker] = {"total_bought": 0, "total_sold": 0, "net_shares": 0}

        if transaction_type == "BUY":
            historic_holdings[ticker]["total_bought"] += transaction_value
            historic_holdings[ticker]["net_shares"] += shares
        elif transaction_type == "SELL":
            historic_holdings[ticker]["total_sold"] += transaction_value
            historic_holdings[ticker]["net_shares"] -= shares

    historic_holdings = {ticker: data for ticker, data in historic_holdings.items() if data["net_shares"] < 0.00001}

    response_data = {}
    for ticker, data in historic_holdings.items():
        if ticker in known_unlisted_stocks:
            stock_name = known_unlisted_stocks[ticker]
        else:
            try:
                stock = yf.Ticker(ticker)
                stock_info = stock.info
                stock_name = stock_info.get("longName")
            except Exception as e:
                print(f"Error fetching data for {ticker}: {e}")
                stock_name = None  # Set to NULL if long name can't be fetched


        total_investment = data["total_bought"]
        total_return = data["total_sold"]
        net_gain_loss = total_return - total_investment

        response_data[ticker] = {
            "name": stock_name,
            "ticker": ticker,
            "net_shares": data["net_shares"],
            "total_investment": total_investment,
            "total_return": total_return,
            "net_gain_loss": net_gain_loss
        }

    # Sort response_data based on net_gain_loss
    sorted_data = sorted(response_data.items(), key=lambda x: x[1]['net_gain_loss'], reverse=True)
    sorted_response_data = {k: v for k, v in sorted_data}

    return JsonResponse(sorted_response_data)
