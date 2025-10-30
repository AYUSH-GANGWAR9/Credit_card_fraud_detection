# src/kafka_consumer.py
import json, os, time, requests
from kafka import KafkaConsumer, KafkaProducer
import joblib, pandas as pd, numpy as np
from sqlalchemy import insert
from src import db
from src.db import *

KAFKA_BOOTSTRAP = os.environ.get('KAFKA_BOOTSTRAP','kafka:9092')
FASTAPI_INGEST = os.environ.get('FASTAPI_INGEST','http://fastapi:8000/ingest_score')
DB_URL = os.environ.get('DATABASE_URL','postgresql://mlflow:mlflowpass@postgres:5432/mlflow_db')
MLFLOW_URI = os.environ.get('MLFLOW_TRACKING_URI','http://mlflow:5000')

# init DB table
db.init_db()

print("Loading models...")
lgb_model = None
xgb_model = None
if os.path.exists('/app/models/lgb_optuna.pkl'):
    lgb_model = joblib.load('/app/models/lgb_optuna.pkl')
if os.path.exists('/app/models/xgb_optuna.pkl'):
    xgb_model = joblib.load('/app/models/xgb_optuna.pkl')
scaler = joblib.load('/app/models/scaler.pkl') if os.path.exists('/app/models/scaler.pkl') else None

consumer = KafkaConsumer(
    'transactions',
    bootstrap_servers=KAFKA_BOOTSTRAP,
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)
producer = KafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP, value_serializer=lambda v: json.dumps(v).encode('utf-8'))

# optional MLflow usage
try:
    import mlflow
    mlflow.set_tracking_uri(MLFLOW_URI)
    mlflow_client = mlflow.tracking.MlflowClient()
except Exception as e:
    mlflow = None
    mlflow_client = None

def features_to_df(features):
    df = pd.DataFrame([features])
    return df

print("Consumer started...")
for msg in consumer:
    payload = msg.value
    tx_id = payload.get('tx_id')
    label = int(payload.get('label', 0))
    features = payload.get('features', {})
    df = features_to_df(features)
    # ensure numeric columns exist
    num_cols = ['Amount_scaled'] + [c for c in df.columns if c.startswith('V')] + ['Hour']
    for c in num_cols:
        if c not in df.columns: df[c]=0.0
    if scaler is not None:
        df[num_cols] = scaler.transform(df[num_cols])

    # score
    try:
        import xgboost as xgb
        px = xgb_model.predict(xgb.DMatrix(df))[0] if xgb_model is not None else 0.0
    except Exception:
        px = 0.0
    try:
        pl = lgb_model.predict(df)[0] if lgb_model is not None else 0.0
    except Exception:
        pl = 0.0
    score = float((px + pl) / 2.0)

    out = {'tx_id': tx_id, 'time': int(time.time()), 'score': score, 'label': label, 'model': 'ensemble_v1'}
    # produce to scores topic
    producer.send('scores', value=out)

    # persist to fastapi (which will write to Postgres)
    try:
        requests.post(FASTAPI_INGEST, json=out, timeout=2.0)
    except Exception as e:
        print("POST to FastAPI failed:", e)

    # log a metric to MLflow if available (per 100 messages to avoid spam)
    if mlflow and mlflow_client:
        try:
            mlflow.set_experiment("fraud_scoring")
            with mlflow.start_run(nested=True):
                mlflow.log_metric("last_score", score)
                # optionally log label counts etc.
        except Exception as e:
            print("MLflow log error:", e)

    print(f"Scored tx {tx_id} -> {score:.4f}")
