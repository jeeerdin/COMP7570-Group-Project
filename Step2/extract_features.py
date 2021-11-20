import numpy as np
from scipy import sparse as sp

tx_to_addr = sp.load_npz('../data/daily_graphs/months_1_to_12_btc_transactions_tx_to_addr.npz').astype('uint64')
addr_to_tx = sp.load_npz('../data/daily_graphs/months_1_to_12_btc_transactions_addr_to_tx.npz').astype('uint64')

input_sum = addr_to_tx.sum(axis = 1).A[:,0]
output_sum = tx_to_addr.sum(axis = 0).A[0,:]

input_sum_sq = addr_to_tx.power(2).sum(axis = 1).A[:,0]
output_sum_sq = tx_to_addr.power(2).sum(axis = 0).A[0,:]

input_count = (addr_to_tx != 0).sum(axis = 1).A[:,0]
output_count = (tx_to_addr != 0).sum(axis = 0).A[0,:]

input_mean = input_sum/input_count
output_mean = np.nan_to_num(output_sum/output_count)

input_mean_sq = input_mean**2
output_mean_sq = output_mean**2

input_sq_mean = input_sum_sq/input_count
output_sq_mean = np.nan_to_num(output_sum_sq/output_count)

input_std = np.nan_to_num((input_sq_mean - input_mean_sq)**.5)
output_std = np.nan_to_num((output_sq_mean - output_mean_sq)**.5)

input_to_output_ratio = np.nan_to_num(input_count/output_count)

features = np.stack([input_sum,output_sum,input_count,output_count,input_mean,output_mean,input_std,output_std,input_to_output_ratio],axis = 1)

np.save('../data/grams/features.npy',features)
