'''
This script runs a random forest on 
months 1-10, and calculates the feature importance
'''

import sklearn as sk
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
import time

THREADS = 8


'''
We read in each day's data
'''

X_days = []
y_days = []

# Loop through the days
for day in range(1,365):

    # load the feature matrix for that day
    X = np.load('../data/grams/X/{}.npy'.format(day))

    # Get the first 1000 darknet addresses and the first 1000 good addresses
    X = np.concatenate([X[:1000],X[-1000:]],axis = 0)

    # Do the same for the label vector
    y = np.load('../data/grams/y/{}.npy'.format(day))
    y = np.concatenate([y[:1000],y[-1000:]],axis=0)

    # Append these to the global list of data
    X_days.append(X)
    y_days.append(y)


# Create a random forest classifier
clf = RandomForestClassifier(n_jobs = THREADS)

# Concatenate the feature matrices from the first 305 days
X = np.concatenate(X_days[:-60],axis = 0)[:,good_features].astype('float32')

# Concatenate the labels from the first 305 days
y = np.concatenate(y_days[:-60],axis = 0)

# Fit the random forest
clf.fit(X,y )

# Print out how important each feature is
print(clf.feature_importances_)
