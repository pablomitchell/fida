"""
Lightweight constituents functionality
"""

import pandas as pd
import pandas_datareader as pdr
import requests
from bs4 import BeautifulSoup


def get_msci_eafe_country_etfs():
    """
    Get MSCI EAFE country ETF constituents

    Returns
    -------
    constituents : panda.DataFrame
        columns:  ['ticker', 'name', 'bucket']

    """
    return pd.DataFrame({
        'ticker': [
            'EWA',  # 'Australia',
            'EWO',  # 'Austria',
            'EWK',  # 'Belgium',
            'EDEN',  # 'Denmark',
            'EFNL',  # 'Finland',
            'EWQ',  # 'France',
            'EWG',  # 'Germany',
            'EWH',  # 'Hong Kong',
            'EIRL',  # 'Ireland',
            'EIS',  # 'Israel',
            'EWI',  # 'Italy',
            'EWJ',  # 'Japan',
            'EWN',  # 'Netherlands',
            'ENZL',  # 'New Zealand',
            'ENOR',  # 'Norway',
            # 'XXX',  # 'Portugal',
            'EWS',  # 'Singapore',
            'EWP',  # 'Spain',
            'EWD',  # 'Sweden',
            'EWL',  # 'Switzerland',
            'EWU',  # 'United Kingdom',
        ],
        'name': [
            'iShares MSCI Australia ETF',
            'iShares MSCI Austria ETF',
            'iShares MSCI Belgium ETF',
            'iShares MSCI Denmark ETF',
            'iShares MSCI Finland ETF',
            'iShares MSCI France ETF',
            'iShares MSCI Germany ETF',
            'iShares MSCI Hong Kong ETF',
            'iShares MSCI Ireland ETF',
            'iShares MSCI Israel ETF',
            'iShares MSCI Italy ETF',
            'iShares MSCI Japan ETF',
            'iShares MSCI Netherlands ETF',
            'iShares MSCI New Zealand ETF',
            'iShares MSCI Norway ETF',
            # 'iShares MSCI Portugal ETF',
            'iShares MSCI Singapore ETF',
            'iShares MSCI Spain ETF',
            'iShares MSCI Sweden ETF',
            'iShares MSCI Switzerland ETF',
            'iShares MSCI United Kingdom ETF',
        ],
        'bucket': [
            'Australia',
            'Austria',
            'Belgium',
            'Denmark',
            'Finland',
            'France',
            'Germany',
            'Hong Kong',
            'Ireland',
            'Israel',
            'Italy',
            'Japan',
            'Netherlands',
            'New Zealand',
            'Norway',
            # 'Portugal',
            'Singapore',
            'Spain',
            'Sweden',
            'Switzerland',
            'United Kingdom',
        ],
    })


def get_sp500():
    """
    Scrape S&P 500 constituents from Wikipedia

    Returns
    -------
    constituents : panda.DataFrame
        columns:  ['ticker', 'name', 'bucket']

    """
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'class': 'wikitable sortable'})
    ticker, name, bucket = [], [], []

    for row in table.findAll('tr')[1:]:
        td = row.findAll('td')
        ticker.append(td[0].text.replace('.', '-').strip())
        name.append(td[1].text.strip())
        bucket.append(td[3].text.strip())

    return pd.DataFrame({'ticker': ticker, 'name': name, 'bucket': bucket})


def get_sp500_sector_etfs():
    """
    Get S&P 500 sector ETF constituents

    Returns
    -------
    constituents : panda.DataFrame
        columns:  ['ticker', 'name', 'bucket']

    """
    return pd.DataFrame({
        'ticker': [
            'XLC',  # communication
            'XLY',  # consumer discretionary
            'XLP',  # consumer staples
            'XLE',  # energy
            'XLF',  # finance
            'XLV',  # health care
            'XLI',  # industrials
            'XLB',  # materials
            'XLRE',  # real estate
            'XLK',  # technology
            'XLU',  # utilities
        ],
        'name': [
            'SP Communication Services ETF',
            'SP Consumer Discretionary ETF',
            'SP Consumer Staples ETF',
            'SP Energy ETF',
            'SP Financials ETF',
            'SP Health Care ETF',
            'SP Industrials ETF',
            'SP Materials ETF',
            'SP Real Estate ETF',
            'SP Technology ETF',
            'SP Utilities ETF',
        ],
        'bucket': [
            'Communication Services',
            'Consumer Discretionary',
            'Consumer Staples',
            'Energy',
            'Financials',
            'Health Care',
            'Industrials',
            'Materials',
            'Real Estate',
            'Technology',
            'Utilities',
        ]
    })


def get_sp600():
    """
    Scrape S&P 600 constituents from Wikipedia

    Returns
    -------
    constituents : panda.DataFrame
        columns:  ['ticker', 'name', 'bucket']

    """
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_600_companies'
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'class': 'wikitable sortable'})
    ticker, name, bucket = [], [], []

    for row in table.findAll('tr')[1:]:
        td = row.findAll('td')
        ticker.append(td[1].text.replace('.', '-').strip())
        name.append(td[0].text.strip())
        bucket.append(td[3].text.strip())

    return pd.DataFrame({'ticker': ticker, 'name': name, 'bucket': bucket})


def get_psuedo_knuteson_index():
    """
    Psuedo Knuteson Index

    Returns
    -------
    constituents : panda.DataFrame
        columns:  ['ticker', 'name', 'bucket']

    """
    return pd.DataFrame({
        'ticker': [
            'SPY',  # SP500
            'QQQ',  # Nasdaq
            'EWA',  # Australia
            'EWC',  # Canada
            'EWG',  # Germany
            'EWH',  # Hong Kong
            'EWI',  # Italy
            'EWJ',  # Japan
            'EWN',  # Netherlands
            'EWQ',  # France
            'EWS',  # Singapore
            'EWT',  # Taiwan
            'EWU',  # United Kingdom
            'EWW',  # Mexico
            'EWY',  # Korea
            'EWZ',  # Brazil
            'EIS',  # Israel
            'ENOR',  # Norway
            'INDA',  # India
            'MCHI',  # China

        ],
        'name': [
            'SSGA S&P 500 ETF',
            'Invesco Nasdaq ETF',
            'iShares MSCI Australia ETF',
            'iShares MSCI Canada ETF',
            'iShares MSCI Germany ETF',
            'iShares MSCI Hong Kong ETF',
            'iShares MSCI Italy ETF',
            'iShares MSCI Japan ETF',
            'iShares MSCI Netherlands ETF',
            'iShares MSCI France ETF',
            'iShares MSCI Singapore ETF',
            'iShares MSCI Taiwan ETF',
            'iShares MSCI United Kingdom ETF',
            'iShares MSCI Mexico ETF',
            'iShares MSCI Korea ETF',
            'iShares MSCI Brazil ETF',
            'iShares MSCI Israel ETF',
            'iShares MSCI Norway ETF',
            'iShares MSCI India ETF',
            'iShares MSCI China ETF',
        ],
        'bucket': [
            'United States',
            'United States',
            'Australia',
            'Canada',
            'Germany',
            'Hong Kong',
            'Italy',
            'Japan',
            'Netherlands',
            'France',
            'Singapore',
            'Taiwan',
            'United Kingdom',
            'Mexico',
            'Korea',
            'Brazil',
            'Israel',
            'Norway',
            'India',
            'China',
        ],
    })


def get_short_term_bond_etfs():
    """
    Short-term Bond ETFs

    Returns
    -------
    constituents : panda.DataFrame
        columns:  ['ticker', 'name', 'bucket']

    """
    return pd.DataFrame({
        'ticker': [
            'BWZ',
            'EMSH',
            'ISHG',
            'SCHO',
            'SHY',
            'SPTS',
            'STIP',
            'USFR',
            'VGSH',
        ],
        'name': [
            'SPDR Barclays Capital Short Term International Treasury Bond ETF',
            'ProShares Short Term USD Emerging Markets Bond ETF',
            'iShares 1-3 Year International Treasury Bond ETF',
            'Schwab Short-Term U.S. Treasury ETF',
            'iShares 1-3 Year Treasury Bond ETF',
            'SPDR Portfolio Short Term Treasury ETF',
            'iShares 0-5 Year TIPS Bond ETF',
            'WisdomTree Bloomberg Floating Rate Treasury Fund',
            'Vanguard Short-Term Treasury ETF',
        ],
        'bucket': [
            'Fixed-Income',
            'Fixed-Income',
            'Fixed-Income',
            'Fixed-Income',
            'Fixed-Income',
            'Fixed-Income',
            'Fixed-Income',
            'Fixed-Income',
            'Fixed-Income',
        ],
    })


def get_tiingo_common_stock_us(start, end):
    qstr = (
        f'(("{start}" <= startDate) or (startDate <= "{end}")) and '
        f'(("{start}" <= endDate) or (endDate <= "{end}")) and '
        f'((exchange == "NYSE") or (exchange == "NASDAQ")) and '
        f'(assetType == "Stock") and '
        f'(priceCurrency == "USD")'
    )
    symbols = pdr.tiingo.get_tiingo_symbols().query(qstr)
    not_preferred_stock = ~symbols.ticker.str.contains('-P-')
    symbols = symbols.loc[not_preferred_stock]

    return symbols.ticker.dropna().sort_values().unique()

