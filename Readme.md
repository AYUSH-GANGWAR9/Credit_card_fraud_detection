# 🚀 Real-Time Credit Card Fraud Detection System (Full MLOps Pipeline)

### 🎯 End-to-End Production-Grade Fraud Detection | Kafka + FastAPI + MLflow + Streamlit + PostgreSQL + Docker

> A complete real-time machine learning pipeline that simulates bank-grade fraud detection and monitoring.

This project streams live transactions via **Kafka**, scores them using **XGBoost + LightGBM + Autoencoder ensemble**, stores results in **PostgreSQL**, serves predictions through **FastAPI**, tracks models with **MLflow**, and visualizes insights in **Streamlit**.

🎓 Ideal for: *MLOps learning, portfolio showcase, ML systems interview prep, production design understanding*

---

## 📌 Features

| Capability | Tech |
|---|---|
| ✅ Real-time streaming fraud inference | Kafka + Python Consumer |
| ✅ ML model ensemble (LGBM + XGBoost + Autoencoder) | Trained in Colab |
| ✅ Model versioning | MLflow |
| ✅ REST API for live fraud scores | FastAPI |
| ✅ Transaction & score database | PostgreSQL |
| ✅ Live dashboard | Streamlit |
| ✅ Fully containerized | Docker Compose |
| ✅ Synthetic live transaction generator | Python Kafka Producer |
| ✅ Metrics: AP, ROC-AUC, PR Curve | Streamlit + DB queries |

---

## 🏗️ Architecture Diagram

Google Colab (training)
│ export models
▼
/models
│
Kafka Producer → Kafka → Fraud Consumer → FastAPI → PostgreSQL
│ │
│ └→ MLflow (model registry)
└→ Streamlit Dashboard (Live Monitoring)

yaml
Copy code

---

## 📂 Project Structure

```bash
credit-card-fraud-detection/
├── docker-compose.yml
├── models/                # 🔴 REQUIRED (export from Colab)
│   ├── lgb_optuna.pkl
│   ├── xgb_optuna.pkl
│   ├── autoencoder.h5
│   └── scaler.pkl
├── src/
│   ├── kafka_producer.py
│   ├── kafka_consumer.py
│   ├── serve.py          # FastAPI backend
│   ├── streamlit_app.py  # Dashboard
│   ├── db.py
│   └── register_models.py
└── README.md

🎒 Requirements
Tool	Version
Docker Desktop	✅ recommended
Python	3.8+
Google Colab	For training models

📁 Place Your Trained Models Here
Before running 🚨 you must add exported models to /models/:

File	Source
lgb_optuna.pkl	Colab
xgb_optuna.pkl	Colab
autoencoder.h5	Colab
scaler.pkl	Colab

(These are generated after training)

⚡ Run With Docker (Recommended)

🔥 1. Start services
bash
Copy code
docker-compose up -d zookeeper kafka postgres mlflow

🐳 2. Build & start apps
bash
Copy code
docker-compose build fastapi consumer streamlit
docker-compose up -d fastapi consumer streamlit

📊 3. Produce live transaction stream
bash
Copy code
python src/kafka_producer.py --topic transactions --rate 5 --bootstrap localhost:9092

🌐 URLs
Service	URL:
🧠 MLflow	http://localhost:5000
⚙️ FastAPI Docs	http://localhost:8000/docs
📈 Streamlit Dashboard	http://localhost:8501
🗄️ PostgreSQL	localhost:5432
💬 Kafka Broker	localhost:9092

🧪 Test API
bash
Copy code
curl "http://localhost:8000/latest_scores?limit=10"
👀 What You Will See
✅ Streamlit Dashboard
Live incoming transactions

Fraud score timeline

Precision-Recall curve

ROC-AUC, Avg Score, Model Version

Number of live fraud alerts

✅ FastAPI UI
Try requests and see responses live

✅ Console Logs
Scored tx XXXXX score: 0.983

Inserted into DB

Kafka consumer active

💡 Expected Output Behavior
Component	Output
Kafka Producer	Streaming random transactions
Consumer	Scores each tx & posts to API
FastAPI	Saves & exposes latest scores
Postgres	Table scores updates in real-time
Streamlit	Live dashboard & PR curve evolves
Fraud Alerts	High score → potential fraud

🧯 Troubleshooting
Error	Fix
ModuleNotFoundError: sklearn	Add to Dockerfile & rebuild
libgomp.so.1	Install gcc, g++, libgomp1
NoBrokersAvailable	Restart Kafka / check .env
SQLAlchemy select error	Use select(table) syntax
Keras load error	compile=False while loading

🚀 Future Enhancements
✅ Multi-model A/B testing
✅ Prometheus + Grafana load metrics
🔄 Online learning mode
🔐 RBAC and JWT auth
🌐 Deploy to Kubernetes (GCP/EKS)

🤝 Contributing
PRs are welcome! Submit enhancements or issues.

👨‍💻 Author
Ayush Gangwar
📍 India
🔗 LinkedIn: https://www.linkedin.com/in/ayush-gangwar-8a856b272/

⭐ Support
If you like this project, please ⭐ star the repo.

This MLOps build shows your production-thinking, real-world ML deployment skills, and modern data engineering stack knowledge.


