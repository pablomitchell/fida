import hashlib
import os

import pandas as pd
from pandas_datareader import tiingo


class OHLCV(object):

    def __init__(self, symbols, start, end, cache='ohlcv'):
        """
        Lightweight Tiingo OHLCV data download class

        Parameters
        ----------
        symbols : seq
            sequence of strings corresponding to company symbols
        start : str or datetime.date compatible object
            download data starting on this date
        end : str or datetime.date compatible object
            download data ending on this date
        cache : str, default 'ohlcv'
            defines the path to the cache directory

        """
        self.symbols = symbols
        self.start = pd.Timestamp(start)
        self.end = pd.Timestamp(end)
        self.cache = cache

    @property
    def cache(self):
        return self._cache

    @cache.setter
    def cache(self, c):
        os.makedirs(c, exist_ok=True)
        self._cache = c

    @property
    def index_names(self):
        return ['symbol', 'date']

    @property
    def store(self):
        symbols = '-'.join(sorted(set(self.symbols)))

        start = self.start.strftime('%Y%m%d')
        end = self.end.strftime('%Y%m%d')

        input = f'{symbols}-{start}-{end}'
        output = hashlib.md5(input.encode('utf-8')).hexdigest()

        return os.path.join(self.cache, f'tiingo-ohlcv-{output}.feather')

    def read(self):
        """
        Downloads then caches price and volume data for a sequence of
        symbols over a specified date range.

        The resulting internal pandas.DataFrame has the following
        index.level and column names:

            - index.level : ('symbol', 'date')  # multi-index
            - columns:  ('close', 'high', 'low', 'open', 'volume',
                         'adjClose', 'adjHigh','adjLow', 'adjOpen', 'adjVolume',
                         'divCash', 'splitFactor')
        """
        if os.path.isfile(self.store):
            return pd.read_feather(self.store).set_index(self.index_names)

        dr = tiingo.TiingoDailyReader(
            symbols=self.symbols,
            start=self.start,
            end=self.end,
        )
        df = dr.read()
        df.reset_index().to_feather(self.store)
        dr.close()

        return df


if __name__ == '__main__':

    symbols = [
        'AAPL',
        'MSFT',
        'GOOG',
    ]
    start = '2020-01-01'
    end = '2020-12-31'

    ohlcv = OHLCV(symbols, start, end)
    df = ohlcv.read()

    close = df.adjClose.unstack().T
    print(close.head())