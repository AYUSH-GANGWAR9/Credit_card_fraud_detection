import mlflow, mlflow.sklearn, joblib, os
mlflow.set_tracking_uri("http://localhost:5000")
model_name = "creditcard_fraud_ensemble"

# log LGB
lgb = joblib.load("models/lgb_optuna.pkl")
with mlflow.start_run():
    mlflow.sklearn.log_model(lgb, "lgb_model", registered_model_name=model_name + "_lgb")

# log XGB (Booster) - wrap with sklearn wrapper or use mlflow.xgboost
xgb = joblib.load("models/xgb_optuna.pkl")
import mlflow.xgboost
mlflow.xgboost.log_model(xgb, artifact_path="xgb_model", registered_model_name=model_name + "_xgb")
