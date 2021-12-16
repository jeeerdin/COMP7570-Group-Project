# Get a list of good addresses for each day
# Get as many good addresses as there are bad addresses.

import numpy as np
from scipy import sparse as sp
from calendar import monthrange

days_per_month = [0]
for i in range(1,12):
    days_per_month.append(monthrange(2015, i)[1])
days_per_month = np.cumsum(days_per_month)

# iterates through each month and day
for month in range(1,13):
  for day in range(1,monthrange(2015,month)[1]+1):

    # this is calculated like being the i'th day of the year, for example Feb. 9th is the 40th day of the year
    raw_day = days_per_month[month - 1] + day

    tx_to_addr = sp.load_npz('../data/daily_graphs/{}_{}_tx_to_addr.npz'.format(month,day)).astype('uint64').tocsr()
    addr_to_tx = sp.load_npz('../data/daily_graphs/{}_{}_addr_to_tx.npz'.format(month,day)).astype('uint64').tocsc()

    # load in this day's list of darknet addresses
    num_bad = np.load('../data/grams/linked/bad_addr/{}.npy'.format(raw_day)).shape[0]
    
    # getting inputs and outputs where the total will be equal to the number of darknets addresses we found
    i = tx_to_addr.indices
    np.random.shuffle(i)
    i = i[:num_bad//2]
    
    o = tx_to_addr.indices
    np.random.shuffle(o)
    o = o[:num_bad//2]

    # our list of good addresses will be the concatenation of both the inputs and outputs
    good_addr = np.concatenate([i,o])
    
    np.save('../data/grams/linked/good_addr/{}.npy'.format(raw_day),good_addr)
