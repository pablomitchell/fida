# mypy: ignore-errors
"""Patches for compatibility with newer pandas versions."""

import pandas as pd
from pandas_datareader.tiingo import TiingoDailyReader


def patch_pandas_datareader():
    """
    Patch pandas_datareader to work with newer pandas versions.
    """

    def patched_read(self):
        """Read data from Tiingo and return as DataFrame."""
        try:
            params = {
                "start": self.start.strftime("%Y-%m-%d"),
                "end": self.end.strftime("%Y-%m-%d"),
            }
            df = self._read_one_data(self.url, params=params)
            if isinstance(df, list):
                dfs = []
                for df_i in df:
                    df_i = pd.DataFrame(df_i)
                    dfs.append(df_i)
                return pd.concat(objs=dfs, axis=self._concat_axis)
            else:
                return pd.DataFrame(df)
        finally:
            self.close()

    TiingoDailyReader.read = patched_read
