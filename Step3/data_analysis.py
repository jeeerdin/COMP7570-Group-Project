import numpy as np
import sklearn as sk
from sklearn import metrics as sk_metrics
import matplotlib.pyplot as plt
import scipy.stats as stats

'''
This script calculates the F1-Score and other metrics for each method, 
the ROC Curve and a bar plot showing the speed of each method
'''


# A list of each method acrynom and a dictionary giving their long name
methods = ['rf','lgb','lr']
long_name = {'rf':'Random Forest','lgb':'LGBM','lr':'Logistic Regression'}

# A dictionary giving the temporal window size of each method
window_size = {'rf':40,'lgb':50,'lr':27}

'''
First we read in the data from the method evaluations
'''

# A dictionary where we will store the predictions for each method
data = {}

# For each method, read its predictions, the ground truth, the training time and predicting time
for m in methods:
    
    # y_pred is a list of prediction made by the method
    # there are 2000 predictions for each day
    # resulting in (365 - window_size)*2000 predictions
    # We ran each method 10 times, so we have ten sets of such predictions
    y_pred = np.load('./{}_results/trial_y_pred.npy'.format(m))


    # y_test is the ground truth of y_pred
    y_test = np.load('./{}_results/trial_y_test.npy'.format(m))

    # fit time is a list of times that it took our methods to fit to the data
    # we divide by the window size to get fit time in milliseconds per sample
    fit_time = np.load('./{}_results/fit_time.npy'.format(m))/(window_size[m])
    
    # pred time is a list of times that it took our methods to make a prediction
    # the unit is in milliseconds per sample
    pred_time = np.load('./{}_results/predict_time.npy'.format(m))

    # We store this data in the data dictionary
    data[m] = {'y_pred':y_pred,'y_test':y_test,'fit_time':fit_time,'pred_time':pred_time}

'''
Then we generate a bar plot showing the average fit time 
and predict time of each method
'''

# Here we store the mean fit time for each method
fit_mean = []

# Here we store the standard deviation of the fit time for each method
fit_top_std = []
fit_bot_std = []

# Here we store the mean predict time for each method
pred_mean = []

# Here we store the standard deviation of the predict time for each method
pred_top_std = []
pred_bot_std = []

# We calculate the mean and std for each methods fit and predict time
for m in methods:
    
    # append the mean fit time
    fit_mean.append(np.mean(data[m]['fit_time']))
    
    # append the standard deviation of the fit time
    fit_top_std.append(np.std(data[m]['fit_time']))
    
    # If the mean - the standard deviation is negative
    # this would not look good when plotted
    # If this is the case, we replace it with zero
    if fit_mean[-1] - fit_top_std[-1] < 0:
        fit_bot_std.append(fit_mean[-1])
    else:
        fit_bot_std.append(fit_top_std[-1])
   
    
    # append the mean prediction time
    pred_mean.append(np.mean(data[m]['pred_time']))
    
    # append the standard deviation of the prediction time
    pred_top_std.append(np.std(data[m]['pred_time']))
    
    # If the mean - the standard deviation is negative
    # this would not look good when plotted
    # If this is the case, we replace it with zero
    if pred_mean[-1] - pred_top_std[-1] < 0:
        pred_bot_std.append(pred_mean[-1])
    else:
        pred_bot_std.append(pred_top_std[-1])

# Plot this data as a bar plot with the standard deviation shown as a black line
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

'''
Create the ROC curve of each method for the train and testing sets
'''

# prep the figure
plt.figure(0).clf()

# Plot the curve for each method on the training data set
# We evaluated each method ten times
# For the ROC curve, we just used the first trial
for m in methods:

    # Get the false positve and true positive for each threshold
    fpr, tpr, thresh = sk_metrics.roc_curve(data[m]['y_test'][0,:-60000], data[m]['y_pred'][0,:-60000])

    # Calculate the area under this curve
    auc = sk_metrics.roc_auc_score(data[m]['y_test'][0,:-60000], data[m]['y_pred'][0,:-60000])

    # Plot the curve and include the AUC in the legend
    plt.plot(fpr,tpr,label="{}, AUC=".format(long_name[m])+str(np.round(auc,4)))

# Label the axis and show the figure
plt.legend(loc=0)
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("Train Set ROC Curve")
plt.show()

# prep the figure
plt.figure(0).clf()

# Plot the curve for each method on the testing data set
# We evaluated each method ten times
# For the ROC curve, we just used the first trial
for m in methods:

    # Get the false positve and true positive for each threshold
    fpr, tpr, thresh = sk_metrics.roc_curve(data[m]['y_test'][0,-60000:], data[m]['y_pred'][0,-60000:])

    # Calculate the area under this curve
    auc = sk_metrics.roc_auc_score(data[m]['y_test'][0,-60000:], data[m]['y_pred'][0,-60000:])

    # Plot the curve and include the AUC in the legend
    plt.plot(fpr,tpr,label="{}, AUC=".format(long_name[m])+str(np.round(auc,4)))

# Label the axis and show the figure
plt.legend(loc=0)
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("Test Set ROC Curve")
plt.show()

'''
We now calculate and print the Precision, Recall, F1-Score, ROC-AUC and Accuracy
'''

# Store the train and test metrics for each method in a dictionary
train_metrics = {}
test_metrics = {}

# calculate the metrics for each method
for m in methods:

    # Initilze the metrics as an empty list
    # Because we have multiple trials
    # we need to record the metrics
    # for each trial
    train_metrics[m] = {'Precision':[],'Recall':[],'F1':[],'ROC-AUC':[],'Accuracy':[]}
    test_metrics[m] = {'Precision':[],'Recall':[],'F1':[],'ROC-AUC':[],'Accuracy':[]}

    # seperate the training and testing data
    y_pred_train = data[m]['y_pred'][:,:-60000]
    y_test_train = data[m]['y_test'][:,:-60000]
    
    y_pred_test = data[m]['y_pred'][:,-60000:]
    y_test_test = data[m]['y_test'][:,-60000:]

    # Calculate the metrics for each trial
    for i in range(10):

        # calculate pr curve and find the threshold that maximizez the f1-score
        precision, recall, thresholds = sk_metrics.precision_recall_curve(y_test_train[i], y_pred_train[i])
        fscore = (2 * precision * recall) / (precision + recall)
        ix = np.argmax(fscore)
        train_thresh = thresholds[ix]

        # Threshhold the predictions
        # note that the testing data uses the training data's threshold 
        y_pred_train_thresh = (y_pred_train[i] >= train_thresh).astype('int')
        y_pred_test_thresh = (y_pred_test[i] >= train_thresh).astype('int')
    
        # Calculate all the train metrics
        train_metrics[m]['Precision'].append(sk_metrics.precision_score(y_test_train[i],y_pred_train_thresh))
        train_metrics[m]['F1'].append(sk_metrics.f1_score(y_test_train[i],y_pred_train_thresh))
        train_metrics[m]['Recall'].append(sk_metrics.recall_score(y_test_train[i],y_pred_train_thresh))
        train_metrics[m]['Accuracy'].append(sk_metrics.accuracy_score(y_test_train[i],y_pred_train_thresh))
        train_metrics[m]['ROC-AUC'].append(sk_metrics.roc_auc_score(y_test_train[i],y_pred_train[i]))
        
        # Calculate all the test metrics
        test_metrics[m]['Precision'].append(sk_metrics.precision_score(y_test_test[i],y_pred_test_thresh))
        test_metrics[m]['F1'].append(sk_metrics.f1_score(y_test_test[i],y_pred_test_thresh))
        test_metrics[m]['Recall'].append(sk_metrics.recall_score(y_test_test[i],y_pred_test_thresh))
        test_metrics[m]['Accuracy'].append(sk_metrics.accuracy_score(y_test_test[i],y_pred_test_thresh))
        test_metrics[m]['ROC-AUC'].append(sk_metrics.roc_auc_score(y_test_test[i],y_pred_test[i]))

# A function that helps print metrics nicely
def print_metric(m,metric,train):
        
    # Get the metric from either the training data
    # or testing data
    if train:
        vals = train_metrics[m][metric]
    else:
        vals = test_metrics[m][metric]

    # calculate its mean and standard deviation
    # recall that we have ten trials
    mean = np.round(np.mean(vals),4)
    std = np.round(np.std(vals),4)

    # print this nicely
    print('{}:{}+-{}'.format(metric,mean,std))


# Print all the metrics for each method
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

'''
Calculate the statistical significance of the results
using the wilcoxen test
Particularily check if the random forest is higher then
the other methods
'''

# Calculate significance for each metric
for metric in ['Precision','Recall','Accuracy','ROC-AUC','F1']:
    
    test_groups = []
    train_groups = []
    
    # Get the train and test metrics for each method
    for m in methods:
        train_groups.append(train_metrics[m][metric])
        test_groups.append(test_metrics[m][metric])

    # Perform the wilcoxen test between the RF and LGBM and check if the 
    # p-value is less then 95%
    # This is done on the train data
    better_1 = stats.wilcoxon(train_groups[0], train_groups[1],alternative = 'greater')[1] < 0.05
    
    # Perform the wilcoxen test between the RF and LR and check if the 
    # p-value is less then 95%
    # This is done on the train data
    better_2 = stats.wilcoxon(train_groups[0], train_groups[2],alternative = 'greater')[1] < 0.05
    print("For {} The RF is better then the LGB on the train set: ".format(metric),better_1)
    print("For {} The RF is better then the LR on the train set: ".format(metric),better_2)
    
    # Perform the wilcoxen test between the RF and LGBM and check if the 
    # p-value is less then 95%
    # This is done on the test data
    better_1 = stats.wilcoxon(test_groups[0], test_groups[1],alternative = 'greater')[1] < 0.05
    
    # Perform the wilcoxen test between the RF and LR and check if the 
    # p-value is less then 95%
    # This is done on the test data
    better_2 = stats.wilcoxon(test_groups[0], test_groups[2],alternative = 'greater')[1] < 0.05
    print("For {} The RF is better then the LGB on the test set: ".format(metric),better_1)
    print("For {} The RF is better then the LR on the test set: ".format(metric),better_2)


