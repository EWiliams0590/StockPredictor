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
        

def AvgHighCloseVolatilityRecursion(high, close, list_of_num_days):
    """
    Run AvgHighCloseVolatility
    for all of the given days in list_of_num_days.
    returns df. Each col is AvgHighCloseVolatility for a
    num_days in list_of_num_days.
    """
    avg_list = []
    for num_days in list_of_num_days:
        avg_ser = AvgHighCloseVolatility(high, close, num_days)
        avg_list.append(avg_ser)
    
    avg_df = pd.concat([x for x in avg_list], axis=1)
    return avg_df


def GetRSI(close, avgs=[3, 10], time_period=14):
    """
    Input close prices of a ticker for at least time_period days
    and a list for the average RSI from the past days
    Get out the RSI and averages.
    """
    # RSI
    RSI = ta.RSI(close, timeperiod=time_period).rename('RSI')
    
    ser_of_avgs = []
    
    for i in avgs:   
        list_of_avgs = [np.nan]*(i-1)
        
        for j in range(i-1, RSI.shape[0]):
            avg = RSI[j-(i-1):j+1].mean()
            list_of_avgs.append(avg)
        # create series
        name = f'RSI_{i}_day_avg'
        curr_ser = pd.Series(data=list_of_avgs, 
                             index=RSI.index, 
                             name=name)
        
        ser_of_avgs.append(curr_ser)
    

  
    feats_to_use = [RSI] + [x for x in ser_of_avgs]
    
    RSI_df = pd.concat(feats_to_use, axis=1)                 
    
    return RSI_df     

    

def VolumeRatio(volume, n_days_small=3, n_days_large=20):
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
                large_vol_avg = np.mean(volume[i-(n_days_large-1):i])
                small_vol_avg = np.mean(volume[i-(n_days_small-1):i])
                
                if large_vol_avg == 0: # small_vol_avg == 0 as well
                    ratios.append(0)
                    
                else:
                    ratio = small_vol_avg/large_vol_avg
                    ratios.append(ratio)

            ratios = pd.Series(data=ratios, index=volume.index, name=name)

            return ratios


def VolumeRatiosRecursion(volume, list_of_days):
    """
    Get volume ratios for list of days, where
    list_of_days is a list of pairs of days in
    the order of (n_days_small, n_days_large)"""
    vols_list = []
    
    for days in list_of_days:
        n_days_small=days[0]
        n_days_large=days[1]
        vol_ratio = VolumeRatio(volume, n_days_small, n_days_large)
        vols_list.append(vol_ratio)
        
    vols_df = pd.concat([x for x in vols_list], axis=1)
    return vols_df


def GetMACD(close):
    macd, macdsignal, macdhist = ta.MACDFIX(close)
    
    macd = macd.rename('MACD')
    macdsignal = macdsignal.rename('MACDSignal')
    macdhist = macdhist.rename('MACDHist')
    
    feats_to_use = [macd, macdhist]
    
    macd_df = pd.concat(feats_to_use, axis=1)
    
    return macd_df
    
    
def GetTarget(close, j=4):
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
    sp_changes_ser = pd.Series(sp_changes, index=close.index, name='SP_change')
    
    
    sp_changes_cond = np.where(sp_changes>=0.0225, 'Yes', np.where(np.isnan(sp_changes), np.nan, 'No'))
    sp_changes_cond = pd.Series(sp_changes_cond, index=close.index, name='Target')
    sp_changes_cond = sp_changes_cond.map({'nan': np.nan, 'Yes': 'Yes', 'No': 'No'})
    
    target_df = pd.concat([sp_changes_ser, sp_changes_cond], axis=1)
    return target_df

