import warnings

from fida import constituents, ohlcv

warnings.simplefilter(action="ignore", category=FutureWarning)


start = "1990-01-01"
end = "2020-12-31"


sp500 = constituents.get_sp500()
print(sp500.sample(10))

# sp600 = constituents.get_sp500()
# print(sp600.sample(10))

sp500 = ohlcv.get_price_yahoo(symbols=sp500.ticker[:10], start=start, end=end)
sp500 = sp500.dropna(axis="index", how="all").dropna(axis="columns", how="all")
sp500.info()


# import yfinance as yf

# df = yf.download("AAPL", start=start, end=end)
# print(df.tail().to_string())
