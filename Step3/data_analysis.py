import numpy as np
import sklearn as sk
from sklearn import metrics as sk_metrics
import matplotlib.pyplot as plt
import scipy.stats as stats


methods = ['rf','lgb','lr']
window_size = {'rf':40,'lgb':50,'lr':27}
long_name = {'rf':'Random Forest','lgb':'LGBM','lr':'Logistic Regression'}
data = {}

for m in methods:

    y_pred = np.load('./{}_results/trial_y_pred.npy'.format(m))
    y_test = np.load('./{}_results/trial_y_test.npy'.format(m))
    fit_time = np.load('./{}_results/fit_time.npy'.format(m))
    pred_time = np.load('./{}_results/predict_time.npy'.format(m))

    data[m] = {'y_pred':y_pred,'y_test':y_test,'fit_time':fit_time/(window_size[m]),'pred_time':pred_time}

# Time analysis
fit_mean = []
fit_top_std = []
fit_bot_std = []
pred_mean = []
pred_top_std = []
pred_bot_std = []
for m in methods:
    
    fit_mean.append(np.mean(data[m]['fit_time']))
    fit_top_std.append(np.std(data[m]['fit_time']))
    
    if fit_mean[-1] - fit_top_std[-1] < 0:
        fit_bot_std.append(fit_mean[-1])
    else:
        fit_bot_std.append(fit_top_std[-1])
    
    pred_mean.append(np.mean(data[m]['pred_time']))
    pred_top_std.append(np.std(data[m]['pred_time']))
    
    if pred_mean[-1] - pred_top_std[-1] < 0:
        pred_bot_std.append(pred_mean[-1])
    else:
        pred_bot_std.append(pred_top_std[-1])



plt.bar([1,2,3], fit_mean, 0.75, yerr=(fit_bot_std,fit_top_std), color = ['r','g','b'])
plt.bar([5,6,7],pred_mean, 0.75, yerr=(pred_bot_std,pred_top_std), color = ['r','g','b'])
plt.xticks([2,6],['Training Time','Predicting Time'])
plt.ylabel('Milliseconds per Sample')
colors = {'Random Forest':'red', 'LGBM':'green','Logistic Regression':'blue'}
labels = list(colors.keys())
handles = [plt.Rectangle((0,0),1,1, color=colors[label]) for label in labels]
plt.legend(handles, labels)
# show plot
plt.show()


plt.figure(0).clf()
# ROC-AUC curve
for m in methods:

    fpr, tpr, thresh = sk_metrics.roc_curve(data[m]['y_test'][0,:-60000], data[m]['y_pred'][0,:-60000])
    auc = sk_metrics.roc_auc_score(data[m]['y_test'][0,:-60000], data[m]['y_pred'][0,:-60000])
    plt.plot(fpr,tpr,label="{}, AUC=".format(long_name[m])+str(auc))

plt.legend(loc=0)
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("Train Set ROC Curve")

plt.show()

plt.figure(0).clf()
# ROC-AUC curve
for m in methods:

    fpr, tpr, thresh = sk_metrics.roc_curve(data[m]['y_test'][0,-60000:], data[m]['y_pred'][0,-60000:])
    auc = sk_metrics.roc_auc_score(data[m]['y_test'][0,-60000:], data[m]['y_pred'][0,-60000:])
    plt.plot(fpr,tpr,label="{}, AUC=".format(long_name[m])+str(auc))

plt.legend(loc=0)
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("Test Set ROC Curve")
plt.show()


# Metrics
train_metrics = {}
test_metrics = {}
for m in methods:

    train_metrics[m] = {'Precision':[],'Recall':[],'F1':[],'ROC-AUC':[],'Accuracy':[]}
    test_metrics[m] = {'Precision':[],'Recall':[],'F1':[],'ROC-AUC':[],'Accuracy':[]}

    y_pred_train = data[m]['y_pred'][:,:-60000]
    y_test_train = data[m]['y_test'][:,:-60000]
    
    y_pred_test = data[m]['y_pred'][:,-60000:]
    y_test_test = data[m]['y_test'][:,-60000:]

    for i in range(10):
        # calculate pr curve
        precision, recall, thresholds = sk_metrics.precision_recall_curve(y_test_train[i], y_pred_train[i])
        fscore = (2 * precision * recall) / (precision + recall)
        ix = np.argmax(fscore)
        train_thresh = thresholds[ix]
        print(train_thresh)

        y_pred_train_thresh = (y_pred_train[i] >= train_thresh).astype('int')
        y_pred_test_thresh = (y_pred_test[i] >= train_thresh).astype('int')
    

        train_metrics[m]['Precision'].append(sk_metrics.precision_score(y_test_train[i],y_pred_train_thresh))
        train_metrics[m]['F1'].append(sk_metrics.precision_score(y_test_train[i],y_pred_train_thresh))
        train_metrics[m]['Recall'].append(sk_metrics.precision_score(y_test_train[i],y_pred_train_thresh))
        train_metrics[m]['Accuracy'].append(sk_metrics.precision_score(y_test_train[i],y_pred_train_thresh))
        train_metrics[m]['ROC-AUC'].append(sk_metrics.roc_auc_score(y_test_train[i],y_pred_train[i]))
        
        test_metrics[m]['Precision'].append(sk_metrics.precision_score(y_test_test[i],y_pred_test_thresh))
        test_metrics[m]['F1'].append(sk_metrics.precision_score(y_test_test[i],y_pred_test_thresh))
        test_metrics[m]['Recall'].append(sk_metrics.precision_score(y_test_test[i],y_pred_test_thresh))
        test_metrics[m]['Accuracy'].append(sk_metrics.precision_score(y_test_test[i],y_pred_test_thresh))
        test_metrics[m]['ROC-AUC'].append(sk_metrics.roc_auc_score(y_test_test[i],y_pred_test[i]))

def print_metric(m,metric,train):
    
    if train:
        vals = train_metrics[m][metric]
    else:
        vals = test_metrics[m][metric]

    mean = np.round(np.mean(vals),4)
    std = np.round(np.std(vals),4)


    print('{}:{}+-{}'.format(metric,mean,std))


# Display the metrics
for m in methods:
    print()
    print(long_name[m])
    print('Training:')
    print_metric(m,'Precision',True)
    print_metric(m,'Recall',True)
    print_metric(m,'Accuracy',True)
    print_metric(m,'ROC-AUC',True)
    print_metric(m,'F1',True)
    print('Testing:')
    print_metric(m,'Precision',False)
    print_metric(m,'Recall',False)
    print_metric(m,'Accuracy',False)
    print_metric(m,'ROC-AUC',False)
    print_metric(m,'F1',False)

for metric in ['Precision','Recall','Accuracy','ROC-AUC','F1']:
    
    test_groups = []
    train_groups = []
    
    for m in methods:
        train_groups.append(train_metrics[m][metric])
        test_groups.append(test_metrics[m][metric])

    # Test if the RF is higher then all other methods
    better_1 = stats.wilcoxon(train_groups[0], train_groups[1])[1] < 0.05
    better_2 = stats.wilcoxon(train_groups[0], train_groups[2])[1] < 0.05
    print("For {} The RF is better then the LGB on the train set: ".format(metric),better_1)
    print("For {} The RF is better then the LR on the train set: ".format(metric),better_2)
    
    better_1 = stats.wilcoxon(test_groups[0], test_groups[1])[1] < 0.05
    better_2 = stats.wilcoxon(test_groups[0], test_groups[2])[1] < 0.05
    print("For {} The RF is better then the LGB on the test set: ".format(metric),better_1)
    print("For {} The RF is better then the LR on the test set: ".format(metric),better_2)


