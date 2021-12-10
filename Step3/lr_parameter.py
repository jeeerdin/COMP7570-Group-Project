import sklearn as sk
import numpy as np
from sklearn.linear_model import LogisticRegression
import optuna

THREADS = 12
good_features = np.array([0,0,1,1,0,0,1,1,0]) == 1


STEP_SIZE = 10
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
X_days,X_testing_days = X_days[:60],X_days[60:]
y_days,y_testing_days = y_days[:60],y_days[60:]

# 1. Define an objective function to be maximized.
def objective(trial):
 
    C = trial.suggest_float('C', 0, 100)
    l1_ratio = trial.suggest_float('l1_ratio', 0, 1)
    warm_start = trial.suggest_categorical('warm start', [False, True])

    window_size = trial.suggest_int('window_size',1,50)
    
    window_start = 0
    all_y_pred = []
    all_y_test = []

    # Train a model on X and y
    clf = LogisticRegression(n_jobs = THREADS,
                             penalty = 'elasticnet',
                             dual = False,
                             C = C,
                             max_iter = 1000,
                             warm_start = warm_start,
                             l1_ratio = l1_ratio,
                             solver = 'saga')
    while window_start + window_size < len(X_days):
        # Read in first ten X and y matrics
        X_window = X_days[window_start:window_start + window_size]
        y_window = y_days[window_start:window_start + window_size]

        # Stack them into one big X and y matrix
        X_train = np.concatenate(X_window,axis = 0)[:,good_features]
        y_train = np.concatenate(y_window,axis = 0)
        X_test = X_days[window_start + window_size][:,good_features]
        y_test = y_days[window_start + window_size]

        clf.fit(X_train,y_train)

        # Predict on the eleventh day
        y_pred = clf.predict(X_test)

        # Recond y_pred
        all_y_pred.append(y_pred)
        all_y_test.append(y_test)

        window_start += STEP_SIZE

    # Record precision,recall, accuracy and f1 score for all predicted values.
    all_y_pred = np.concatenate(all_y_pred,axis = 0)
    all_y_test = np.concatenate(all_y_test,axis = 0)


    f1 = sk.metrics.roc_auc_score(all_y_test,all_y_pred)
    print('Roc Auc: ', f1)

    return f1

# 3. Create a study object and optimize the objective function.
study = optuna.create_study(direction='maximize')
study.optimize(objective, n_trials=100)
