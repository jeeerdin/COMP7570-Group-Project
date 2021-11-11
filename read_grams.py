import numpy as np
import os
import pandas as pd
import json

folders = os.listdir('grams/')

csv = {}

for folder in folders:
    csv[folder] = os.listdir('grams/'+folder)

prices = {}

for folder in folders:
    markets = csv[folder]
    tx = []
    for m in markets:
        try:
            x = pd.read_csv('grams/{}/{}'.format(folder,m),on_bad_lines='warn')['price'].to_numpy()
            tx.append(x)
        except Exception:
            print('error in {} {}'.format(folder,m))

    if len(tx) == 0:
        pass
    price = np.concatenate(tx)
    
    month = str(int(folder[5:7]))
    day = str(int(folder[8:10]))
    mmdd = month + '_' + day

    prices[mmdd] = price

for mmdd in prices:
    arr = prices[mmdd]
    arr = arr*1e8
    arr = arr.astype('uint64')
    np.save('grams_parsed/'+mmdd,arr)
