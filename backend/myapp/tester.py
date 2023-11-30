import yfinance as yf

ticker = yf.Ticker("VUAG.L")
print(ticker.info)