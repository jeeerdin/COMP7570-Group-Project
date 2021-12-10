import sklearn as sk
import numpy as np
import optuna
import lightgbm as lgb

THREADS = 8
good_features = np.array([0,0,1,1,0,0,1,1,0]) == 1


STEP_SIZE = 30
X_days = []
y_days = []

for day in range(1,365):
    X = np.load('../data/grams/X/{}.npy'.format(day))
    X = np.concatenate([X[:1000],X[-1000:]],axis = 0)
    y = np.load('../data/grams/y/{}.npy'.format(day))
    y = np.concatenate([y[:1000],y[-1000:]],axis=0)
    X_days.append(X)
    y_days.append(y)

# We shouldn't tune paramerters on the same data that we are testing on.
# We will leave the two months out
X_days,X_testing_days = X_days[:-60],X_days[-60:]
y_days,y_testing_days = y_days[:-60],y_days[-60:]

# 1. Define an objective function to be maximized.
def objective(trial):

    # 2. Suggest values for the hyperparameters using a trial object.
    window_size = trial.suggest_int('window_size',1,50)


    # 2. Suggest values of the hyperparameters using a trial object.
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

    window_start = 0
    all_y_pred = []
    all_y_test = []

    while window_start + window_size < len(X_days):
        # Read in first ten X and y matrics
        X_window = X_days[window_start:window_start + window_size]
        y_window = y_days[window_start:window_start + window_size]

        # Stack them into one big X and y matrix
        X_train = np.concatenate(X_window,axis = 0)[:,good_features]
        y_train = np.concatenate(y_window,axis = 0)
        X_test = X_days[window_start + window_size][:,good_features]
        y_test = y_days[window_start + window_size]

        clf = lgb.LGBMClassifier(verbosity = -100,n_jobs = THREADS, **param)
        clf.fit(
            X_train,
            y_train)


        # Predict on the eleventh day
        y_pred = clf.predict(X_test)

        # Recond y_pred
        all_y_pred.append(y_pred)
        all_y_test.append(y_test)

        window_start += STEP_SIZE

    # Record precision,recall, accuracy and f1 score for all predicted values.
    all_y_pred = np.concatenate(all_y_pred,axis = 0)
    all_y_test = np.concatenate(all_y_test,axis = 0)

    roc_auc = sk.metrics.roc_auc_score(all_y_test,all_y_pred)
    print('Roc Auc: ', roc_auc)
    print('f1: ', sk.metrics.f1_score(all_y_test,np.round(all_y_pred)))
    return roc_auc

# 3. Create a study object and optimize the objective function.
study = optuna.create_study(direction='maximize')
study.optimize(objective, n_trials=100)
