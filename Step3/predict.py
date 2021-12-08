import sklearn as sk
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification

good_features = [0,0,1,1,0,0,1,1,0]
X = np.load('../data/grams/X.npy')[:,np.array(good_features) == 1]
y = np.load('../data/grams/y.npy')

idx = np.arange(X.shape[0])
np.random.shuffle(idx)

X = X[idx]
y = y[idx]

clf = RandomForestClassifier(max_depth=2, random_state=0)

X_train = X[:int(0.8*X.shape[0])]
y_train = y[:int(0.8*y.shape[0])]

X_test = X[int(0.8*X.shape[0]):]
y_test = y[int(0.8*y.shape[0]):]

clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)

print((y_pred == y_test).sum() / y_pred.shape[0])
print(sk.metrics.precision_score(y_test,y_pred))
print(sk.metrics.recall_score(y_test,y_pred))
print(sk.metrics.f1_score(y_test,y_pred))
