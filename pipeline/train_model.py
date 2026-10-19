from sklearn.model_selection import train_test_split
import json
from pipeline.supervised_ml import RunRegressionModels
import joblib
import pandas as pd

clean_df = pd.read_csv(r"C:\Users\nurai\OneDrive\Documents\GitHub\StrokePrediction\data\preprocessed.csv", index=False)
target = 'surv18' # for regression # nts: defined here and preprocessing.py

# split data into train and test sets
X_train, X_test, y_train, y_test = train_test_split(clean_df.drop(target, axis=1), clean_df[target], 
                                                    test_size=0.2, random_state=42)

feature_names = X_train.columns.tolist()
with open("feature_names.json", "w") as f:
    json.dump(feature_names, f)
# actual: 183
# linear regression prediction: 396.0586995197378
with open("dummy_data.json", "w") as f:
    json.dump(X_train.iloc[0].to_dict(), f)

test_run = RunRegressionModels(X_train, y_train, X_test, y_test)
test_run.run_linear_regression(save_model=True)
test_run.run_lasso_regression()
test_run.run_lassocv_regression()
test_run.run_ridge_regression()
test_run.run_ridgecv_regression()
test_run.run_decisiontree_regression()
test_run.run_svm_regression()
test_run.run_randomforest_regression()
test_run.run_gradboost_regression()

# save model
joblib.dump(test_run.models['linear_reg'], "stroke_prediction_model.joblib")