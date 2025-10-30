# src/serve.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import os, time
import joblib
from collections import deque
from sqlalchemy import insert, select
from src import db

app = FastAPI()
db.init_db()

# load models if present (if not present, endpoints still work)
MODEL_PATH_LGB = os.environ.get('MODEL_LGB', '/app/models/lgb_optuna.pkl')
MODEL_PATH_XGB = os.environ.get('MODEL_XGB', '/app/models/xgb_optuna.pkl')

try:
    lgb_model = joblib.load(MODEL_PATH_LGB)
except Exception as e:
    lgb_model = None

try:
    import xgboost as xgb
    xgb_model = joblib.load(MODEL_PATH_XGB)
except Exception as e:
    xgb_model = None

class ScorePayload(BaseModel):
    tx_id: str
    time: Optional[int]
    score: float
    label: Optional[int] = None
    model: Optional[str] = None

@app.post("/ingest_score")
def ingest_score(payload: ScorePayload):
    entry = payload.dict()
    entry['time'] = entry.get('time') or int(time.time())
    # persist to Postgres
    conn = db.engine.connect()
    ins = insert(db.scores_table).values(
        tx_id=entry['tx_id'],
        score=entry['score'],
        label=entry.get('label'),
        model=entry.get('model')
    )
    conn.execute(ins)
    conn.close()
    return {"status":"ok", "stored": True}

@app.get("/latest_scores")
def latest_scores(limit: int = 100):
    conn = db.engine.connect()
    stmt = select(db.scores_table).order_by(db.scores_table.c.id.desc()).limit(limit)
    res = conn.execute(stmt).fetchall()
    conn.close()
    # convert to list of dicts
    out = [dict(r) for r in res]
    return out

@app.get("/metrics")
def metrics(window: int = 500):
    conn = db.engine.connect()
    stmt = select(db.scores_table).order_by(db.scores_table.c.id.desc()).limit(window)
    res = conn.execute(stmt).fetchall()
    conn.close()
    if not res:
        return {"count":0}
    import numpy as np
    arr = [dict(r) for r in res]
    scores = np.array([r['score'] for r in arr])
    labels = np.array([r['label'] or 0 for r in arr])
    from sklearn.metrics import average_precision_score, roc_auc_score
    return {
        "count": len(arr),
        "avg_score": float(scores.mean()),
        "ap": float(average_precision_score(labels, scores)) if labels.sum()>0 else None,
        "roc_auc": float(roc_auc_score(labels, scores)) if labels.sum()>0 else None
    }
