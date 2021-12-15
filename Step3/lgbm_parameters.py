'''
This script finds the optimal hyperparameters for the lgbm model
using the optuna optimiziation library
'''
import sklearn as sk
import numpy as np
import optuna
import lightgbm as lgb

THREADS = 8

# We only use the features that had more then 10% feature importance
good_features = np.array([0,0,1,1,0,0,1,1,0]) == 1

# Typically, we will shift the temporal window by 1 day
# for speed, we increase this to ten
# this will result in some data lost but it
# is worth it for the speed increase
STEP_SIZE = 10

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

# We shouldn't tune paramerters on the same data that we are testing on.
# We will leave the two months out
X_days,X_testing_days = X_days[:-60],X_days[-60:]
y_days,y_testing_days = y_days[:-60],y_days[-60:]

# According to optuna's documentation
# we define an objective function to be maximized.
def objective(trial):

    # Use optuna to select a range for the hyperparameters
    window_size = trial.suggest_int('window_size',1,50)
    param = {
        'objective': 'binary',
        'metric': 'binary_logloss',
        'device' : 'cpu',
        'reg_alpha': trial.suggest_float('reg_alpha', 1e-8, 10.0),
        "learning_rate": trial.suggest_float("learning_rate", 0.01, 0.3),
        'reg_lambda': trial.suggest_float('reg_lambda', 1e-8, 10.0),
        'num_leaves': trial.suggest_int('num_leaves', 2, 256),
        'colsample_bytree': trial.suggest_categorical('colsample_bytree', [0.25,0.5,0.75, 1.0]),
        'subsample': trial.suggest_float('subsample', 0.25,1.0),
        'subsample_freq': trial.suggest_int('subsample_freq', 0, 7),
        'min_child_samples': trial.suggest_int('min_child_samples', 5, 100),
        "n_estimators": trial.suggest_int("n_estimators",2,1000),
        "max_depth": trial.suggest_int("max_depth", 2, 12)*trial.suggest_categorical("no_depth",[-1,1]),
        "min_split_gain": trial.suggest_float("min_split_gain", 0, 15),
    }

    # start the window at day zero
    window_start = 0

    # Keep a recond of the predictions and their ground truth
    all_y_pred = []
    all_y_test = []

    # Loop untill we run out of days
    while window_start + window_size < len(X_days):

        # Get all the days in the window
        X_window = X_days[window_start:window_start + window_size]
        y_window = y_days[window_start:window_start + window_size]

        # Stack them into one big X and y matrix
        X_train = np.concatenate(X_window,axis = 0)[:,good_features]
        y_train = np.concatenate(y_window,axis = 0)

        # Get the testing day
        X_test = X_days[window_start + window_size][:,good_features]
        y_test = y_days[window_start + window_size]

        # Fit a LGBM classifier
        clf = lgb.LGBMClassifier(verbosity = -100,n_jobs = THREADS, **param)
        clf.fit(
            X_train,
            y_train)


        # Predict on the test day
        y_pred = clf.predict(X_test)

        # Record y_pred
        all_y_pred.append(y_pred)
        all_y_test.append(y_test)

        # Shift the window
        window_start += STEP_SIZE

    # Record ROC AUC for all predicted values.
    all_y_pred = np.concatenate(all_y_pred,axis = 0)
    all_y_test = np.concatenate(all_y_test,axis = 0)
    roc_auc = sk.metrics.roc_auc_score(all_y_test,all_y_pred)
    
    # Print and return this value
    # Optuna will try to optimize this
    print('Roc Auc: ', roc_auc)
    return roc_auc

# Execute optuna to maximize the ROC-AUC over 100 trials
study = optuna.create_study(direction='maximize')
study.optimize(objective, n_trials=100)
