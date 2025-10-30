# src/db.py
from sqlalchemy import create_engine, Column, Integer, Float, String, MetaData, Table, TIMESTAMP, text
from sqlalchemy.engine.url import make_url
from sqlalchemy.exc import OperationalError
import os
import time

DATABASE_URL = os.environ.get('DATABASE_URL','postgresql://mlflow:mlflowpass@postgres:5432/mlflow_db')

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

metadata = MetaData()

scores_table = Table(
    'scores', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('tx_id', String(128), nullable=False),
    Column('ts', TIMESTAMP, server_default=text('CURRENT_TIMESTAMP')),
    Column('score', Float, nullable=False),
    Column('label', Integer, nullable=True),
    Column('model', String(128), nullable=True)
)

def init_db(retries=5, wait=3):
    for i in range(retries):
        try:
            metadata.create_all(engine)
            return
        except OperationalError as e:
            time.sleep(wait)
    raise RuntimeError("Could not initialize DB")
