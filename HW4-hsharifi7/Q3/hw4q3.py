## Data and Visual Analytics - Homework 4
## Georgia Institute of Technology
## Applying ML algorithms to detect eye state

import numpy as np
import pandas as pd
import time

from sklearn.model_selection import cross_val_score, GridSearchCV, cross_validate, train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.svm import SVC
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, normalize
from sklearn.decomposition import PCA

######################################### Reading and Splitting the Data ###############################################
# XXX
# TODO: Read in all the data. Replace the 'xxx' with the path to the data set.
# XXX
data = pd.read_csv('eeg_dataset.csv')

# Separate out the x_data and y_data.
x_data = data.loc[:, data.columns != "y"]
y_data = data.loc[:, "y"]

# The random state to use while splitting the data.
random_state = 100

# XXX
# TODO: Split 70% of the data into training and 30% into test sets. Call them x_train, x_test, y_train and y_test.
# Use the train_test_split method in sklearn with the parameter 'shuffle' set to true and the 'random_state' set to 100.
# XXX
x_train, x_test, y_train, y_test = train_test_split(x_data, y_data, train_size=0.70, test_size=0.30, random_state=100, shuffle=True)

# ############################################### Linear Regression ###################################################
# XXX
# TODO: Create a LinearRegression classifier and train it.
# XXX
reg = LinearRegression().fit(x_train, y_train)
reg.score(x_train, y_train)
reg.coef_
reg.intercept_
y_predict_train = reg.predict(x_train)
y_predict_test = reg.predict(x_test)


# XXX
# TODO: Test its accuracy (on the training set) using the accuracy_score method.
# TODO: Test its accuracy (on the testing set) using the accuracy_score method.
# Note: Round the output values greater than or equal to 0.5 to 1 and those less than 0.5 to 0. You can use y_predict.round() or any other method.
# XXX
print(accuracy_score(y_train, y_predict_train.round()))
print(accuracy_score(y_test, y_predict_test.round()))

# ############################################### Random Forest Classifier ##############################################
# XXX
# TODO: Create a RandomForestClassifier and train it.
# XXX
clf = RandomForestClassifier(n_estimators=100, max_depth=2, random_state=0)
clf.fit(x_train, y_train)

y_predict_train = clf.predict(x_train)
y_predict_test = clf.predict(x_test)


# XXX
# TODO: Test its accuracy on the training set using the accuracy_score method.
# TODO: Test its accuracy on the test set using the accuracy_score method.
# XXX
print(accuracy_score(y_train, y_predict_train.round()))
print(accuracy_score(y_test, y_predict_test.round()))

# XXX
# TODO: Determine the feature importance as evaluated by the Random Forest Classifier.
#       Sort them in the descending order and print the feature numbers. The report the most important and the least important feature.
#       Mention the features with the exact names, e.g. X11, X1, etc.
#       Hint: There is a direct function available in sklearn to achieve this. Also checkout argsort() function in Python.
# XXX
importances = clf.feature_importances_
indices = np.argsort(importances)[::-1]
#for f in range(x_data.shape[1]):
#    print("%d. feature %s (%f)" % (f + 1, x_data.columns[indices[f]], importances[indices[f]]))

print("Most importan is %s. Least important is %s" % (x_data.columns[indices[0]], x_data.columns[indices[x_data.shape[1]-1]]))

# XXX
# TODO: Tune the hyper-parameters 'n_estimators' and 'max_depth'.
#       Print the best params, using .best_params_, and print the best score, using .best_score_.
# XXX
parameters = {'n_estimators':[100, 125, 150], 'max_depth':[2, 4, 6]}
clf = RandomForestClassifier(random_state=0)
gsCV = GridSearchCV(clf, parameters, cv=10)
gsCV.fit(x_train, y_train)
sorted(gsCV.cv_results_.keys())
print("best_params ", gsCV.best_params_)
print("best_score ", gsCV.best_score_)

# ############################################ Support Vector Machine ###################################################
# XXX
# TODO: Pre-process the data to standardize or normalize it, otherwise the grid search will take much longer
# TODO: Create a SVC classifier and train it.
# XXX
x_test_normalize = normalize(x_test)
x_train_normalize = normalize(x_train)

clf = SVC(gamma='auto')
clf.fit(x_train_normalize, y_train) 

y_predict_train = clf.predict(x_train_normalize)
y_predict_test = clf.predict(x_test_normalize)

# XXX
# TODO: Test its accuracy on the training set using the accuracy_score method.
# TODO: Test its accuracy on the test set using the accuracy_score method.
# XXX
print(accuracy_score(y_train, y_predict_train.round()))
print(accuracy_score(y_test, y_predict_test.round()))

# XXX
# TODO: Tune the hyper-parameters 'C' and 'kernel' (use rbf and linear).
#       Print the best params, using .best_params_, and print the best score, using .best_score_.
# XXX
x_data_normalize = normalize(x_data)

parameters = {'C':[0.0001, 0.001, 0.01], 'kernel':('linear', 'rbf')}
clf = SVC(gamma='auto')
gsCV = GridSearchCV(clf, parameters, return_train_score=True, cv=10)
gsCV.fit(x_data_normalize, y_data)
sorted(gsCV.cv_results_.keys())
print("best_params ", gsCV.best_params_)
print("best_score ", gsCV.best_score_)
print("Params ", gsCV.cv_results_["params"])
print("mean training score ", np.around(gsCV.cv_results_['mean_train_score'], 2))
print("mean testing score ", np.around(gsCV.cv_results_['mean_test_score'], 2))
print("mean fit time ", np.around(gsCV.cv_results_['mean_fit_time'], 2))


# ######################################### Principal Component Analysis #################################################
# XXX
# TODO: Perform dimensionality reduction of the data using PCA.
#       Set parameters n_component to 10 and svd_solver to 'full'. Keep other parameters at their default value.
#       Print the following arrays:
#       - Percentage of variance explained by each of the selected components
#       - The singular values corresponding to each of the selected components.
# XXX
pca = PCA(n_components=10, svd_solver='full')
pca.fit(x_train)

print(np.around(pca.explained_variance_ratio_, 2))
print(np.around(pca.singular_values_, 2)) 
