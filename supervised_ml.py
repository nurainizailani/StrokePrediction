#import packages and libraries
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn import linear_model, tree, svm
from sklearn.metrics import (mean_squared_error, r2_score, explained_variance_score, mean_absolute_error,
                             root_mean_squared_error, accuracy_score, auc, confusion_matrix, f1_score, precision_score,
                             recall_score)
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn import svm
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor

class RunRegressionModels:
    def __init__(self, X, y, X_new, y_true):
        self.train_metrics_all = {}
        self.test_metrics_all = {}
        self.train_df = pd.DataFrame(X)
        self.test_df = pd.DataFrame(X_new)
        self.train_df['actual'] = y
        self.test_df['actual'] = y_true
        self.X = X
        self.y = y
        self.X_new = X_new
        self.y_true = y_true

    def regression_metrics(self, y_true, y_pred):
        metrics = {}
        metrics['r2'] = r2_score(y_true, y_pred)
        metrics['evs'] = explained_variance_score(y_true, y_pred)
        metrics['mae'] = mean_absolute_error(y_true, y_pred)
        metrics['mse'] = mean_squared_error(y_true, y_pred)
        metrics['rmse'] = root_mean_squared_error(y_true, y_pred)
        return metrics
    
    def run_linear_regression(self):
        model = LinearRegression().fit(self.X, self.y)
        y_cv = model.predict(self.X)
        train_metrics = self.regression_metrics(self.y, y_cv)
        self.train_df['linear_reg'] = y_cv
        self.train_metrics_all['linear_reg'] = train_metrics
        y_pred = model.predict(self.X_new)
        test_metrics = self.regression_metrics(self.y_true, y_pred)
        self.test_df['linear_reg'] = y_pred
        self.test_metrics_all['linear_reg'] = test_metrics

    def run_ridge_regression(self, regularization=0.5):
        model = linear_model.Ridge(alpha=regularization).fit(self.X, self.y)
        y_cv = model.predict(self.X)
        train_metrics = self.regression_metrics(self.y, y_cv)
        self.train_df['ridge_reg'] = y_cv
        self.train_metrics_all['ridge_reg'] = train_metrics
        y_pred = model.predict(self.X_new)
        test_metrics = self.regression_metrics(self.y_true, y_pred)
        self.test_df['ridge_reg'] = y_pred
        self.test_metrics_all['ridge_reg'] = test_metrics

    def run_ridgecv_regression(self, regularization_range=100):
        model = linear_model.RidgeCV(alphas=regularization_range).fit(self.X, self.y)
        y_cv = model.predict(self.X)
        train_metrics = self.regression_metrics(self.y, y_cv)
        self.train_df['ridgecv_reg'] = y_cv
        self.train_metrics_all['ridgecv_reg'] = train_metrics
        y_pred = model.predict(self.X_new)
        test_metrics = self.regression_metrics(self.y_true, y_pred)
        self.test_df['ridgecv_reg'] = y_pred
        self.test_metrics_all['ridgecv_reg'] = test_metrics

    def run_lasso_regression(self, regularization=0.1):
        model = linear_model.Lasso(alpha=regularization).fit(self.X, self.y)
        y_cv = model.predict(self.X)
        train_metrics = self.regression_metrics(self.y, y_cv)
        self.train_df['lasso_reg'] = y_cv
        self.train_metrics_all['lasso_reg'] = train_metrics
        y_pred = model.predict(self.X_new)
        test_metrics = self.regression_metrics(self.y_true, y_pred)
        self.test_df['lasso_reg'] = y_pred
        self.test_metrics_all['lasso_reg'] = test_metrics

    def run_lassocv_regression(self, regularization_range=100):
        model = linear_model.LassoCV(alphas=regularization_range).fit(self.X, self.y)
        y_cv = model.predict(self.X)
        train_metrics = self.regression_metrics(self.y, y_cv)
        self.train_df['lassocv_reg'] = y_cv
        self.train_metrics_all['lassocv_reg'] = train_metrics
        y_pred = model.predict(self.X_new)
        test_metrics = self.regression_metrics(self.y_true, y_pred)
        self.test_df['lassocv_reg'] = y_pred
        self.test_metrics_all['lassocv_reg'] = test_metrics

    def run_decisiontree_regression(self):
        model = tree.DecisionTreeRegressor().fit(self.X, self.y)
        y_cv = model.predict(self.X)
        train_metrics = self.regression_metrics(self.y, y_cv)
        self.train_df['decisiontree_reg'] = y_cv
        self.train_metrics_all['decisiontree_reg'] = train_metrics
        y_pred = model.predict(self.X_new)
        test_metrics = self.regression_metrics(self.y_true, y_pred)
        self.test_df['decisiontree_reg'] = y_pred
        self.test_metrics_all['decisiontree_reg'] = test_metrics

    def run_svm_regression(self):
        model = svm.SVR().fit(self.X, self.y)
        y_cv = model.predict(self.X)
        train_metrics = self.regression_metrics(self.y, y_cv)
        self.train_df['svm_reg'] = y_cv
        self.train_metrics_all['svm_reg'] = train_metrics
        y_pred = model.predict(self.X_new)
        test_metrics = self.regression_metrics(self.y_true, y_pred)
        self.test_df['svm_reg'] = y_pred
        self.test_metrics_all['svm_reg'] = test_metrics

    def run_randomforest_regression(self):
        model = RandomForestRegressor(max_depth=5, random_state=0).fit(self.X, self.y)
        y_cv = model.predict(self.X)
        train_metrics = self.regression_metrics(self.y, y_cv)
        self.train_df['randomforest_reg'] = y_cv
        self.train_metrics_all['randomforest_reg'] = train_metrics
        y_pred = model.predict(self.X_new)
        test_metrics = self.regression_metrics(self.y_true, y_pred)
        self.test_df['randomforest_reg'] = y_pred
        self.test_metrics_all['randomforest_reg'] = test_metrics

    def run_gradboost_regression(self):
        model = GradientBoostingRegressor(random_state=0).fit(self.X, self.y)
        y_cv = model.predict(self.X)
        train_metrics = self.regression_metrics(self.y, y_cv)
        self.train_df['gradboost_reg'] = y_cv
        self.train_metrics_all['gradboost_reg'] = train_metrics
        y_pred = model.predict(self.X_new)
        test_metrics = self.regression_metrics(self.y_true, y_pred)
        self.test_df['gradboost_reg'] = y_pred
        self.test_metrics_all['gradboost_reg'] = test_metrics



# def logistic_regression(X, y, X_new, y_true):
#     model = LogisticRegression().fit(X, y)
#     y_pred = model.predict(X_new)
#     accuracy = accuracy_score(y_true, y_pred)
#     aucroc = auc(y_true, y_pred)
#     cm = confusion_matrix(y_true, y_pred)
#     f1 = f1_score(y_true, y_pred)
#     precision = precision_score(y_true, y_pred)
#     recall = recall_score(y_true, y_pred)
#     return accuracy, aucroc, cm, f1, precision, recall

# def decision_tree(X, y, X_new, y_true):
#     model = DecisionTreeClassifier().fit(X, y)
#     y_pred = model.predict(X_new)
#     accuracy = accuracy_score(y_true, y_pred)
#     aucroc = auc(y_true, y_pred)
#     cm = confusion_matrix(y_true, y_pred)
#     f1 = f1_score(y_true, y_pred)
#     precision = precision_score(y_true, y_pred)
#     recall = recall_score(y_true, y_pred)
#     return accuracy, aucroc, cm, f1, precision, recall

# def random_forest(X, y, X_new, y_true):
#     model = RandomForestClassifier().fit(X, y)
#     y_pred = model.predict(X_new)
#     accuracy = accuracy_score(y_true, y_pred)
#     aucroc = auc(y_true, y_pred)
#     cm = confusion_matrix(y_true, y_pred)
#     f1 = f1_score(y_true, y_pred)
#     precision = precision_score(y_true, y_pred)
#     recall = recall_score(y_true, y_pred)
#     return accuracy, aucroc, cm, f1, precision, recall

# def support_vector(X, y, X_new, y_true):
#     model = svm.SVC(kernel='linear').fit(X, y)
#     y_pred = model.predict(X_new)
#     accuracy = accuracy_score(y_true, y_pred)
#     aucroc = auc(y_true, y_pred)
#     cm = confusion_matrix(y_true, y_pred)
#     f1 = f1_score(y_true, y_pred)
#     precision = precision_score(y_true, y_pred)
#     recall = recall_score(y_true, y_pred)
#     return accuracy, aucroc, cm, f1, precision, recall

# def naive_bayes(X, y, X_new, y_true):
#     model = GaussianNB().fit(X, y)
#     y_pred = model.predict(X_new)
#     accuracy = accuracy_score(y_true, y_pred)
#     aucroc = auc(y_true, y_pred)
#     cm = confusion_matrix(y_true, y_pred)
#     f1 = f1_score(y_true, y_pred)
#     precision = precision_score(y_true, y_pred)
#     recall = recall_score(y_true, y_pred)
#     return accuracy, aucroc, cm, f1, precision, recall