import numpy as np
import pandas as pd

from sklearn.base import BaseEstimator, TransformerMixin

from FunctionsForFeatureAdding import AvgHighCloseVolatilityRecursion, GetRSI
from FunctionsForFeatureAdding import GetMACD, GetTarget

class ColumnAdder(BaseEstimator, TransformerMixin):
    def __init__(self, remove_outliers=False):
        self.remove_outliers = remove_outliers
        
    
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
            
            target = GetTarget(close, j=4)
            
            dfs = [curr, volatilities, rsi, macd, target]
            curr_trans = pd.concat(dfs, axis=1)
                        
            curr_trans_no_nan = curr_trans.dropna(axis=0)
            cols_to_drop = ['index', 'Date', 'Open', 'High', 'Low', 'Close',
                            'Volume', 'Ticker']
            
            final_trans = curr_trans_no_nan.drop(cols_to_drop, axis=1)
            
            df = df.append(final_trans)
        
        # Reset index on df
        df.reset_index(drop=True, inplace=True)
        
        if self.remove_outliers == True:
            # Save the outlier numbers trained on.
            
            outlier_values = []
            
            num_features = df.select_dtypes(include='number').columns
                        
            indices_no_outliers = df.index
            
            boxplot_removals = ['HighCloseVolAvg_1', 'HighCloseVolAvg_10', 'HighCloseVolAvg_20']
            
            for feat in boxplot_removals:
                q1 = df[feat].quantile(q=0.25)
                q3 = df[feat].quantile(q=0.75)
            
                iqr = q3-q1
            
                lower = q1-1.5*iqr
                upper = q1+1.5*iqr
                
                outlier_values.append([feat, lower, upper])
                
                no_outliers = df[(df[feat]>lower) & (df[feat]<upper)]
                idx = no_outliers.index
                
                indices_no_outliers = np.intersect1d(indices_no_outliers, idx)
                
            normal_removals = [x for x in num_features if x not in boxplot_removals]
            
            for feat in normal_removals:
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
    
    
df = pd.read_csv('TechStockDataForModel.csv')

df_prep = ColumnAdder(remove_outliers=False).fit_transform(df)

df_prep.to_csv('TechStockDataForModelPrepped.csv', index=False)

df_prep_no_outliers = ColumnAdder(remove_outliers=True).fit_transform(df)

df_prep_no_outliers.to_csv('TechStockDataForModelPreppedNoOutliers.csv', index=False)