import numpy as np
import os
from scipy import sparse as sp

days = os.listdir('grams_parsed/')
tx_to_addr = sp.load_npz('daily_graphs/months_1_to_12_btc_transactions_tx_to_addr.npz')
dirty = []

for day in days:
    prices = np.load('grams_parsed/'+day)
    prices = prices[prices != 0]
    found = np.zeros_like(prices)
    
    for p in prices:
        find = tx_to_addr == p
        if len(find.data) == 1:
            tId = sp.find(find)[0][0]
            print("tId = {} is a darknet transaction".format(tId))
            dirty.append(tId)


np.save('bad_tId.npy',np.array(dirty))
