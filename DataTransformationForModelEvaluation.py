import pandas as pd

from sklearn.base import BaseEstimator, TransformerMixin

from FunctionsForFeatureAdding import AvgHighCloseVolatilityRecursion, GetRSI
from FunctionsForFeatureAdding import GetMACD


class FeatureAdder(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        tickers = X['Ticker'].unique()
        
        df = pd.DataFrame()
        
        for ticker in tickers:
            curr = X[X['Ticker']==ticker].reset_index()
            
            close = curr['Close']
            high = curr['High']
            
            list_for_volatilities = [1, 10, 20]
            volatilities = AvgHighCloseVolatilityRecursion(high, close, list_for_volatilities)
            
            rsi = GetRSI(close)
            
            macd = GetMACD(close)
                        
            dfs = [curr, volatilities, rsi, macd]
            curr_trans = pd.concat(dfs, axis=1)
                        
            curr_trans_no_nan = curr_trans.dropna(axis=0)
            cols_to_drop = ['Open', 'High', 'Low', 'Close',
                            'Volume']
            curr_trans_no_nan_dropped = curr_trans_no_nan.drop(cols_to_drop, axis=1)
            
            # Only keep the row with the final date
            last = curr_trans_no_nan_dropped['Date'].max()
            final_trans = curr_trans_no_nan_dropped[curr_trans_no_nan_dropped['Date']==last]
            
            # Set index to be ticker and date
            final = final_trans.set_index(['Ticker', 'Date'])
            
            df = df.append(final)
            
                            
        return df
    
