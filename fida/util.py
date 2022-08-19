import pandas as pd
import pandas_datareader as pdr


class Symbols(object):

    def __init__(self):
        self.symbols = (
            pdr
            .tiingo.get_tiingo_symbols()
            .dropna()
            .assign(start=lambda x: pd.to_datetime(x.startDate))
            .assign(end=lambda x: pd.to_datetime(x.endDate))
            .get(["ticker", "start", "end"])
            .set_index("ticker")
        )

    def validate(self, symbol, start, end):
        if symbol not in self.symbols:
            err = f"{symbol} not covered by fida"

        record = self.symbols.loc[symbol]

        if not isinstance(record, pd.Series):
            # means "symbol" has valid data on multiple disjoint dates
            # should handle this case but taking the easy way out for now
            err = f"{symbol} is either empty or has multiple records"
            raise ValueError(symbol)

        if end < record.start or record.end < start:
            err = f"only have {symbol} for: {record.start} to {record.end}"
            raise ValueError(err)

        record.start = max(record.start, start)
        record.end = min(record.end, end)

        args = record.to_dict()
        args["symbols"] = symbol

        return args


SYMBOLS = Symbols()


