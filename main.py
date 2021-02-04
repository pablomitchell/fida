
import pandas
import matplotlib.pylab as plt
from pandas_datareader import tiingo


plt.style.use('seaborn')

if __name__ == '__main__':

    symbols = [
        'AAPL',
        'MSFT',
        'GOOG',
    ]

    dr = tiingo.TiingoDailyReader(
        symbols=symbols,
        start='2020-01-01',
        end='2020-12-31',
    )
    df = dr.read()
    dr.close()

    df.info()
