import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

def print_stock_performance():
    data = pd.read_csv('/Users/ethansmith/Documents/GitHub/investments/investment_data.csv')

   # Convert Date and Time into a single datetime column and sort
    data['DateTime'] = pd.to_datetime(data['Date'] + ' ' + data['Time'], dayfirst=True)
    data.sort_values(by='DateTime', inplace=True)

    # Remove '$' sign and convert to float
    data['Price per Share USD'] = data['Price per Share USD'].replace('[\$,]', '', regex=True).astype(float)

    # Dictionary to track each stock's performance
    stock_performance = {}
    SHARE_THRESHOLD = 1e-8  # Threshold for considering shares count as negligible


    for index, row in data.iterrows():
        ticker = row['Ticker Symbol']
        shares = float(row['No. of Shares'])
        transaction_type = row['Transaction Type']
        transaction_value = shares * row['Price per Share USD']

        if ticker not in stock_performance:
            stock_performance[ticker] = {'shares': 0, 'invested': 0}

        if transaction_type == 'BUY':
            stock_performance[ticker]['shares'] += shares
            stock_performance[ticker]['invested'] += transaction_value
        elif transaction_type == 'SELL':
            stock_performance[ticker]['shares'] -= shares
            stock_performance[ticker]['invested'] -= transaction_value

    # Display gains/losses and current holdings
    for ticker, info in stock_performance.items():
        # Adjust for small or negative share counts
        if abs(info['shares']) < SHARE_THRESHOLD:
            info['shares'] = 0

        if info['shares'] == 0:
            result = "Loss" if info['invested'] > 0 else "Gain"
            print(f"{ticker} - {result}: ${abs(info['invested']):.2f}")
        else:
            print(f"{ticker} - Current Holdings: {info['shares']} shares, Invested: ${info['invested']:.2f}")

    return stock_performance

# Example usage
##print_current_holdings()
#valuation_changes = print_stock_performance()
#for change in valuation_changes:
#    print(change)





import pandas as pd

def analyze_stock_performance(csv_path):
    data = pd.read_csv(csv_path)

    # Convert Date and Time into a single datetime column and sort
    data['DateTime'] = pd.to_datetime(data['Date'] + ' ' + data['Time'], dayfirst=True)
    data.sort_values(by='DateTime', inplace=True)
    data['Price per Share USD'] = data['Price per Share USD'].replace('[\$,]', '', regex=True).astype(float)

    stock_performance = {}
    portfolio_value_over_time = []

    for index, row in data.iterrows():
        ticker = row['Ticker Symbol']
        shares = float(row['No. of Shares'])
        transaction_type = row['Transaction Type']
        transaction_value = shares * row['Price per Share USD']

        if ticker not in stock_performance:
            stock_performance[ticker] = {'shares': 0, 'invested': 0}

        if transaction_type == 'BUY':
            stock_performance[ticker]['shares'] += shares
            stock_performance[ticker]['invested'] += transaction_value
        elif transaction_type == 'SELL':
            stock_performance[ticker]['shares'] -= shares
            stock_performance[ticker]['invested'] -= transaction_value

        # Calculate the total portfolio value at this point in time
        total_value = sum(stock['invested'] for stock in stock_performance.values())
        portfolio_value_over_time.append({'DateTime': row['DateTime'], 'TotalValue': total_value})

    # Create a DataFrame for the portfolio value over time
    portfolio_value_df = pd.DataFrame(portfolio_value_over_time)
    return portfolio_value_df

def plot_portfolio_value_over_time(performance_data):
    plt.figure(figsize=(10, 6))
    # Convert 'DateTime' and 'TotalValue' to lists or numpy arrays for proper handling
    plt.plot(performance_data['DateTime'].tolist(), performance_data['TotalValue'].tolist())
    plt.title('Portfolio Value Over Time')
    plt.xlabel('Date')
    plt.ylabel('Total Portfolio Value')
    plt.grid(True)
    plt.show()

# Example usage
csv_path = '/Users/ethansmith/Documents/GitHub/investments/investment_data.csv'
##performance_data = analyze_stock_performance(csv_path)

# Example usage
##plot_portfolio_value_over_time(performance_data)


def plot_stock_performance(stock_symbol, csv_path):
    # Load your transaction data
    data = pd.read_csv(csv_path)
    data['DateTime'] = pd.to_datetime(data['Date'] + ' ' + data['Time'], dayfirst=True)
    data.sort_values(by='DateTime', inplace=True)

    # Filter data for the specific stock and calculate cumulative shares
    stock_data = data[data['Ticker Symbol'] == stock_symbol].copy()
    stock_data['Cumulative Shares'] = stock_data.apply(lambda x: x['No. of Shares'] if x['Transaction Type'] == 'BUY' else -x['No. of Shares'], axis=1).cumsum()

    # Fetch historical market data for the stock
    start_date = stock_data['DateTime'].min()
    end_date = pd.to_datetime('today')
    market_data = yf.download(stock_symbol, start=start_date, end=end_date)

    # Merge market data with your transaction data
    merged_data = pd.merge_asof(market_data, stock_data, left_index=True, right_on='DateTime')
    merged_data['Holding Value'] = merged_data['Cumulative Shares'] * merged_data['Close']

    # Plot the holding value over time
    plt.figure(figsize=(12, 6))
    plt.plot(merged_data['DateTime'].values, merged_data['Holding Value'].values)
    plt.title(f'Holding Value Over Time: {stock_symbol}')
    plt.xlabel('Date')
    plt.ylabel('Holding Value')
    plt.grid(True)
    plt.show()

##plot_stock_performance('VUAG.L', '/Users/ethansmith/Documents/GitHub/investments/investment_data.csv')


def plot_total_portfolio_value(csv_path):
    data = pd.read_csv(csv_path)
    data['DateTime'] = pd.to_datetime(data['Date'] + ' ' + data['Time'], dayfirst=True)
    data.sort_values(by='DateTime', inplace=True)
    data['Price per Share USD'] = data['Price per Share USD'].replace('[\$,]', '', regex=True).astype(float)

    unique_stocks = data['Ticker Symbol'].unique()
    portfolio_values = []

    for stock in unique_stocks:
        stock_data = data[data['Ticker Symbol'] == stock].copy()
        stock_data['Cumulative Shares'] = stock_data.apply(
            lambda x: x['No. of Shares'] if x['Transaction Type'] == 'BUY' else -x['No. of Shares'], 
            axis=1
        ).cumsum()

        try:
            historical_data = yf.download(stock, start=stock_data['DateTime'].min(), end=pd.to_datetime('today'))
            merged_data = pd.merge_asof(historical_data, stock_data, left_index=True, right_on='DateTime')
            merged_data['Holding Value'] = merged_data['Cumulative Shares'] * merged_data['Close']
            portfolio_values.append(merged_data[['DateTime', 'Holding Value']])
        except Exception as e:
            print(f"Failed to download data for {stock}: {e}")
            continue  # Skip this stock

    total_portfolio = pd.concat(portfolio_values).groupby('DateTime').sum().reset_index()

    total_portfolio_cleaned = remove_outliers(total_portfolio, 'Holding Value', num_std=3)

    # Plotting the total portfolio value over time
    plt.figure(figsize=(12, 6))
    plt.plot(total_portfolio['DateTime'].values, total_portfolio['Holding Value'].values)  # Use .values for proper indexing
    plt.title('Total Portfolio Value Over Time')
    plt.xlabel('Date')
    plt.ylabel('Total Portfolio Value')
    plt.grid(True)
    plt.show()

def remove_outliers(df, column_name, num_std=3):
    """ Remove outliers from a dataframe by column, using n standard deviations """
    mean_val = df[column_name].mean()
    std_val = df[column_name].std()

    # Define the upper and lower limit for detecting outliers
    upper_limit = mean_val + (num_std * std_val)
    lower_limit = mean_val - (num_std * std_val)

    # Filter out outliers
    filtered_df = df[(df[column_name] <= upper_limit) & (df[column_name] >= lower_limit)]
    return filtered_df


plot_total_portfolio_value(csv_path)




# create stock dictionary for each stock in csv
def create_stock_dictionaries(csv_path):
    data = pd.read_csv(csv_path)
    data['DateTime'] = pd.to_datetime(data['Date'] + ' ' + data['Time'], dayfirst=True)
    data.sort_values(by='DateTime', inplace=True)

    stocks_dict = {}
    for index, row in data.iterrows():
        ticker = row['Ticker Symbol']
        shares = float(row['No. of Shares'])  # Ensuring shares are treated as float
        price_per_share = float(row['Price per Share USD'].replace('$', ''))  # Handling potential $ sign

        if ticker not in stocks_dict:
            stocks_dict[ticker] = {'cumulative_shares': 0, 'total_cost': 0, 'transactions': []}

        transaction = {'type': row['Transaction Type'], 'shares': shares, 'price_per_share': price_per_share}
        stocks_dict[ticker]['transactions'].append(transaction)

        if transaction['type'] == 'BUY':
            stocks_dict[ticker]['cumulative_shares'] += shares
            stocks_dict[ticker]['total_cost'] += shares * price_per_share
        elif transaction['type'] == 'SELL':
            # Assuming you sell shares at the same average price, if available
            avg_price = stocks_dict[ticker]['total_cost'] / stocks_dict[ticker]['cumulative_shares'] if stocks_dict[ticker]['cumulative_shares'] > 0 else 0
            stocks_dict[ticker]['cumulative_shares'] -= shares
            stocks_dict[ticker]['total_cost'] -= shares * avg_price

        if stocks_dict[ticker]['cumulative_shares'] > 0:
            stocks_dict[ticker]['average_price_per_share'] = stocks_dict[ticker]['total_cost'] / stocks_dict[ticker]['cumulative_shares']
        else:
            stocks_dict[ticker]['average_price_per_share'] = 0

    return stocks_dict

# calculating the gain/loss for each stock
def calculate_gain_loss(stocks_dict):
    for ticker, stock_info in stocks_dict.items():
        # Fetch current price for the stock
        current_price = yf.Ticker(ticker).history(period="1d")['Close'].iloc[-1]

        # Calculate current value of held shares
        current_value = stock_info['cumulative_shares'] * current_price

        # Calculate total invested amount
        # Assuming 'total_cost' is already updated in stock_info during transaction processing
        total_invested = stock_info['total_cost']

        # Calculate gain/loss
        gain_loss = current_value - total_invested

        # Update the stocks_dict with current value and gain/loss
        stock_info['current_value'] = current_value
        stock_info['gain_loss'] = gain_loss

    return stocks_dict