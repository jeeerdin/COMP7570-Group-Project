import numpy as np
from scipy import sparse as sp

tx_to_addr = sp.load_npz('../data/daily_graphs/months_1_to_12_btc_transactions_tx_to_addr.npz').astype('uint64')
addr_to_tx = sp.load_npz('../data/daily_graphs/months_1_to_12_btc_transactions_addr_to_tx.npz').astype('uint64').tocsc()

bad_addr = []

# loads in each persons linked transactions
judah = np.load('../data/grams/linked/judah_bad_tId.npy')[:,0]
jordan = np.load('../data/grams/linked/jordan_bad_tId.npy')[:,0]
abram = np.load('../data/grams/linked/abram_bad_tId.npy')[:,0]

# concatenates the data together
tId = np.concatenate([judah,jordan,abram])

# for each transaction appending its associated addresses to bad_addr
for t in tId:
    o = sp.find(tx_to_addr[t])
    i = sp.find(addr_to_tx[:,t])
    bad_addr.append(o[1])
    bad_addr.append(i[1])

# trimming the darknet addresses to be unique then saving it
bad_addr = np.unique(np.concatenate(bad_addr))
np.save('../data/grams/linked/bad_addr.npy',bad_addr)
