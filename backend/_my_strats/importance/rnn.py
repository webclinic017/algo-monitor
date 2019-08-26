# -*- coding: utf-8 -*-

import helpers as h
import os
import pandas as pd
from sklearn.preprocessing import StandardScaler
import numpy as np
import tensorflow as tf
import keras
from keras import backend as k
from keras.models import Sequential
from keras.layers import Dense, Dropout, LSTM, LeakyReLU, CuDNNLSTM
from keras.callbacks import TensorBoard, ModelCheckpoint
from keras.utils import to_categorical
from sklearn.metrics import confusion_matrix
import preprocess
import matplotlib.pyplot as plt

###################################
# TensorFlow wizardry
config = tf.ConfigProto()

# Don't pre-allocate memory; allocate as-needed
config.gpu_options.allow_growth = True

# Only allow a total of half the GPU memory to be allocated
config.gpu_options.per_process_gpu_memory_fraction = 0.75

# Create a session with the above options specified.
k.tensorflow_backend.set_session(tf.Session(config=config))
###################################

get_data = lambda tkr, reset: preprocess.yahoo_api(f"{tkr}.SA", reset)
df_init = get_data('BOVA11', True)[0]
df_init = df_init.head(2000)
df_init = df_init.iloc[::-1]

# PREPROCESSING

df_init['Date'] = list(map(h.cast_date, df_init['Date']))
df_init.set_index("Date", inplace=True)

# Close
#df_init.insert(0, f'Close {config["pred_offset"]}', df_init['Close'].shift(-offset))
# Min Max
#df_init.insert(0, f'Max {config["pred_offset"]}', df_init['Max'].shift(-offset))
#df_init.insert(0, f'Min {config["pred_offset"]}', df_init['Min'].shift(-offset))
# Pocid
df_pocid_future = pd.DataFrame(to_categorical(h.pocid_series(df_init['Close'], df_init['Close'].shift(-5))), columns=[f'Down Future {5}',f'Up Future {5}'])
df_init = pd.concat([df_pocid_future.set_index(df_init.index), df_init], axis=1)

cfg_outputs = 2
cfg_range = 75
cfg_nodes = 100
cfg_batch = 50
cfg_epoch = 75

accs = []

for i in range(10):
    
    accs.append([])
    
    for c in range(len(df_init.columns) - cfg_outputs + 4 + 1):
        
        df = df_init.copy()
            
        if c != len(df_init.columns) - cfg_outputs:
            emas = []
            for ema in [15, 25, 50, 200]:
                emas.append(df.loc[:, ['Close']].ewm(span=ema, adjust=False).mean().rename(columns={'Close':f'EMA {ema}'}))
            df = pd.concat([df, *emas], axis=1)
        
        if c != len(df_init.columns) + 1 - cfg_outputs:
            pocids = []
            for pocid in [1, 5, 50, 200]:
                pocids.append(pd.DataFrame(to_categorical(h.pocid_series(df['Close'].shift(pocid), df['Close'])), columns=[f'Down {pocid}',f'Up {pocid}']).set_index(df.index))
            df = pd.concat([df, *pocids], axis=1)
        
        if c != len(df_init.columns) + 2 - cfg_outputs:
            for macd in [[12, 26],[50, 200]]:
                df[f'MACD {macd[0]}-{macd[1]}'] = h.macd_series(df['Close'], macd[0], macd[1])
        
        if c != len(df_init.columns) + 3 - cfg_outputs:
            for rsi in [14]:
                df[f'RSI {rsi}'] = h.rsi_series(df['Close'], rsi)
        
        if c < len(df_init.columns) - cfg_outputs:
            df = df.drop(df_init.columns[c+cfg_outputs], axis=1)
        
        df.dropna(inplace=True)
        
        x, y = h.create_timeseries(df, cfg_range, cfg_outputs)
        
        test_size = round(len(x)*0.2)
        x_test = x[:test_size].copy()
        y_test = y[:test_size].copy()
        x_train = x[test_size:].copy()
        y_train = y[test_size:].copy()
        
        scalers = {}
        for c in range(x_train.shape[2]):
            scalers[c] = StandardScaler()
            x_train[:, :, c] = scalers[c].fit_transform(x_train[:, :, c])
        
        for c in range(x_test.shape[2]):
            x_test[:, :, c] = scalers[c].transform(x_test[:, :, c])
            
        # MODEL
        
        model = Sequential()
        
        model.add(CuDNNLSTM(cfg_nodes, input_shape=(x_train.shape[1:]), return_sequences=True))
        model.add(Dropout(0.2))
        model.add(CuDNNLSTM(cfg_nodes, input_shape=(x_train.shape[1:])))
        model.add(Dropout(0.2))
        model.add(Dense(cfg_outputs, activation='softmax'))
        
        opt = keras.optimizers.Adam(lr=1e-3, decay=1e-6)
        
        model.compile(loss='categorical_crossentropy',
                    optimizer=opt,
                    metrics=['accuracy'])
        
        hist = model.fit(
            x_train, y_train,
            batch_size=cfg_batch,
            epochs=cfg_epoch,
            validation_data=(x_test, y_test),
            verbose=1
        )
        
        index = hist.history["val_loss"].index(min(hist.history["val_loss"]))
        acc = float(round(hist.history["val_acc"][index],5))
        print('Acc: ',acc)
        accs[i].append(acc)
        
        keras.backend.clear_session()

accs = np.array(accs)
accs_mean = np.mean(accs, axis=0)
accs_std = np.std(accs, axis=0)

# n, emas, pocid, macd, rsi, full