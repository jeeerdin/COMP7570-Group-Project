import numpy as np
from scipy import sparse as sp
import threading

THREADS = 8

prices = np.load('../data/grams/parsed/judah.npy')
tx_to_addr = sp.load_npz('../data/daily_graphs/months_1_to_12_btc_transactions_tx_to_addr.npz').tocsc()

# Remove zero prices because they are not very unique
prices = prices[prices[:,0] != 0]

# the number of darknet transactions with this amount
counts = prices[:,1]
# the amount
prices = prices[:,0]

# dividing the prices data into equal sections for each thread
l = prices.shape[0]
indices = []
for i in range(THREADS):
    indices.append((i*l//THREADS,(i+1)*l//THREADS))

all_ = []

# links darknet amounts to addresses from indices start to end
def search(start,end):
        global all_
#
        i = start
#
        # loops through the indices of the prices data until it reaches the end
        # will also stop if the number of linked addresses hits the goal of 122,000
        # This number was calculated by 1000 * 365 = 365,000 / 3 =  ~122,000
        dirty = []
        while len(dirty) <= 122000//THREADS and i < end:
#
            # gets the amount at this index and also the unmber of times this amount appeared in darknet data
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
                # calculates a confidence to assign to that addres being darknet
                # only addresses with a confidence >= 50% are included in the list of suspected darknet addresses
                if count*(num_found**-1) >= .5:
                    dirty.append((tId,count*(num_found**-1)))
#
            i+=1
        all_ = all_ + dirty

# for each thread they use their own equal sized disjoint sets of indices to run through
threads =[]
for idx in indices:
    t = threading.Thread(target = search, args = (idx[0],idx[1]))
    t.start()
    threads.append(t)

for t in threads:
    t.join()

# Save all the darknet transaction ID to file
np.save('../data/grams/linked/judah_bad_tId.npy',np.array(all_))
