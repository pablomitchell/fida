from collections import OrderedDict

import pandas as pd
import pandas_datareader as pdr


def get_sp500():
    """
    Scrape S&P 500 constituents from Wikipedia

    Returns
    -------
    constituents : panda.DataFrame
        columns:  ["ticker", "name", "bucket"]

    """
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

    rename = OrderedDict()
    rename["Symbol"] = "ticker"
    rename["Security"] = "name"
    rename["GICS Sector"] = "bucket"

    frame_list = pd.read_html(url)

    frame = frame_list[0].rename(columns=rename)
    frame = frame.get(rename.values())
    frame["ticker"] = frame["ticker"].str.replace(".", "-")

    return frame


def get_sp600():
    """
    Scrape S&P 600 constituents from Wikipedia

    Returns
    -------
    constituents : panda.DataFrame
        columns:  ["ticker", "name", "bucket"]

    """
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_600_companies"

    rename = OrderedDict()
    rename["Ticker symbol"] = "ticker"
    rename["Company"] = "name"
    rename["GICS Sector"] = "bucket"

    frame_list = pd.read_html(url)

    frame = frame_list[1].rename(columns=rename)
    frame = frame.get(rename.values())
    frame["ticker"] = frame["ticker"].str.replace(".", "-")

    return frame
