import mlflow
import joblib
from tensorflow.keras.models import load_model

# Paths
lgb_path = "models/lgb_optuna.pkl"
xgb_path = "models/xgb_optuna.pkl"
ae_path  = "models/autoencoder.h5"
scaler_path = "models/scaler.pkl"

# Load models
lgb_model = joblib.load(lgb_path)
xgb_model = joblib.load(xgb_path)
autoencoder = load_model(ae_path, compile=False)
scaler = joblib.load(scaler_path)

mlflow.set_tracking_uri("http://127.0.0.1:5000")
mlflow.set_experiment("Credit-Fraud-Detection")

with mlflow.start_run(run_name="model-registration"):

    # Log models to MLflow
    mlflow.sklearn.log_model(lgb_model, "lgb_model", registered_model_name="LightGBM-Fraud-Detector")
    mlflow.sklearn.log_model(xgb_model, "xgb_model", registered_model_name="XGBoost-Fraud-Detector")
    mlflow.keras.log_model(autoencoder, "autoencoder_model", registered_model_name="Autoencoder-Fraud-Detector")

    # Log scaler as artifact
    mlflow.log_artifact(scaler_path, artifact_path="preprocessing")

print("✅ Models registered in MLflow")
