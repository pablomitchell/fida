from collections import OrderedDict

import pandas as pd


def get_sp500() -> pd.DataFrame:
    """
    Scrape S&P 500 constituents from Wikipedia

    Returns
    -------
    pd.DataFrame
        DataFrame with columns: ["ticker", "name", "bucket"]
    """
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    rename = OrderedDict(
        [("Symbol", "ticker"), ("Security", "name"), ("GICS Sector", "bucket")]
    )
    frame_list = pd.read_html(url)
    frame = frame_list[0].rename(columns=rename)
    frame = frame.get(rename.values())
    frame["ticker"] = frame["ticker"].str.replace(".", "-")
    return frame


def get_sp600() -> pd.DataFrame:
    """
    Scrape S&P 600 constituents from Wikipedia

    Returns
    -------
    pd.DataFrame
        DataFrame with columns: ["ticker", "name", "bucket"]
    """
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_600_companies"
    rename = OrderedDict(
        [("Ticker symbol", "ticker"), ("Company", "name"), ("GICS Sector", "bucket")]
    )
    frame_list = pd.read_html(url)
    frame = frame_list[1].rename(columns=rename)
    frame = frame.get(rename.values())
    frame["ticker"] = frame["ticker"].str.replace(".", "-")
    return frame
