import numpy as np
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt

#How many to show
NUM = 10000

features = np.load('../data/grams/features.npy')


bad_addr = np.load('../data/grams/linked/bad_addr.npy')
np.random.shuffle(bad_addr)
good_addr = np.load('../data/grams/linked/good_addr.npy')
np.random.shuffle(good_addr)

bad_addr = features[bad_addr]
bad_addr = bad_addr[bad_addr[:,2] != 0]
bad_addr = bad_addr[:NUM]

good_addr = features[good_addr]
good_addr = good_addr[good_addr[:,2] != 0]
good_addr = good_addr[:NUM]

features = np.concatenate([bad_addr,good_addr],axis = 0)
features = features - features.mean(axis = 0)
features = features/np.std(features,axis = 0)

emb = TSNE(verbose=2,n_jobs = 8,n_iter = 1000,init = 'pca').fit_transform(features)

plt.scatter(emb[:NUM,0],emb[:NUM,1],0.5,c = 'red')
plt.scatter(emb[NUM:,0],emb[NUM:,1],0.5,c = 'green')
plt.show()
