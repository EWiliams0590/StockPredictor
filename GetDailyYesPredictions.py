from DataTransformationForModelEvaluation import FeatureAdder

from joblib import load

from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np

import yfinance as yf
from datetime import date, timedelta

def get_tickers():
    """
    Get tickers from a search using a Yahoo Finance screener.
    """
    tickers = []
    
    i = 0
    
    while i > -1:
        curr_tickers = []
        url = f'https://finance.yahoo.com/screener/unsaved/64413ad6-3475-4e94-a132-f5a7406404e5?dependentField=sector&dependentValues=Technology&offset={i}&count=100'
        html = requests.get(url).text
        soup = BeautifulSoup(html, 'lxml')    
        table = soup.find_all('tr')[1:]

        for j in range(len(table)):
            ticker = table[j].find_all('td', attrs={'aria-label': 'Symbol'})[0].text
            curr_tickers.append(ticker)
    
        if len(curr_tickers) > 0:
            tickers.extend(curr_tickers)
            i += 100 
        else:
            i = -1
            
    return tickers

tickers = get_tickers()



# Add in new date data
def get_ticker_data(ticker):
    ticker_name = yf.Ticker(ticker)

    start = date.today()-timedelta(days=50)
    end = date.today()

    df1 = ticker_name.history(start=start, end=end, actions=False)
    
    # If there is not at least 30 days worth of data, do not use this ticker
    if df1.shape[0] < 30:
        return None
    else:
        df1['Ticker'] = ticker
        return df1
    
    
def get_df_for_tickers(tickers):
    df = pd.DataFrame()
    for ticker in tickers:
        curr = get_ticker_data(ticker)
        df = df.append(curr)
        
    return df


df = get_df_for_tickers(tickers)


df_trans = FeatureAdder().fit_transform(df)

# Remove data with any outlier values
outlier_values = pd.read_csv('OutlierValues.csv', index_col='Ticker')


for feat in outlier_values.index:
    low = outlier_values.loc[feat]['Low']
    high = outlier_values.loc[feat]['High']
    
    df_trans = df_trans[(df_trans[feat]>low) & (df_trans[feat]<high)]
    
    
model = load('FinalStockModel.joblib')

pred = model.predict(df_trans)
prob = model.predict_proba(df_trans)[:,1]

data=np.column_stack((pred, prob))

columns = ['Prediction', 'Probability']
results = pd.DataFrame(index=df_trans.index, data=data, columns=columns)

today = results.index[0][1]
today = str(today).split(' ')[0]

yes = results[results['Prediction']=='Yes'].sort_values(by='Probability', 
                                                        ascending=False)

yes.to_csv(f'StockPicks{today}.csv')
