import warnings

from fida import constituents, ohlcv

warnings.simplefilter(action="ignore", category=FutureWarning)

params = {
    "symbols": constituents.get_sp500().sample(10).ticker,
    "start": "1990-01-01",
    "end": "2020-12-31",
    "interpolate": True,
}
prices = ohlcv.get_price_tiingo(**params)
returns = ohlcv.get_return_tiingo(log=True, **params)

print("PRICES")
print(prices.head().to_string())
print(prices.tail().to_string())
print("-" * 80)
print("RETURNS")
print(returns.head().to_string())
print(returns.tail().to_string())
