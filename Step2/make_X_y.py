import numpy as np


features = np.load('../data/grams/features.npy')

TOTAL_DAYS = 365

for day in range(1, TOTAL_DAYS):
    good_addr = np.load('../data/grams/linked/good_addr/{}.npy'.format(day))
    bad_addr = np.load('../data/grams/linked/bad_addr/{}.npy'.format(day))

    # getting the list of features associated with our lists of good and bad addesses
    good_features = features[good_addr]
    bad_features = features[bad_addr]

    # concatenating the features lists for both good and bad into X
    X = np.concatenate([good_features,bad_features],axis = 0)
    
    # labelling each good address with a 0 and each darknet with a 1
    y = np.concatenate([np.zeros_like(good_addr),np.ones_like(bad_addr)],axis = 0)

    np.save('../data/grams/X/{}.npy'.format(day),X)
    np.save('../data/grams/y/{}.npy'.format(day),y)

