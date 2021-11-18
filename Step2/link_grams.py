import numpy as np
import os
from scipy import sparse as sp

days = os.listdir('../data/grams/parsed/')
tx_to_addr = sp.load_npz('../data/daily_graphs/months_1_to_12_btc_transactions_tx_to_addr.npz').tocsc()
dirty = {}

for day in days:
    # Load the grams data for that day
    
    prices = np.load('../data/grams/parsed/'+day)

    # Remove zero prices because they are not very unique
    prices = prices[prices != 0]
    
    num_missed = 0
    num_hit = 0

    # For the last 1000 prices in the grams data
    for p in prices[-1000:]:

        # Find all entries in the tx_to_addr matrix that matches that price
        find = tx_to_addr == p
        idx = find.indices
        num_found = len(idx)

        # For each transaction found
        for tId in idx:

            # Print it out
            print("tId = {} is a darknet transaction with confidence {}".format(tId,num_found**-1))
            
            # Append it to a list of all darknet transactions
            try:
                dirty[tId] += num_found**-1
            except:
                dirty[tId] = num_found**-1


print(dirty)

# Save all the darknet transaction ID to file
#np.save('../data/grams/linked/bad_tId.npy',np.array(dirty))
