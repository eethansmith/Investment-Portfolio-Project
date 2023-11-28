import csv
import json

def calculate_transaction_valuation(rows):
    for row in rows:
        shares = float(row['No. of Shares'])
        price_per_share = float(row['Price per Share USD'].replace('$', ''))
        transaction_valuation = shares * price_per_share
        row['Transaction Valuation USD'] = transaction_valuation

    return rows


def calculate_overall_holdings(rows):
    holdings = {}  # Dictionary to keep track of holdings for each stock
    for row in rows:
        ticker = row['Ticker Symbol']
        shares = float(row['No. of Shares'])
        transaction_type = row['Transaction Type']

        if ticker not in holdings:
            holdings[ticker] = 0  # Initialize if ticker not in holdings

        if transaction_type == 'BUY':
            holdings[ticker] += shares  # Add shares if bought
        elif transaction_type == 'SELL':
            holdings[ticker] -= shares  # Subtract shares if sold

        row['Overall Holdings'] = holdings[ticker]  # Update current row with overall holdings

    return rows



def calculate_average_cost_per_share(rows):
    stock_info = {}  # Dictionary to keep track of stock information

    for row in rows:
        ticker = row['Ticker Symbol']
        shares = float(row['No. of Shares'])
        transaction_price = float(row['Price per Share USD'].replace('$', ''))
        transaction_type = row['Transaction Type']

        if ticker not in stock_info:
            stock_info[ticker] = {'total_shares': 0, 'total_cost': 0, 'average_cost_per_share': 0}

        if transaction_type == 'BUY':
            new_total_shares = stock_info[ticker]['total_shares'] + shares
            new_total_cost = stock_info[ticker]['total_cost'] + (shares * transaction_price)

            stock_info[ticker]['total_shares'] = new_total_shares
            stock_info[ticker]['total_cost'] = new_total_cost

            if new_total_shares > 0:
                stock_info[ticker]['average_cost_per_share'] = new_total_cost / new_total_shares
        elif transaction_type == 'SELL':
            new_total_shares = stock_info[ticker]['total_shares'] - shares

            # Adjust the total cost based on the average cost at the time of the sell
            if new_total_shares > 0:
                new_total_cost = stock_info[ticker]['average_cost_per_share'] * new_total_shares
            else:
                new_total_cost = 0

            stock_info[ticker]['total_shares'] = new_total_shares
            stock_info[ticker]['total_cost'] = new_total_cost

        row['Average Cost per Share USD'] = stock_info[ticker]['average_cost_per_share']

    return rows



def calculate_realized_gains_losses(rows):
    for row in rows:
        transaction_type = row['Transaction Type']
        if transaction_type == 'SELL':
            shares_sold = float(row['No. of Shares'])
            sell_price_per_share = float(row['Price per Share USD'].replace('$', ''))
            average_cost_per_share = float(row['Average Cost per Share USD'])

            realized_gain_loss = (sell_price_per_share - average_cost_per_share) * shares_sold
            row['Realized Gain/Loss USD'] = realized_gain_loss
        else:
            row['Realized Gain/Loss USD'] = 0  # Or you can omit this line if you prefer not to show this field for non-SELL transactions

    return rows


def calculate_portfolio_valuation(rows):
    portfolio_valuation = 0  # Initialize the portfolio valuation

    for row in rows:
        transaction_type = row['Transaction Type']
        transaction_valuation = float(row['Transaction Valuation USD'])

        if transaction_type == 'BUY':
            portfolio_valuation += transaction_valuation
        elif transaction_type == 'SELL':
            portfolio_valuation -= transaction_valuation

        row['Portfolio Valuation USD'] = portfolio_valuation

    return rows





# CSV file path
csv_file_path = '/Users/ethansmith/Documents/GitHub/investments/investment_data.csv'

# JSON file path
json_file_path = '/Users/ethansmith/Documents/GitHub/investments/investment_data.json'

# Read the CSV and add the data to a dictionary
data = []
try:
    with open(csv_file_path, mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        rows = list(csv_reader)  # Convert the CSV reader to a list
        rows.reverse()  # Reverse the order to make it chronological

        # Calculate transaction valuation
        updated_rows = calculate_transaction_valuation(rows)
        
        # Calculate overall holdings and update the rows
        updated_rows = calculate_overall_holdings(updated_rows)

        # Calculate average cost per share using the updated rows
        updated_rows = calculate_average_cost_per_share(updated_rows)

        # Calculate realized gains/losses
        updated_rows = calculate_realized_gains_losses(updated_rows)

        # Calculate portfolio valuation
        updated_rows = calculate_portfolio_valuation(updated_rows)

        # Write data to a JSON file
        with open(json_file_path, mode='w', encoding='utf-8') as json_file:
            json.dump(updated_rows, json_file, indent=4)
        result = f"Data successfully written to {json_file_path}"
except Exception as e:
    result = f"An error occurred: {e}"

print(result)
