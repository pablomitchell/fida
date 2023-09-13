import warnings

from fida import constituents, ohlcv

warnings.simplefilter(action="ignore", category=FutureWarning)


start = "1990-01-01"
end = "2020-12-31"


sp500 = constituents.get_sp500()
print(sp500.sample(10))

sp500_prices = ohlcv.get_price_tiingo(symbols=sp500.ticker[:10], start=start, end=end)
sp500_prices = sp500_prices.dropna(axis="index", how="all").dropna(axis="columns", how="all")
sp500.info()
