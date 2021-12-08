import numpy as np


features = np.load('../data/grams/features.npy')


for day in range(1,365):
    good_addr = np.load('../data/grams/linked/good_addr/{}.npy'.format(day))
    bad_addr = np.load('../data/grams/linked/bad_addr/{}.npy'.format(day))

    good_features = features[good_addr]
    bad_features = features[bad_addr]

    X = np.concatenate([good_features,bad_features],axis = 0)
    y = np.concatenate([np.zeros_like(good_addr),np.ones_like(bad_addr)],axis = 0)

    np.save('../data/grams/X/{}.npy'.format(day),X)
    np.save('../data/grams/y/{}.npy'.format(day),y)

