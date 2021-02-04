
import pandas
import pandas_datareader.tiingo as tiingo
import matplotlib.pylab as plt


plt.style.use('seaborn')


allowed_exchanges = [
    'NASDAQ',
    'NYSE',
    'NYSE ARCA',
    'NYSE MKT',
]

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


    # client = TiingoClient()
    # tickers = client.list_stock_tickers()
    # tickers_df = pd.DataFrame(tickers)
    # tickers_usd_df = tickers_df.query('exchange in @allowed_exchanges')
    #
    # df = client.get_dataframe(
    #     'SPY',
    #     startDate='1990-01-01',
    #     endDate='2020-12-31',
    #     frequency='daily',
    # )
    #
    # df.info()
    # print(df.tail().to_string())
    # print(df.head().to_string())
    #
    # df.divCash.plot()
    # plt.show()
