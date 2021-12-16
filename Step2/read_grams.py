import numpy as np
import os
import pandas as pd

# getting list of grams data folders
folders = os.listdir('../data/grams/raw/')

csv = {}

# places all csv market files in array, with lookup by day
# a search for csv['2015-05-03'] would return with list of markets ['BB.csv', 'OutLaw.csv', 'Agora.csv', 'Alpha.csv', 'NK.csv', 'ME.csv']
for folder in folders:
    csv[folder] = os.listdir('../data/grams/raw/'+folder)

prices = {}

for folder in folders:

    # gets a list of markets for this day
    markets = csv[folder]

    # a list to hold all the amounts for items on the darknet
    tx = []
    
    # iterating through each market
    for m in markets:
        try:
            # appending all the transaction amounts from each market to the list tx
            x = pd.read_csv('../data/grams/raw/{}/{}'.format(folder,m),on_bad_lines='warn')['price'].to_numpy()
            tx.append(x)
        except Exception:
            print('error in {} {}'.format(folder,m))
    
    # if there is are no markets from a day we continue onto the next day
    if len(tx) == 0:
        continue

    # concatenating lists from each market to make one list for all the amounts from the day
    price = np.concatenate(tx)
    
    # formatting the month and day
    month = str(int(folder[5:7]))
    day = str(int(folder[8:10]))
    mmdd = month + '_' + day

    # the prices dictionary at that date will point to the list of tx amounts
    prices[mmdd] = price

# fomatting the data and then storing it in a file for each day
for mmdd in prices:
    arr = prices[mmdd]
    arr = arr*1e8
    arr = arr.astype('uint64')
    np.save('../data/grams/parsed/'+mmdd,arr)
