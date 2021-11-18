import numpy as np
import os
from scipy import sparse as sp

# The problem with this script right now is that we are finding very few
# (less then 10%) of the prices in the matrix.
# We would expect to find all of them
# Maybe there is a bug?

days = os.listdir('../data/grams/parsed/')
tx_to_addr = sp.load_npz('../data/daily_graphs/months_1_to_12_btc_transactions_tx_to_addr.npz').tocsc()
dirty = {}

def days_in_month(month):
    if month in {1, 3, 5, 7, 8, 10, 12}:
        return 31
    if month == 2:
        return 28
    return 30

def decrement_day(day,month):
    month_min = month == 1

    day_min = day == 1

    if day_min:
        if not month_min:
            prev_month = month - 1
            prev_day = days_in_month(prev_month)
        else:
            return -1,-1
    else:
        prev_month = month
        prev_day = day - 1

    return prev_day,prev_month

def increment_day(day,month):
    month_max = month == 12
    
    day_max = day == days_in_month(month)

    if day_max:
        if not month_max:
            next_month = month + 1
            next_day = 1
        else:
            return -1,-1
    else:
        next_month = month
        next_day = day + 1

    return next_day,next_month

def get_days(day):
    ret = []
    
    day = day[:-4]
    
    month,day = day.split('_')
    
    day = int(day)
    month = int(day)
    
    ret.append('{}_{}'.format(month,day)) 
    
    NUM = 0

    prev_day = day
    prev_month = month
    for i in range(NUM):
        prev_day,prev_month = decrement_day(prev_day,prev_month)
        if prev_day != -1:
            ret.append('{}_{}'.format(prev_month,prev_day))
        else:
            pass
    
    next_day = day
    next_month = month
    for i in range(NUM):
        next_day,next_month = increment_day(next_day,next_month)
        if next_day != -1:
            ret.append('{}_{}'.format(next_month,next_day))
        else:
            pass

    return ret

for day in days:
    # Load the grams data for that day
    
    prices = np.load('grams_parsed/'+day)

    # Remove zero prices because they are not very unique
    prices = prices[prices != 0]
    
#    num_missed = 0
#    num_hit = 0
    # For each price in the grams data
    total = len(prices)
    curr = 0
    for p in prices:
        curr +=1
        print(curr/total)

        # Find all entries in the tx_to_addr matrix that matches that price
        find = tx_to_addr == p
        idx = find.indices
        num_found = len(idx)

#        if num_found == 0:
#            num_missed+=1
#        else:
#            num_hit+=1
#            confidence = num_found**-1

#        print("Ratio: {}".format(num_hit/(num_missed+num_hit)))
        # For each transaction found
        for tId in idx:

            # Print it out
            #print("tId = {} is a darknet transaction with confidence {}".format(tId,confidence))
            
            # Append it to a list of all darknet transactions
            try:
                dirty[tId] += num_found**-1
            except:
                dirty[tId] = num_found**-1


print(dirty)

# Save all the darknet transaction ID to file
#np.save('../data/grams/linked/bad_tId.npy',np.array(dirty))
