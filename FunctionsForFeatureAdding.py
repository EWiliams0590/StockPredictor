import numpy as np
import pandas as pd

import talib as ta


def AvgHighCloseVolatility(high, close, num_days):
    """
    Define High-Close Volatility as (High-Close)/Close for a given day.
    Find the average over the past num_days days.
    """
    high_close_vols = []
    N = high.shape[0]
    name = f'HighCloseVolAvg_{num_days}'
    
    if num_days > N:
        print("num_days large than length of df. Use smaller num_days")
    elif num_days < 1:
        print(f"num_days must be positive. Did not compute for num_days={num_days}")
    else:
        for i in range(N):
            high_close_vol = (high[i]-close[i])/close[i]
            high_close_vols.append(high_close_vol)
        
        if num_days == 1:
            avgs_ser = pd.Series(data=high_close_vols, name=name, index=close.index)
        else:
            avgs = [np.nan]*(num_days-1)

            for i in range(num_days-1, N):
                curr_avg = np.mean(high_close_vols[i-(num_days-1):i+1])
                avgs.append(curr_avg)

            avgs_ser = pd.Series(data=avgs, name=name, index=close.index)
        
        return avgs_ser


def GetRSI(close, time_period):
    RSI = ta.RSI(close, timeperiod=time_period).rename(f'RSI_{time_period}')                
    return RSI    
    

def VolumeRatio(volume, n_days_small, n_days_large):
    """
    Calculates the ratio of the average volume from n_days_small
    over n_days_large. n_days_small < n_days_large.
    """
    if n_days_small < 1:
        print("Both day inputs must be positive.")
        print(f"Did not compute for n_days_small={n_days_small}")
    elif n_days_small >= n_days_large:
        print("n_days_small must be smaller than n_days_large.")
        print(f"Did not compute for n_days_small={n_days_small} and n_days_large={n_days_large}")
    else:
        N = volume.shape[0]
        name=f'Volume_{n_days_small}_over_{n_days_large}'

        if N < n_days_large:
            ratios = [np.nan]*N
            ratios = pd.Series(data=ratios, index=volume.index, name=name)
            return ratios
        else:
            ratios = [np.nan]*(n_days_large-1)

            for i in range(n_days_large-1, N):
                large_vol_avg = np.mean(volume[i-(n_days_large-1):i+1])
                small_vol_avg = np.mean(volume[i-(n_days_small-1):i+1])
                
                if large_vol_avg == 0: # small_vol_avg == 0 as well
                    ratios.append(0)
                    
                else:
                    ratio = small_vol_avg/large_vol_avg
                    ratios.append(ratio)

            ratios = pd.Series(data=ratios, index=volume.index, name=name)

            return ratios


def GetSPChanges(close, n_days):
    """
    Returns a series for the relative change in stock price  from
    n_days ago.
    """
    N = close.shape[0]
    changes = [np.nan]*n_days
    
    for i in range(n_days, N):
        curr = close[i]
        prev = close[i-n_days]
        change = (curr-prev)/curr
        changes.append(change)
    
    changes_ser = pd.Series(data=changes, index=close.index, name=f"SP_change_{n_days}")
    return changes_ser
        
def GetTarget(close, j=1):
    """
    Get the target column. Calculate the maximum
    SP (as a %) change starting from the given day through j
    days in the future. Base price is closing price for a day, and
    the SP Change is calculated using the maximum high over the next j days.
    """
    N = close.shape[0]
    sp_changes = []
    for i in range(N-j):
        curr_sp = close[i]
        futures = close[(i+1):(i+j+1)]
        max_future = np.max(futures)
        max_change = (max_future-curr_sp)/curr_sp
        sp_changes.append(max_change)
 
    sp_changes = np.append(np.array(sp_changes), [np.nan]*j)
    sp_changes_ser = pd.Series(sp_changes, index=close.index, name='SP_change_Target')
    
    
    sp_changes_cond = np.where(sp_changes>=0.0225, 'Yes', np.where(np.isnan(sp_changes), np.nan, 'No'))
    sp_changes_cond = pd.Series(sp_changes_cond, index=close.index, name='Target')
    sp_changes_cond = sp_changes_cond.map({'nan': np.nan, 'Yes': 'Yes', 'No': 'No'})
    
    target_df = pd.concat([sp_changes_ser, sp_changes_cond], axis=1)
    return target_df

