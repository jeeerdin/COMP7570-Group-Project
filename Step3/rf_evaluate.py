'''
This script uses the optimal hyper-parameters
discovered by optuna and trains a random forest to
make prediction on both the test and train data
'''
import sklearn as sk
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
import time

THREADS = 8

window_size = 40

# Run the model ten seperate times for ropustness
TRIALS = 10

# We only use the features that had more then 10% feature importance
good_features = np.array([0,0,1,1,0,0,1,1,0]) == 1

STEP_SIZE = 1 

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


# Keep a global record of the predictions,
# ground truth, time to fit and time to predict
trial_y_pred = []
trial_y_test = []
fit_time = []
predict_time = []

# Repeat the experiment 10 times
for i in range(TRIALS):

    # Keep a record of the predictions
    # and ground truth
    all_y_pred = []
    all_y_test = []

    # Start the window at day zero
    window_start = 0

    # Continue until we are out of data
    while window_start + window_size < len(X_days):

        # Get all the days in the window
        X_window = X_days[window_start:window_start + window_size]
        y_window = y_days[window_start:window_start + window_size]

        # Stack them into one big X and y matrix
        X_train = np.concatenate(X_window,axis = 0)[:,good_features]
        y_train = np.concatenate(y_window,axis = 0)
        
        # Get the testing day
        X_test = X_days[window_start + window_size][:,good_features]
        y_test = y_days[window_start + window_size ]

        # Create a random forest classifier
        clf = RandomForestClassifier(n_jobs = THREADS,
                                     criterion = 'entropy',
                                     bootstrap = False,
                                     max_features = 'auto',
                                     min_samples_split = 14,
                                     min_samples_leaf = 2,
                                     max_depth = 86,
                                     n_estimators = 111)

        # Fit the random forest and keep track of how long
        # it takes
        start = time.time()
        clf.fit(X_train, y_train)
        end = time.time()
        fit_time.append(end - start)

        # Predict on the testing day
        # and keep track of how long it takes
        start = time.time()
        y_pred = clf.predict(X_test)
        end = time.time()
        predict_time.append(end - start)

        # Record the predictions and ground truth
        all_y_pred.append(y_pred)
        all_y_test.append(y_test)

        # Shift the window over by one
        window_start += STEP_SIZE


# Write the results to disk to be analyized in another script
trial_y_pred = np.stack(trial_y_pred,axis = 0)
trial_y_test = np.stack(trial_y_test,axis = 0)
fit_time = np.array(fit_time)
predict_time = np.array(predict_time)
np.save('rf_results/trial_y_pred.npy',trial_y_pred)
np.save('rf_results/trial_y_test.npy',trial_y_test)
np.save('rf_results/fit_time.npy',fit_time)
np.save('rf_results/predict_time.npy',predict_time)
