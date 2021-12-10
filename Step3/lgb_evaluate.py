import sklearn as sk
import numpy as np
import lightgbm as lgb
import time


window_size = 50
good_features = np.array([0,0,1,1,0,0,1,1,0]) == 1
THREADS = 8
TRIALS = 10
STEP_SIZE = 1 # Test to make sure the script works by setting this to be a high number like 60


X_days = []
y_days = []

for day in range(1,365):
    X = np.load('../data/grams/X/{}.npy'.format(day))
    X = np.concatenate([X[:1000],X[-1000:]],axis = 0)
    y = np.load('../data/grams/y/{}.npy'.format(day))
    y = np.concatenate([y[:1000],y[-1000:]],axis=0)
    X_days.append(X)
    y_days.append(y)

trial_y_pred = []
trial_y_test = []
fit_time = []
predict_time = []

for i in range(TRIALS):
    all_y_pred = []
    all_y_test = []
    window_start = 0
    param = {
        'objective': 'binary',
        'metric': 'binary_logloss',
        'device' : 'cpu',
        'reg_alpha': 4.359,
        "learning_rate": 0.2649,
        'reg_lambda': 8.9324,
        'num_leaves': 72,
        'colsample_bytree': 1.0,
        'subsample': 0.9012,
        'subsample_freq': 5,
        'min_child_samples': 50,
        "n_estimators": 247,
        "max_depth": 9,
        "min_split_gain": 0.0112,
    }
    while window_start + window_size < len(X_days):
        # Read in first ten X and y matrics
        X_window = X_days[window_start:window_start + window_size]
        y_window = y_days[window_start:window_start + window_size]

        # Stack them into one big X and y matrix
        X_train = np.concatenate(X_window,axis = 0)[:,good_features]
        y_train = np.concatenate(y_window,axis = 0)
        X_test = X_days[window_start + window_size][:,good_features]
        y_test = y_days[window_start + window_size ]

        # Train a model on X and y
        clf = lgb.LGBMClassifier(verbosity = -100,n_jobs = THREADS, **param)
        start = time.time()
        clf.fit(
            X_train,
            y_train)
        end = time.time()
        fit_time.append(end - start)

        # Predict on the eleventh day
        start = time.time()
        y_pred = clf.predict(X_test)
        end = time.time()
        predict_time.append(end - start)

        # Recond y_pred
        all_y_pred.append(y_pred)
        all_y_test.append(y_test)

        window_start += STEP_SIZE

    # Record precision,recall, accuracy and f1 score for all predicted values.
    all_y_pred = np.concatenate(all_y_pred,axis = 0)
    all_y_test = np.concatenate(all_y_test,axis = 0)
    trial_y_pred.append(all_y_pred)
    trial_y_test.append(all_y_test)


    print('Accuracy: ',(all_y_pred == all_y_test).sum() / all_y_pred.shape[0])
    print('Precision: ',sk.metrics.precision_score(all_y_test,all_y_pred))
    print('Recall: ',sk.metrics.recall_score(all_y_test,all_y_pred))
    print('F1 Score: ',sk.metrics.f1_score(all_y_test,all_y_pred))

trial_y_pred = np.stack(trial_y_pred,axis = 0)
trial_y_test = np.stack(trial_y_test,axis = 0)
fit_time = np.array(fit_time)
predict_time = np.array(predict_time)
np.save('lgb_results/trial_y_pred.npy',trial_y_pred)
np.save('lgb_results/trial_y_test.npy',trial_y_test)
np.save('lgb_results/fit_time.npy',fit_time)
np.save('lgb_results/predict_time.npy',predict_time)
