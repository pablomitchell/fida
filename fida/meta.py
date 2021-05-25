"""
Financial Data module
"""

import hashlib
import os

import pandas as pd
import pandas_datareader as pdr

from . import mp
from .util import SYMBOLS


class MetaSingle(object):

    def __init__(self, symbol, start, end, cache='meta'):
        """
        Single symbol Tiingo meta data download class.  Must have
        environment variable TIINGO_API_KEY set or authentication.

        Parameters
        ----------
        symbol : string
            company ticker
        start : str or datetime.date compatible object
            not used - for compatibility with tiingo
        end : str or datetime.date compatible object
            not used - for compatibility with tiingo
        cache : str, default 'meta'
            defines the prefix of the cache directory

        """
        self.symbol = symbol
        self.start = pd.Timestamp(start)
        self.end = pd.Timestamp(end)
        self.cache = cache

    @property
    def cache(self):
        return self._cache

    @property
    def columns(self):
        return [
            'name',
            'description',
            'exchangeCode',
        ]

    @cache.setter
    def cache(self, c):
        os.makedirs(c, exist_ok=True)
        self._cache = c

    @property
    def store(self):
        return os.path.join(self.cache, f'{self.symbol}_meta.feather')

    def read(self):
        """
        Downloads meta data for a single symbol.  The resulting internal
        pandas.DataFrame has the following index and column names:
            - columns:  ('name', 'description', 'exchange')

        Cache the data in a feather store for subsequent calls.
        """
        if os.path.isfile(self.store):
            return pd.read_feather(self.store).set_index('symbol')

        args = SYMBOLS.validate(
            symbol=self.symbol,
            start=self.start,
            end=self.end,
        )

        dr = pdr.tiingo.TiingoMetaDataReader(**args)
        try:
            df = dr.read()
        except Exception as e:
            raise ValueError(e)

        df = df.transpose().get(self.columns).reset_index(drop=True)

        print(df.drop('description', axis=1).to_string())
        print('-'*45)

        df.to_feather(self.store)
        dr.close()

        return df


def _meta_single(symbol, start, end):
    try:
        return MetaSingle(symbol, start, end).read()
    except ValueError:
        pass


class MetaBatch(object):

    def __init__(self, symbols, start, end, cache='meta'):
        """
        Multiple symbol Tiingo Meta data download class.  Must have
        environment variable TIINGO_API_KEY set or authentication.

        Parameters
        ----------
        symbols : seq
            sequence of strings representing company tickers
        start : str or datetime.date compatible object
            download data starting on this date
        end : str or datetime.date compatible object
            download data ending on this date
        cache : str, default 'meta'
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
    def store(self):
        input = '-'.join(sorted(set(self.symbols)))
        output = hashlib.md5(input.encode('utf-8')).hexdigest()
        return os.path.join(self.cache, f'tiingo-meta-{output}.feather')

    def read(self):
        """
        Downloads meta data for a sequence of symbols.  The resulting internal
        pandas.DataFrame has the following index and column names:
            - index : 'symbol'
            - columns:  ('name', 'description', 'exchange')

        Cache the data in a feather store for subsequent calls.
        """
        if os.path.isfile(self.store):
            return pd.read_feather(self.store).set_index('symbol')

        results = mp.amap(_meta_single, self.symbols, start=self.start, end=self.end)

        df = pd.concat(results).droplevel(1)
        df.index.name = 'symbol'
        df.reset_index().to_feather(self.store)

        return df
