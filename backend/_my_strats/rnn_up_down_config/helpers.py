# -*- coding: utf-8 -*-

import numpy as np
import random
from datetime import datetime
from collections import deque
import math

def create_timeseries(df, prev_range, num_out, shuffle=True):
    # Gera lista historica
    sequential_data = []
    prev_days = deque(maxlen=prev_range)
    
    for i in df.values:
        prev_days.append([n for n in i[num_out:]])
        dependents = i[:num_out]
        if len(prev_days) == prev_range:
            sequential_data.append([np.array(prev_days),dependents]) # histórico , min
    
    if shuffle: random.shuffle(sequential_data)
    
    # X y generation
    X = []
    y = []
    for seq, target in sequential_data:
        X.append(seq)
        y.append(target)
        
    return np.array(X), np.array(y)

def cast_date(date):
    return datetime(*(list(map(int,date.split('.')[::-1]))))

def mean_absolute_percentage_error(y_true, y_pred): 
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100

def remove_random_list(list1):
    choosen = random.sample(range(len(list1)), np.random.randint(len(list1) + 1))
    list2 = []
    for c in choosen:
        list2.append(list1[c])
    return list2

def df_reorder(df, column1, column2):
    cols = df.columns.tolist()
    cols[column1], cols[column2] = cols[column2], cols[column1]
    df = df[cols]
    return df

def df_reorder_rng(df, start, end, pos=0, pos_end=False):    
    cols = df.columns.tolist()
    if end is None:
        temp = cols[start:]
        cols = cols[:start]
    else:
        temp = cols[start:end]
        cols = cols[:start] + cols[end:]
    if pos_end:
        cols = cols + temp
    else:
        for e in temp[::-1]: cols.insert(pos, e)
    df = df[cols]
    return df

def mkdir_conditional(folder):    
    import os
    if not os.path.exists(folder):
        os.makedirs(folder)

def pocid(current, future):
    return 1 if future > current else 0

def pocid_series(current_series, future_series):
    return list(map(pocid, current_series, future_series))

def macd_series(series, nslow, nfast):
    emaslow = series.ewm(span=nslow, adjust=False).mean()
    emafast = series.ewm(span=nfast, adjust=False).mean()
    return emafast - emaslow
        
def rsi_series(close_series, window):
    #close_series should be date DESC
    delta = close_series.diff()
    delta = delta[1:]
    
    up, down = delta.copy(), delta.copy()
    up[up < 0] = 0
    down[down > 0] = 0
    
    roll_up = up.ewm(span=window, adjust=False).mean()
    roll_down = down.abs().ewm(span=window, adjust=False).mean()
    
    RS = roll_up / roll_down
    RSI = 100.0 - (100.0 / (1.0 + RS))
    return RSI

def get_random(arr):
    return arr[np.random.randint(0,len(arr))]