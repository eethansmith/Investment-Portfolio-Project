import yfinance as yf

# giving the start and end dates
startDate = '2023-03-01'
endDate = '2023-11-01'

# setting the ticker value
ticker = 'VUAG.L'

# downloading the data of the ticker value between
# the start and end dates
resultData = yf.download(ticker, startDate, endDate)

# Setting date as index
resultData["Date"] = resultData.index

# Giving column names
resultData = resultData[["Date", "Open", "High","Low", "Close", "Adj Close", "Volume"]]

# Resetting the index values
resultData.reset_index(drop=True, inplace=True)

# getting the first 5 rows of the data
print(resultData.head())