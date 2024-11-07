import asyncio
import io
import warnings

import nest_asyncio
import numpy as np
import pandas as pd
import pandas_datareader as pdr
import requests_cache
import yfinance as yf
from loguru import logger
from pyrate_limiter import Duration, Limiter, RequestRate, SQLiteBucket
from requests import Session  # type: ignore
from requests_ratelimiter import LimiterMixin
from tqdm.auto import tqdm

from fida.patches import patch_pandas_datareader

nest_asyncio.apply()
warnings.simplefilter(action="ignore", category=FutureWarning)

patch_pandas_datareader()


class CachedLimiterSession(LimiterMixin, Session):
    pass


session_yahoo = CachedLimiterSession(
    limiter=Limiter(
        RequestRate(2, Duration.SECOND * 5),  # max 2 requests per 5 seconds
        bucket_class=SQLiteBucket,
        bucket_kwargs={"path": "yahoo.cache"},
    )
)
session_tiingo = requests_cache.CachedSession(
    cache_name="tiingo.cache", backend="sqlite"
)


# Symbols = Union[str, list[str]]
Symbols = str | list[str]


async def read_symbol_yahoo_async(
    symbol: str,
    start: str,
    end: str,
    field: str,
) -> pd.DataFrame:
    """Read a single symbol"""
    df = yf.Ticker(symbol, session=session_yahoo).history(
        start=start,
        end=end,
    )
    df = df.get(field).rename(symbol)
    df.index = pd.to_datetime(df.index.date)
    return df


async def read_symbols_yahoo_async(
    symbols: Symbols, start: str, end: str, field: str
) -> pd.DataFrame:
    """Read a collection of symbols"""
    if isinstance(symbols, str):
        symbols = [symbols]

    dfs = []
    for symbol in tqdm(symbols, desc="Yahoo Download"):
        df = await read_symbol_yahoo_async(
            symbol=symbol, start=start, end=end, field=field
        )

        if not df.empty:
            dfs.append(df)

    df = pd.concat(dfs, axis=1).sort_index(axis="columns")
    return df


def get_field_yahoo(
    symbols: Symbols,
    start: str,
    end: str,
    field: str,
    interpolate: bool = False,
) -> pd.DataFrame:
    """Get a field for a collection of symbols"""
    out = asyncio.run(
        read_symbols_yahoo_async(
            symbols=symbols,
            start=start,
            end=end,
            field=field,
        )
    )

    if interpolate:
        out = out.interpolate(axis=0, method="pchip")

    buffer = io.StringIO()
    out.info(buf=buffer)
    logger.info(f"\n{buffer.getvalue()}")

    return out


def get_price_yahoo(
    symbols: Symbols,
    start: str,
    end: str,
    interpolate: bool = False,
) -> pd.DataFrame:
    return get_field_yahoo(
        symbols=symbols,
        start=start,
        end=end,
        field="Close",
        interpolate=interpolate,
    )


def get_volume_yahoo(
    symbols: Symbols,
    start: str,
    end: str,
    interpolate: bool = False,
) -> pd.DataFrame:
    return get_field_yahoo(
        symbols=symbols,
        start=start,
        end=end,
        field="Volume",
        interpolate=interpolate,
    )


def get_return_yahoo(
    symbols: Symbols,
    start: str,
    end: str,
    interpolate: bool = False,
    log: bool = False,
) -> pd.DataFrame:
    prices = get_price_yahoo(
        symbols=symbols,
        start=start,
        end=end,
        interpolate=interpolate,
    )

    if log:
        return np.log(prices).diff()
    else:
        return prices.pct_change()


# ----------------------------------------------------------------------------- #


async def read_symbol_tiingo_async(
    symbol: str,
    start: str,
    end: str,
    field: str,
) -> pd.DataFrame:
    """Read a single symbol"""
    try:
        df = pdr.get_data_tiingo(
            symbol,
            start=start,
            end=end,
            session=session_tiingo,
        )
    except KeyError:
        logger.warning(f"Symbol {symbol} not found")
        return pd.DataFrame()
    else:
        df = df.get(field).droplevel(0).rename(symbol)
        df.index = pd.to_datetime(df.index.date)
        return df


async def read_symbols_tiingo_async(
    symbols: Symbols, start: str, end: str, field: str
) -> pd.DataFrame:
    """Read a collection of symbols"""
    if isinstance(symbols, str):
        symbols = [symbols]

    dfs = []
    for symbol in tqdm(symbols, desc="Tiingo Download"):
        df = await read_symbol_tiingo_async(
            symbol=symbol,
            start=start,
            end=end,
            field=field,
        )

        if not df.empty:
            dfs.append(df)

    df = pd.concat(dfs, axis=1).sort_index(axis="columns")
    return df


def get_field_tiingo(
    symbols: Symbols,
    start: str,
    end: str,
    field: str,
    interpolate: bool = False,
) -> pd.DataFrame:
    """Get a field for a collection of symbols"""
    out = asyncio.run(
        read_symbols_tiingo_async(
            symbols=symbols,
            start=start,
            end=end,
            field=field,
        )
    )

    if interpolate:
        out = out.interpolate(axis=0, method="pchip")

    buffer = io.StringIO()
    out.info(buf=buffer)
    logger.info(f"\n{buffer.getvalue()}")

    return out


def get_price_tiingo(
    symbols: Symbols,
    start: str,
    end: str,
    interpolate: bool = False,
) -> pd.DataFrame:
    return get_field_tiingo(
        symbols=symbols,
        start=start,
        end=end,
        field="adjClose",
        interpolate=interpolate,
    )


def get_volume_tiingo(
    symbols: Symbols,
    start: str,
    end: str,
    interpolate: bool = False,
) -> pd.DataFrame:
    return get_field_tiingo(
        symbols=symbols,
        start=start,
        end=end,
        field="adjVolume",
        interpolate=interpolate,
    )


def get_return_tiingo(
    symbols: Symbols,
    start: str,
    end: str,
    interpolate: bool = False,
    log: bool = False,
) -> pd.DataFrame:
    prices = get_price_tiingo(
        symbols=symbols,
        start=start,
        end=end,
        interpolate=interpolate,
    )

    if log:
        return np.log(prices).diff()
    else:
        return prices.pct_change()


# ----------------------------------------------------------------------------- #


async def read_msymbol_tiingo_async(symbol: str, start: str, end: str) -> pd.Series:
    out = (
        pdr.tiingo.TiingoMetaDataReader(
            symbol,
            start=start,
            end=end,
            session=session_tiingo,
        )
        .read()
        .squeeze()
    )
    return out


async def read_msymbols_tiingo_async(
    symbols: Symbols, start: str, end: str
) -> pd.DataFrame:
    out = {}

    if isinstance(symbols, str):
        symbols = [symbols]

    for symbol in tqdm(symbols, desc="Tiingo Download"):
        out[symbol] = await read_msymbol_tiingo_async(
            symbol=symbol, start=start, end=end
        )

    out = pd.DataFrame(out)
    return out


def get_meta(symbols: Symbols, start: str, end: str) -> pd.Series:
    out = asyncio.run(
        read_msymbols_tiingo_async(
            symbols=symbols,
            start=start,
            end=end,
        )
    )
    out = out.transpose()

    buffer = io.StringIO()
    out.info(buf=buffer)
    logger.info(f"\n{buffer.getvalue()}")

    return out
