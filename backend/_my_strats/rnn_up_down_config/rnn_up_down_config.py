# -*- coding: utf-8 -*-

import helpers as h
import os
import pandas as pd
from sklearn.preprocessing import StandardScaler
import numpy as np
import time
import tensorflow as tf
import keras
from keras import backend as k
from keras.models import Sequential
from keras.layers import Dense, Dropout, LSTM, LeakyReLU, CuDNNLSTM
from keras.callbacks import TensorBoard, ModelCheckpoint
from keras.utils import to_categorical
from sklearn.metrics import confusion_matrix
import preprocess
import json
import uuid
import matplotlib.pyplot as plt
import sys

config_id = sys.argv[1]
with open(f'config_{config_id}.json') as file:
	config_list = json.loads(file.read())
	# config_list representa uma lista composta por N conjuntos de parâmetros,
	# em que cada um dos conjuntos segue o esquema definido no cadastro do algoritmo

test = config_list[0]['is_test']
gpu = config_list[0]['use_gpu']
ticker_iterations = config_list[0]['ticker_iterations']
config_iterations = config_list[0]['config_iterations']

cfg_num_out = 2

LSTM_layer = CuDNNLSTM if gpu else LSTM

if gpu:
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

#tickers = ['PETR4','ITUB4','BOVA11','IVVB11','BOVV11','SMAL11','MALL11','XBOV11','BRAX11']
tickers = config_list[0]['tickers']

for tkr in tickers: # para cada ticker
    reset = True

    for tkr_i in range(ticker_iterations): # rode n vezes por ticker
    
        cfg_pred_offset = [3,5,10,15,20,25]
        cfg_prev_range = [5,10,25,50,75,100]
        cfg_sample_size = [1000,2000,3000]
        cfg_test_size = [0.1,0.15,0.2]
        cfg_epochs = [25,50,75,100]
        cfg_batchs = [10,25,50]
        cfg_nodes = [50,100,300]
        cfg_emas = [5,10,15,25,50,100,200]
        cfg_pocids = [1,5,10,50,200]
        cfg_macds = [[12,26],[50,200]]
        cfg_dropout = [0.2,0.5,0.75]
    
        cfgs = config_list

        for offset in cfgs[0]['pred_offset']:

            for c in cfgs: # para cada configuração (fará média com todas cfgs - ensemble)
                macds_config = list(c['macds'].values())

                date = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
                
                guid = uuid.uuid4()
                
                preds = []
                metrics = []
                durations = []
                
                for cfg_i in range(config_iterations): # faça n testes para essa configuração
                    
                    start = time.time()
                    
                    config = c.copy()
                    max_crop = max(config['emas'] + config['pocids'] + sum(macds_config, []) + config['rsis'])
                    if test: max_crop += offset
                    
                    #pd.read_csv('stocks.csv')
                    #preprocess.investing_csv(tkr, reset)
                    #preprocess.alpha_vantage_api(f"{tkr}.SAO", reset)
                    get_data = lambda tkr, reset: preprocess.yahoo_api(f"{tkr}.SA", reset)
                    get_data_fallback = lambda tkr, reset: preprocess.alpha_vantage_api(f"{tkr}.SAO", reset)
                    if reset:
                        df_init, poor_data = get_data(tkr, reset)
                        if poor_data:
                            df_init_fallback, poor_data_fallback = get_data_fallback(tkr, reset)
                            if not poor_data_fallback:
                                df_init = df_init_fallback.copy()
                    else:
                        df_init = get_data(tkr, reset)[0]
                    
                    if not config['full_data']:
                        df_init = df_init[['Date','Close','Vol','Var']]
                    
                    reset = False
                    
                    if (config['sample_size']+max_crop > len(df_init.index)):
                        print('*****resizing sample size*****')
                        config['sample_size'] = len(df_init.index) - max_crop
                        if config['sample_size'] < 250:
                            print('*****data size is too small*****')
                            break
                        
                    df_init = df_init.head(config['sample_size']+max_crop)
                    df_init = df_init.iloc[::-1]
                    pred_day = '-'.join(df_init.loc[df_init.index[-1], 'Date'].split('.'))
                    
                    # PREPROCESSING
                    
                    df_init['Date'] = list(map(h.cast_date, df_init['Date']))
                    df_init.set_index("Date", inplace=True)
                    
                    emas = []
                    for ema in config['emas']:
                        emas.append(df_init.loc[:, ['Close']].ewm(span=ema, adjust=False).mean().rename(columns={'Close':f'EMA {ema}'}))
                    df_init = pd.concat([df_init, *emas], axis=1)
                    
                    pocids = []
                    for pocid in config['pocids']:
                        pocids.append(pd.DataFrame(to_categorical(h.pocid_series(df_init['Close'].shift(pocid), df_init['Close'])), columns=[f'Down {pocid}',f'Up {pocid}']).set_index(df_init.index))
                        #df_init[f'POCID {pocid}'] = h.pocid_series(df_init['Close'].shift(pocid), df_init['Close'])
                    df_init = pd.concat([df_init, *pocids], axis=1)
                        
                    for macd in macds_config:
                        df_init[f'MACD {macd[0]}-{macd[1]}'] = h.macd_series(df_init['Close'], macd[0], macd[1])
                    
                    for rsi in config['rsis']:
                        df_init[f'RSI {rsi}'] = h.rsi_series(df_init['Close'], rsi)
                    
                    df_pocid_future = pd.DataFrame(to_categorical(h.pocid_series(df_init['Close'], df_init['Close'].shift(-offset))), columns=[f'Down Future {config["pred_offset"]}',f'Up Future {config["pred_offset"]}'])
                    df_init = pd.concat([df_pocid_future.set_index(df_init.index), df_init], axis=1)
                    
                    df = df_init.copy()                
                    
                    df = df[:-offset]
                    df = df[max_crop-offset:]
                    
                    pred_data = {
                        'pocid': float(df.loc[df.index[-1], f'Up Future {config["pred_offset"]}']) if test else float('nan'),
                        'close': float(df_init.loc[df_init.index[-1], 'Close'])
                    }
                    
                    # Scale
                    
                    df.dropna(inplace=True)                
                    
                    x, y = h.create_timeseries(df, config['prev_range'], cfg_num_out)
                    
                    test_size = round(len(x)*config['test_size'])
                    x_test = x[:test_size].copy()
                    y_test = y[:test_size].copy()
                    x_train = x[test_size:].copy()
                    y_train = y[test_size:].copy()
            
                    scalers = {}
                    for i in range(x_train.shape[2]):
                        scalers[i] = StandardScaler()
                        x_train[:, :, i] = scalers[i].fit_transform(x_train[:, :, i])
            
                    for i in range(x_test.shape[2]):
                        x_test[:, :, i] = scalers[i].transform(x_test[:, :, i])
                        
                    # MODEL
                    
                    model = Sequential()
                    
                    if config['extra_layers'] == 0:
                        model.add(LSTM_layer(config['nodes'], input_shape=(x_train.shape[1:]))) # usar return_sequences=True caso o próximo layer seja LSTM
                    else:
                        model.add(LSTM_layer(config['nodes'], input_shape=(x_train.shape[1:]), return_sequences=True))
                    if not gpu:
                        model.add(LeakyReLU(alpha=0.05))
                    model.add(Dropout(config['dropout']))
                
                    for i in range(config['extra_layers']):
                        if i == config['extra_layers'] - 1:
                            model.add(LSTM_layer(config['nodes'], input_shape=(x_train.shape[1:])))
                        else:
                            model.add(LSTM_layer(config['nodes'], input_shape=(x_train.shape[1:]), return_sequences=True))
                        if not gpu:
                            model.add(LeakyReLU(alpha=0.05))
                        model.add(Dropout(config['dropout']))
            
                    model.add(Dense(cfg_num_out, activation='softmax'))
                    
                    opt = keras.optimizers.Adam(lr=1e-3, decay=1e-6)
                    
                    model.compile(loss='categorical_crossentropy',
                                optimizer=opt,
                                metrics=['accuracy'])
                    
                    #h.mkdir_conditional('logs')
                    h.mkdir_conditional('models')
                    #tensorboard = TensorBoard(log_dir=f'logs/log_{tkr}_{guid}_{cfg_i}')
                    checkpoint = ModelCheckpoint(filepath=f'models/weights_{guid}.hdf5', verbose=0, save_best_only=True)
                    
                    hist = model.fit(
                            x_train, y_train,
                            batch_size=config['batchs'],
                            epochs=config['epochs'],
                            validation_data=(x_test, y_test),
                            callbacks=[checkpoint],#, tensorboard],
                            verbose=0
                            )
                    
                    # Get Best
                    model.load_weights(f'models/weights_{guid}.hdf5')
                    os.remove(f'models/weights_{guid}.hdf5')
                    
                    # PRED
                    
                    # y_result = model.predict(x_test)
                    
                    # cm = confusion_matrix(y_test.argmax(axis=1), y_result.argmax(axis=1))
                    # acc = (cm[0][0] + cm[1][1]) / np.sum(cm)  
                    
                    # df_result = pd.DataFrame({'Test': y_test[:, 1], 'Result': np.round(y_result[:, 1]), 'Result Raw': y_result[:, 1]})
                    # df_result['Error'] = df_result.apply(lambda row: abs(row['Result Raw'] - 0.5) if row['Test'] != row['Result'] else None, axis=1)
                    # df_result[['Normalized Error']] = df_result[['Error']].apply(lambda x: x/x.max())
                    # df_result_wrong = df_result.loc[df_result['Test'] != df_result['Result']]
                    # mean_error = df_result_wrong['Error'].sum() / len(df_result_wrong.index) if len(df_result_wrong.index) != 0 else 0
                    #plt.plot(y_result[:, 1])
                    #plt.show()              
                    
                    if test: df_pred_next = df_init[-(config['prev_range']+offset):].drop(df_init.tail(offset).index).copy()
                    else: df_pred_next = df_init[-(config['prev_range']):].copy() # utiliza até ultimo dia para prever dia + pred_offset
                    #else: df_pred_next = df_init[-(config['prev_range']+offset-1):].drop(df_init.tail(offset-1).index).copy() # sempre tenta prever dia + 1
                    x_pred_next, y_pred_next = h.create_timeseries(df_pred_next, config['prev_range'], cfg_num_out, False)
                    for i in range(x_pred_next.shape[2]):
                        x_pred_next[:, :, i] = scalers[i].transform(x_pred_next[:, :, i])
                    
                    y_result_next = model.predict(x_pred_next)
                    print(y_result_next)
                    print(pred_data['pocid'])
                    
                    # REPORT
                    
                    preds.append(y_result_next[0][1])
                    best_index = hist.history["val_loss"].index(min(hist.history["val_loss"]))
                    metrics.append({
                        'valloss': float(round(hist.history["val_loss"][best_index],5)),
                        'loss': float(round(hist.history["loss"][best_index],5)),
                        'valacc': float(round(hist.history["val_acc"][best_index],5)),
                        'acc': float(round(hist.history["acc"][best_index],5)),
                    })
                    
                    keras.backend.clear_session()
                    
                    print('\n','-'*10)
                    print('#',tkr,tkr_i,cfg_i)
                    duration = time.time() - start
                    print(f'Duration: {duration}')
                    durations.append(duration)
                    print('Mean duration:',sum(durations)/len(durations))
                    print('-'*10,'\n')
            
            if (len(preds) > 0):
                avg_preds = float(np.mean(preds))
                std_preds = float(np.std(preds))
                avg_loss = np.mean([x['valloss'] for x in metrics])
                avg_acc = np.mean([x['valacc'] for x in metrics])

                result_id = str(uuid.uuid4())
                with open(f'result_{result_id}.json', 'w') as file:
                    result = {
                        "id": result_id,			# id do resultado
                        "config": cfgs,			# configurações utilizadas pelo algoritmo
                        "result": {				# resultados do algoritmo, composto por "real", "pred" e "metrics"
                            "real": [pred_data['pocid']],		# array com os valores reais (Ex.: para um algoritmo que prevê a abertura do dia seguinte, na lista pode constar o preço real da abertura, para comparação)
                            "pred": [avg_preds],		# array com os valores da previsão
                            "metrics": {			# campo livre para salvar as métricas do algoritmo (Ex. MAE, MAPE, Accuracy...)
                                'ticker': tkr,
                                'offset': offset,
                                'poor_data': poor_data,
                                'raw': metrics,
                                'avg_loss': avg_loss,
                                'avg_acc': avg_acc,
                                'pred_std': [std_preds],
                                'close_reference': pred_data['close']
                            }
                        }
                    }
                    print(json.dumps(result))
                    file.write(json.dumps(result))