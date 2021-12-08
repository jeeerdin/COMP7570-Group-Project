import sklearn as sk
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification

window_size = 10
window_start = 0
good_features = np.array([0,0,1,1,0,0,1,1,0]) == 1
THREADS = 8

X_days = []
all_y_pred = []
all_y_test = []
y_days = []

for day in range(1,365):
    X = np.load('../data/grams/X/{}.npy'.format(day))
    X = np.concatenate([X[:1000],X[-1000:]],axis = 0)
    y = np.load('../data/grams/y/{}.npy'.format(day))
    y = np.concatenate([y[:1000],y[-1000:]],axis=0)
    X_days.append(X)
    y_days.append(y)

while window_start + window_size <= 364:
    # Read in first ten X and y matrics
    X_window = X_days[window_start:window_start + window_size]
    y_window = y_days[window_start:window_start + window_size]

    # Stack them into one big X and y matrix
    X_train = np.concatenate(X_window,axis = 0)[:,good_features]
    y_train = np.concatenate(y_window,axis = 0)
    X_test = X_days[window_start + window_size + 10][:,good_features]
    y_test = y_days[window_start + window_size + 10]

    # Train a model on X and y
    clf = RandomForestClassifier(n_jobs = THREADS)
    #clf = sk.tree.DecisionTreeClassifier(max_depth = 3)
    clf.fit(X_train, y_train)
    #sk.tree.export_graphviz(clf,out_file='./tree.dot',
    #                        feature_names = ['Input Count','Output Count','Input Standard Deviation','Output Standard Deviation'],
    #                        class_names = ['Clean','Darknet'])

    # Predict on the eleventh day
    y_pred = clf.predict(X_test)

    # Recond y_pred
    all_y_pred.append(y_pred)
    all_y_test.append(y_test)

    print((y_pred == y_test).sum() / y_pred.shape[0])

    window_start += 1

# Record precision,recall, accuracy and f1 score for all predicted values.
all_y_pred = np.concatenate(all_y_pred,axis = 0)
all_y_test = np.concatenate(all_y_test,axis = 0)


print('Accuracy: ',(all_y_pred == all_y_test).sum() / all_y_pred.shape[0])
print('Precision: ',sk.metrics.precision_score(all_y_test,all_y_pred))
print('Recall: ',sk.metrics.recall_score(all_y_test,all_y_pred))
print('F1 Score: ',sk.metrics.f1_score(all_y_test,all_y_pred))

