# src/kafka_producer.py
import json
import time
import argparse
import pandas as pd
from kafka import KafkaProducer
import joblib
import numpy as np

def send_transactions(csv_path='creditcard.csv', topic='transactions', rate=100, bootstrap_servers='localhost:9092'):
    # If you have preprocessed X_test saved as a CSV/npz, you can load that. Here we load creditcard.csv and construct feature dict.
    df = pd.read_csv('creditcard.csv')  # or load a preprocessed test csv
    # For demo: take a small sample or last 5000 rows as test stream
    df = df.sample(frac=1, random_state=42).reset_index(drop=True).iloc[:5000]
    producer = KafkaProducer(bootstrap_servers=bootstrap_servers,
                             value_serializer=lambda v: json.dumps(v).encode('utf-8'))
    for idx, row in df.iterrows():
        payload = {
            'tx_id': str(idx),
            'time': int(row['Time']),
            'Amount': float(row['Amount']),
            'features': {c: float(row[c]) for c in row.index if c.startswith('V') or c in ['Hour','Amount_scaled'] or c=='Amount'},
            'label': int(row['Class']) if 'Class' in row.index else 0
        }
        producer.send(topic, value=payload)
        if idx % 100 == 0:
            print(f"Sent {idx} messages")
        time.sleep(1.0 / rate)  # rate messages per second
    producer.flush()
    producer.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--topic', default='transactions')
    parser.add_argument('--rate', type=float, default=10.0)  # messages per second
    parser.add_argument('--bootstrap', default='localhost:9092')
    args = parser.parse_args()
    send_transactions(topic=args.topic, rate=args.rate, bootstrap_servers=args.bootstrap)
