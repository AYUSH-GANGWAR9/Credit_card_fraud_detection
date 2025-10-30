# src/streamlit_app.py
import streamlit as st
import pandas as pd
import numpy as np
import joblib
import time
from collections import deque
from sklearn.metrics import precision_recall_curve, average_precision_score, roc_auc_score
import plotly.graph_objects as go

# CONFIG
SCORES_STORE = deque(maxlen=1000)  # in-memory store for demo (consumer will POST here)

@st.cache_resource
def load_models():
    import xgboost as xgb
    import lightgbm as lgb
    try:
        lgb_model = joblib.load('models/lgb_optuna.pkl')
    except:
        lgb_model = None
    try:
        xgb_model = joblib.load('models/xgb_optuna.pkl')
    except:
        xgb_model = None
    scaler = joblib.load('models/scaler.pkl') if (Path := 'models/scaler.pkl') else None
    return xgb_model, lgb_model, scaler

st.set_page_config(layout="wide", page_title="Fraud Dashboard")
st.title("Credit Card Fraud Detection — Live Dashboard")

xgb_model, lgb_model, scaler = load_models()

col1, col2 = st.columns(2)

with col1:
    st.subheader("Live incoming transactions (most recent)")
    latest_df = pd.DataFrame(list(SCORES_STORE))[['time','score','label','tx_id']].tail(20) if len(SCORES_STORE) else pd.DataFrame()
    st.table(latest_df)

with col2:
    st.subheader("Summary metrics (last N)")
    n = st.slider("Window size (records)", min_value=100, max_value=1000, value=500, step=100)
    recent = pd.DataFrame(list(SCORES_STORE))[-n:]
    if not recent.empty:
        ap = average_precision_score(recent['label'], recent['score'])
        roc = roc_auc_score(recent['label'], recent['score'])
        st.metric("Average Precision (AP)", f"{ap:.4f}")
        st.metric("ROC AUC", f"{roc:.4f}")
    else:
        st.write("No scored transactions yet — start the consumer.")

st.markdown("---")
st.subheader("Precision-Recall curve (live window)")
if len(SCORES_STORE) >= 50:
    recent = pd.DataFrame(list(SCORES_STORE)).tail(n)
    p, r, _ = precision_recall_curve(recent['label'], recent['score'])
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=r, y=p, mode='lines', name='PR'))
    fig.update_layout(xaxis_title='Recall', yaxis_title='Precision', width=900, height=500)
    st.plotly_chart(fig)
else:
    st.write("Not enough data to plot PR curve (need >= 50 records).")

st.markdown("---")
st.subheader("Controls")
if st.button("Clear store"):
    SCORES_STORE.clear()
    st.success("Cleared in-memory store")

st.markdown("## REST ingestion endpoint (for demo)")
st.code("POST /ingest_score  -> JSON payload { 'tx_id':str, 'score':float, 'label':0/1, 'time':timestamp }")

# Small local server to accept POSTs would be the FastAPI consumer; for demo you can simulate push here.
st.markdown("To simulate: run the Kafka consumer which will POST to the FastAPI endpoint. This dashboard reads from in-memory store; if you deploy, point Streamlit to a DB or change consumer to write to a file/DB.")
