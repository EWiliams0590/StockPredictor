import numpy as np
import pandas as pd

from sklearn.base import BaseEstimator, TransformerMixin

from FunctionsForFeatureAdding import AvgHighCloseVolatility, GetRSI
from FunctionsForFeatureAdding import GetTarget, GetSPChanges

class ColumnAdder(BaseEstimator, TransformerMixin):
    def __init__(self, remove_outliers=False, keep=True):
        self.remove_outliers = remove_outliers
        self.keep = keep
        
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        tickers = X['Ticker'].unique()
        
        df = pd.DataFrame()
        
        for ticker in tickers:
            curr = X[X['Ticker']==ticker].reset_index(drop=True)
                        
            close = curr['Close']
            high = curr['High']
            
            # Volatilities
            list_for_volatilities = [1, 5, 20]
            volatilities = []
            
            for i in list_for_volatilities:
                vol = AvgHighCloseVolatility(high, close, num_days=i)
                volatilities.append(vol)
            
            # RSI
            list_of_rsis = [10]
            rsis = []
            
            for i in list_of_rsis:  
                rsi = GetRSI(close, i)
                rsis.append(rsi)
            
            # SP_changes
            list_of_sp_changes = [1, 3, 5, 10]
            sp_changes = []
            
            for i in list_of_sp_changes:
                sp_change = GetSPChanges(close, i)
                sp_changes.append(sp_change)
                
            # Target Column(s)
            target = GetTarget(close, j=4)
            
            # Concatenate all data
            transformed_dfs = rsis
            transformed_dfs.extend(volatilities)
            transformed_dfs.extend(sp_changes)
            transformed_dfs.append(target)                
            
            if self.keep == True:
                transformed_dfs.append(curr)
                
            curr_trans = pd.concat(transformed_dfs, axis=1)
            final_trans = curr_trans.dropna(axis=0)
            
            df = df.append(final_trans)
        
        # Reset index on df
        df.reset_index(drop=True, inplace=True)
        
        if self.remove_outliers == True:
            # Save the outlier numbers trained on.
            
            outlier_values = []
            
            num_features = df.select_dtypes(include='number').columns.drop('SP_change_Target', axis=1)
                        
            indices_no_outliers = df.index
            
            for feat in num_features:
                mean = df[feat].mean()
                std = df[feat].std()
                
                lower = mean - 3*std
                upper = mean + 3*std
                if feat != 'SP_change':
                    outlier_values.append((feat, lower, upper))
                
                no_outliers = df[(df[feat]>lower) & (df[feat]<upper)]
                
                idx = no_outliers.index
                
                indices_no_outliers = np.intersect1d(indices_no_outliers, idx)
                
            
            outlier_values_df = pd.DataFrame(data=outlier_values,
                                             columns=['Ticker', 'Low', 'High'])
            
            outlier_values_df = outlier_values_df.set_index('Ticker')
            
            outlier_values_df.to_csv('OutlierValues.csv')
            
            no_outliers = df.loc[indices_no_outliers]
            
            return no_outliers
        
        else:
            return df