import numpy as np
import os
from scipy import sparse as sp

# The problem with this script right now is that we are finding very few
# (less then 10%) of the prices in the matrix.
# We would expect to find all of them
# Maybe there is a bug?

days = os.listdir('grams_parsed/')
tx_to_addr = sp.load_npz('daily_graphs/months_1_to_12_btc_transactions_tx_to_addr.npz')
dirty = []

for day in days:
    # Load the grams data for that day
    prices = np.load('grams_parsed/'+day)

    # Remove zero prices because they are not very unique
    prices = prices[prices != 0]
    
    # For each price in the grams data
    for p in prices:

        # Find all entries in the tx_to_addr matrix that matches that price
        find = tx_to_addr == p

        # If there is exactly one price that matches
        if len(find.data) == 1:

            # Find the transaction ID of that price
            tId = sp.find(find)[0][0]

            # Print it out
            print("tId = {} is a darknet transaction".format(tId))
            
            # Append it to a list of all darknet transactions
            dirty.append(tId)


# Save all the darknet transaction ID to file
np.save('bad_tId.npy',np.array(dirty))
