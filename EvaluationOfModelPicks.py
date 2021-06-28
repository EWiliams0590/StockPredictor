### For determining how well the stock picks did for the week
import pandas as pd
from datetime import date, timedelta
import yfinance as yf



def add_SP_increase(date):
    """
    Parameters
    ----------
    date : The date to evaluate data from.

    Returns
    -------
    Writes SP_increase column to stock picks df.
    """
    today = date.today()
    filename = f'StockPicks{date}.csv'
    df = pd.read_csv(filename).set_index('Ticker')
    tickers = df.index
    SP_increases = []
    
    for ticker in tickers:
        curr_close = df.loc[ticker][f"Close on {date}"]
        ticker_name = yf.Ticker(ticker)
        start = date + timedelta(days=1)
        end = today
        ticker_df = ticker_name.history(start=start, end=end, actions=False)
        closes = ticker_df['Close']
        max_close = closes.max() # largest close
        SP_increase = (max_close-curr_close)/curr_close
        SP_increases.append(SP_increase)
    
    df['SP_increases'] = SP_increases
    
    df.to_csv(filename)
    
    
date = date(2021, 6, 21)

add_SP_increase(date)





