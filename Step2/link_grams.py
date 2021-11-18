import numpy as np
import os
from scipy import sparse as sp
import threading

THREADS = 8

prices = np.load('../data/grams/parsed/judah.npy')
tx_to_addr = sp.load_npz('../data/daily_graphs/months_1_to_12_btc_transactions_tx_to_addr.npz').tocsc()

# Remove zero prices because they are not very unique
prices = prices[prices[:,0] != 0]

counts = prices[:,1]
prices = prices[:,0]

l = prices.shape[0]
indices = []
for i in range(THREADS):
    indices.append((i*l//THREADS,(i+1)*l//THREADS))

all_ = []

def search(start,end):
        global all_
#
        i = start
#
        dirty = []
        while len(dirty) <= 122000//THREADS//24//12 and i < end:
#
            p = prices[i]
            count = counts[i]
#
            # Find all entries in the tx_to_addr matrix that matches that price
            find = tx_to_addr == p
            idx = find.indices
            num_found = len(idx)
#
            # For each transaction found
            for tId in idx:
#
                # Print it out
#                print("tId = {} is a darknet transaction with confidence {}".format(tId,count*(num_found**-1)))
#            
                dirty.append((tId,count*(num_found**-1)))
#
            i+=1
        all_ = all_ + dirty


threads =[]
for idx in indices:
    t = threading.Thread(target = search, args = (idx[0],idx[1]))
    t.start()
    threads.append(t)

for t in threads:
    t.join()

print(all_)

# Save all the darknet transaction ID to file
np.save('../data/grams/linked/judah_bad_tId.npy',np.array(all_))
