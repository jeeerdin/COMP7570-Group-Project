import sklearn as sk
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
import time

THREADS = 8

good_features = np.array([1,1,1,1,0,1,1,1,1]) == 1

X_days = []
y_days = []

for day in range(1,365):
    X = np.load('../data/grams/X/{}.npy'.format(day))
    X = np.concatenate([X[:1000],X[-1000:]],axis = 0)
    y = np.load('../data/grams/y/{}.npy'.format(day))
    y = np.concatenate([y[:1000],y[-1000:]],axis=0)
    X_days.append(X)
    y_days.append(y)


# Train a model on X and y
clf = RandomForestClassifier(n_jobs = THREADS)
X = np.concatenate(X_days[:-60],axis = 0)[:,good_features].astype('float32')
y = np.concatenate(y_days[:-60],axis = 0)
clf.fit(X,y )


print(clf.feature_importances_)
