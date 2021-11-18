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

    # Remove non unique valuse
    prices,counts = np.unique(prices,return_counts = True)

    for i in range(1000,len(prices)):

        p = prices[i]
        count = counts[i]

        # Find all entries in the tx_to_addr matrix that matches that price
        find = tx_to_addr == p
        idx = find.indices
        num_found = len(idx)

        # For each transaction found
        for tId in idx:

            # Print it out
            print("tId = {} is a darknet transaction with confidence {}".format(tId,count*(num_found**-1)))
            
            # Append it to a list of all darknet transactions
            try:
                dirty[tId] += count*(num_found**-1)
            except:
                dirty[tId] = count*(num_found**-1)


print(dirty)

# Save all the darknet transaction ID to file
#np.save('../data/grams/linked/bad_tId.npy',np.array(dirty))
