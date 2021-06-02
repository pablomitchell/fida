import pandas as pd
import matplotlib.pylab as plt

from fida import constituents
from fida import mp
from fida import meta
from fida import ohlcv
from fida import meta


plt.style.use('seaborn')

start = '1990-01-01'
end = '2020-12-31'

# symbols = constituents.get_psuedo_knuteson_index().ticker
# symbols = constituents.get_tiingo_common_stock_us(start, end)

sp500_frame = constituents.get_sp500()
print(sp500_frame.head().to_string())
print(sp500_frame.tail().to_string())

sp600_frame = constituents.get_sp600()
print(sp600_frame.head().to_string())
print(sp600_frame.tail().to_string())

exit()

# df = ohlcv.OHLCVBatch(symbols, start, end).read()
# close = df.adjClose.unstack().T.SPY
# close.plot(title='SPY')
# plt.show()

# df = ohlcv.OHLCVSingle('AAPL', start=start, end=end).read()
# print(df.head().to_string())
# print()
# print(df.tail().to_string())


# def ohlcv_single(symbol, start, end):
#     try:
#         return ohlcv.OHLCVSingle(symbol, start, end).read()
#     except ohlcv.OHLCVError:
#         pass
#
#
# results = mp.amap(ohlcv_single, symbols, start=start, end=end)
# df = pd.concat(results)
# df.info()


df = meta.MetaBatch(symbols, start, end).read()
df.info()
print(df.drop('description', axis=1).to_string())

# df = ohlcv.OHLCVBatch(symbols[:10], start, end).read()
# df.info()


# df.loc['AAPL'].get('adjClose').plot()
# plt.show()