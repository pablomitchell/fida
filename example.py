import warnings

from fida import constituents, ohlcv

warnings.simplefilter(action="ignore", category=FutureWarning)


params = {
    "symbols": constituents.get_sp500().sample(10).ticker,
    "start": "1990-01-01",
    "end": "2020-12-31",
    "interpolate": True,
}

sp_subset_prices = ohlcv.get_price_tiingo(**params)
sp_subset_returns = ohlcv.get_return_tiingo(**params)

print("PRICES")
print(sp_subset_prices.head().to_string())
print(sp_subset_prices.tail().to_string())
print("-" * 80)
print("RETURNS")
print(sp_subset_returns.head().to_string())
print(sp_subset_returns.tail().to_string())
