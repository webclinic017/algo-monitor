# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import helpers as h
import requests
import io
import os
from yahoo_historical import Fetcher

# Date, Open, Close, Min, Max, Vol, Var

def vol_process(vol):
    if vol  == '-':
        return np.NaN
    if vol.find('K') != -1:
        return int(float(vol.replace('K','')) * 1000)
    if vol.find('M') != -1:
        return int(float(vol.replace('M','')) * 1000000)

def investing_csv(tkr, reset):
    poor_data = False
    
    if not reset:
        return pd.read_csv('stocks.csv'), poor_data

    os.system(f"cd manual_download && npm test --tkr={tkr}")    

    df = pd.read_csv('_stocks.csv')
    df.columns = ['Date','Close','Open','Max','Min','Vol','Var']
    #df = df.set_index(files[i][1][0])

    df = h.df_reorder(df, 1, 2)
    df = h.df_reorder(df, 3, 4)
    
    df = df.applymap(lambda x: x.replace(',','.'))
    df.iloc[:, -1] = df.iloc[:, -1].map(lambda x: x.replace('%',''))
    df.iloc[:, -2] = df.iloc[:, -2].map(vol_process)
    df.iloc[:, [1,2,3,4,6]] = df.iloc[:, [1,2,3,4,6]].applymap(lambda x: float(x))

    df[['Open','Max','Min','Close','Vol']] = df[['Open','Max','Min','Close','Vol']].applymap(lambda x: x if x != 0 else None)
    if df.isnull().sum().max() / len(df.index) > 0.3: poor_data = True
    df[['Open','Max','Min','Close','Vol']] = df[['Open','Max','Min','Close','Vol']].fillna(method='bfill')
    
    df = df.dropna()

    df.to_csv('stocks.csv')
    return df, poor_data
    
def alpha_vantage_api(tkr, reset):
    poor_data = False
    
    if not reset:
        return pd.read_csv('stocks.csv'), poor_data

    url = f'https://www.alphavantage.co/query?apikey=WU8VTI1IRD58LFV5&function=TIME_SERIES_DAILY_ADJUSTED&symbol={tkr}&datatype=csv&outputsize=full'
    data = requests.get(url).content
    df = pd.read_csv(io.StringIO(data.decode('utf-8')))
    
    df = df.rename(columns={
        'timestamp': 'Date',
        'open': 'Open',
        'adjusted_close': 'Close',
        'low': 'Min',
        'high': 'Max',
        'volume': 'Vol',
    })
    
    df.iloc[:,0] = list(map(lambda x: x.replace('-', '.'), df.iloc[:,0]))
    df['Date']= df['Date'].map(lambda x: '.'.join(x.split('.')[::-1]))

    df[['Open','Max','Min','Close','Vol']] = df[['Open','Max','Min','Close','Vol']].applymap(lambda x: x if x != 0 else None)
    if df.isnull().sum().max() / len(df.index) > 0.3 or len(df.index) < 50: poor_data = True
    df[['Open','Max','Min','Close','Vol']] = df[['Open','Max','Min','Close','Vol']].fillna(method='bfill')
    
    df['last_close'] = df['Close'].shift(-1)
    df['Var'] = list(map(lambda x,y: (x / y) - 1, df['Close'], df['last_close']))
    
    df = df.drop(['close', 'last_close', 'dividend_amount', 'split_coefficient'], axis=1)
    df = df[['Date', 'Open', 'Close', 'Min', 'Max', 'Vol', 'Var']]    
    #if df[['Vol']].sum(axis=0)[0] == 0: df = df.drop(columns=['Vol'])
    
    df = df.dropna()
    df.to_csv('stocks.csv')
    return df, poor_data

def yahoo_api(tkr, reset):
    poor_data = False
    if not reset:
        return pd.read_csv('stocks.csv'), poor_data
    
    data = Fetcher(tkr, [2000,1,1])
    df = data.getHistorical()
    
    df = df.drop(['Close'], axis=1)
    df = df.rename(columns={
        'High': 'Max',
        'Low': 'Min',
        'Adj Close': 'Close',
        'Volume': 'Vol'
    })
    df.iloc[:] = df.iloc[::-1].values
    
    df.iloc[:,0] = list(map(lambda x: x.replace('-', '.'), df.iloc[:,0]))
    df['Date']= df['Date'].map(lambda x: '.'.join(x.split('.')[::-1]))
    
    df['last_close'] = df['Close'].shift(-1)
    df['Var'] = list(map(lambda x,y: (x / y) - 1, df['Close'], df['last_close']))

    df[['Open','Max','Min','Close','Vol']] = df[['Open','Max','Min','Close','Vol']].applymap(lambda x: x if x != 0 else None)
    if df.isnull().sum().max() / len(df.index) > 0.3 or len(df.index) < 50: poor_data = True
    df[['Open','Max','Min','Close','Vol']] = df[['Open','Max','Min','Close','Vol']].fillna(method='bfill')
    
    df['last_close'] = df['Close'].shift(-1)
    df['Var'] = list(map(lambda x,y: (x / y) - 1, df['Close'], df['last_close']))
    
    df = df[['Date', 'Open', 'Close', 'Min', 'Max', 'Vol', 'Var']]
    #if df[['Vol']].sum(axis=0)[0] == 0: df = df.drop(columns=['Vol'])
    
    df = df.dropna()
    df.to_csv('stocks.csv')
    return df, poor_data