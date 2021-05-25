"""
Financial Data module
"""

import hashlib
import os

import pandas as pd
import pandas_datareader as pdr

from . import mp
from .util import SYMBOLS


class OHLCVSingle(object):

    def __init__(self, symbol, start, end, cache='ohlcv'):
        """
        Single symbol Tiingo OHLCV data download class.  Must have
        environment variable TIINGO_API_KEY set or authentication.

        Parameters
        ----------
        symbol : string
            company ticker
        start : str or datetime.date compatible object
            download data starting on this date
        end : str or datetime.date compatible object
            download data ending on this date
        cache : str, default 'ohlcv'
            defines the prefix of the cache directory
                <cache>_<start>_<end>

        """
        self.symbol = symbol
        self.start = pd.Timestamp(start)
        self.end = pd.Timestamp(end)
        self.cache = cache

    @property
    def cache(self):
        return self._cache

    @cache.setter
    def cache(self, c):
        start = self.start.strftime('%Y%m%d')
        end = self.end.strftime('%Y%m%d')
        cache = f'{c}_{start}_{end}'
        os.makedirs(cache, exist_ok=True)
        self._cache = cache

    @property
    def store(self):
        return os.path.join(self.cache, f'{self.symbol}_ohlcv.feather')

    def read(self):
        """
        Downloads price and volume data for a single symbol over a
        specified date range.  The resulting internal pandas.DataFrame
        has the following index and column names:
            - index : 'date'
            - columns:  ('close', 'high', 'low', 'open', 'volume',
                         'adjClose', 'adjHigh','adjLow', 'adjOpen', 'adjVolume',
                         'divCash', 'splitFactor')

        Cache the data in a feather store for subsequent calls.
        """
        if os.path.isfile(self.store):
            return pd.read_feather(self.store).set_index('date')

        args = SYMBOLS.validate(
            symbol=self.symbol,
            start=self.start,
            end=self.end,
        )

        dr = pdr.tiingo.TiingoDailyReader(**args)

        try:
            df = dr.read()
        except Exception as e:
            raise ValueError(e)

        df = df.reset_index(level='symbol', drop=True)
        is_weekday = ~df.index.day_name().str.startswith('S')
        df = df[is_weekday]
        df.reset_index().to_feather(self.store)
        dr.close()

        return df


def _ohlcv_single(symbol, start, end):
    try:
        return OHLCVSingle(symbol, start, end).read()
    except ValueError:
        pass


class OHLCVBatch(object):

    def __init__(self, symbols, start, end, cache='ohlcv'):
        """
        Multiple symbol Tiingo OHLCV data download class.  Must have
        environment variable TIINGO_API_KEY set or authentication.

        Parameters
        ----------
        symbols : seq
            sequence of strings representing company tickers
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
        Downloads price and volume data for a sequence of symbols
        over a specified date range.  The resulting internal
        pandas.DataFrame has the following index.level and column
        names:

            - index.level : ('symbol', 'date')  # multi-index
            - columns:  ('close', 'high', 'low', 'open', 'volume',
                         'adjClose', 'adjHigh','adjLow', 'adjOpen', 'adjVolume',
                         'divCash', 'splitFactor')

        Cache the data in a feather store for subsequent calls.
        """
        if os.path.isfile(self.store):
            return pd.read_feather(self.store).set_index(self.index_names)

        results = mp.amap(_ohlcv_single, self.symbols, start=self.start, end=self.end)
        df = pd.concat(results, names=self.index_names)
        df.reset_index().to_feather(self.store)

        return df
