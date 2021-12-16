# Change the bad transaction Id's to a list of bad transactions.

import numpy as np
from scipy import sparse as sp

tx_to_addr = sp.load_npz('../data/daily_graphs/months_1_to_12_btc_transactions_tx_to_addr.npz').astype('uint64')
addr_to_tx = sp.load_npz('../data/daily_graphs/months_1_to_12_btc_transactions_addr_to_tx.npz').astype('uint64').tocsc()

# iterating through each day
for day in range(365):
    
    # getting darknet transaction Id's
    tId = np.load('../data/grams/linked/daily_bad_tId/{}.npy'.format(day))
    
    bad_addr = []
    for t in tId:
        # getting inputs and outputs from this transaction and appending them to list of darknet addresses
        o = sp.find(tx_to_addr[t])
        i = sp.find(addr_to_tx[:,t])
        bad_addr.append(o[1])
        bad_addr.append(i[1])
    
    if len(bad_addr) > 0:
        bad_addr = np.unique(np.concatenate(bad_addr))
        np.save('../data/grams/linked/bad_addr/{}.npy'.format(day),bad_addr)
