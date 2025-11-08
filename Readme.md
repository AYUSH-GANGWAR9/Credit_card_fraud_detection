<h1 align="center">💳 Credit Card Fraud Detection System</h1>
<p align="center">
An end-to-end Machine Learning pipeline to detect fraudulent credit card transactions in real-time — complete with model training, evaluation, explainability, and a modern Streamlit dashboard.
</p>

<div align="center">
  
[![](https://img.shields.io/badge/ML-Pipeline-blueviolet?style=for-the-badge)]()
[![](https://img.shields.io/badge/Streamlit-App-red?style=for-the-badge)]()
[![](https://img.shields.io/badge/Imbalanced_Data-SMOTE-orange?style=for-the-badge)]()
[![](https://img.shields.io/badge/Model-LogisticRegression-success?style=for-the-badge)]()

</div>

---

## 🌟 Overview

Credit card fraud is **rare but costly**—only ~0.17% of transactions in this dataset are fraudulent.  
This project focuses on **catching frauds aggressively** while maintaining **precision**, using:

- **SMOTE** oversampling for class imbalance
- **Precision-Recall optimization**
- **Threshold tuning focused on maximum F1**
- **Streamlit dashboard** for real-time and batch scoring

This system is **deploy-ready**, **demo-ready**, and **resume-ready**.

---

## 🎯 Goal

Detect fraudulent transactions **before** they cause financial damage — focusing on:
- **High Recall for Fraud Class**
- **Low False-Alarm Rate**
- **Operational interpretability**

---

## 🧠 Dataset

| Feature | Description |
|--------|-------------|
| `V1` → `V28` | PCA-transformed features to anonymize sensitive data |
| `Amount` | Transaction value |
| `Class` | 0 → Legitimate, 1 → Fraud |

📌 Dataset Source: **Kaggle**  
https://www.kaggle.com/mlg-ulb/creditcardfraud

---

## 🔥 What This Project Includes

| Component | Status | Details |
|---------|:------:|---------|
| Data Preprocessing | ✅ | Scaling + SMOTE Oversampling |
| Model Training | ✅ | Logistic Regression + Class Weights |
| Threshold Optimization | ✅ | F1-based threshold selection |
| Performance Metrics | ✅ | PR-AUC, ROC-AUC, Confusion Matrix |
| Interactive Dashboard | ✅ | Streamlit UI for Prediction |
| Batch Inference | ✅ | Score entire CSV files |
| Deployment Option | ✅ | ngrok public demo link |

---

## 🚀 Quick Start (Google Colab — No Local Setup Required)

Just open the Colab notebook and run all cells:

📌 *`notebooks/training_pipeline.ipynb`*

This will automatically:
✔ Train the model  
✔ Save the artifacts  
✔ Launch the dashboard  
✔ Generate a public web URL  

No installations. No environment headaches.

---

## 🖥️ Streamlit App Preview

**App Features**
- Input transaction features → Get prediction instantly  
- Upload CSV → Get fraud scores for thousands of rows  
- One-click export to `fraud_predictions.csv`

---

## 🏗️ Project Architecture (System setup)
credit-card-fraud-detection/
│
├─ app.py                      # Streamlit Dashboard
├─ requirements.txt
│
├─ artifacts/
│   ├─ model.joblib            # Saved ML model
│   └─ metadata.json           # Threshold + feature list
│
├─ data/
│   └─ creditcard.csv          # Dataset (not included in repo)
│
├─ notebooks/
│   └─ training_pipeline.ipynb # Google Colab training notebook
│
└─ src/
    ├─ train.py                # Automated training script
    └─ predict_batch.py        # Batch CSV fraud scoring 


## 📈 Model Performance (Test Set)

| Metric | Value |
|-------|------|
| **ROC-AUC** | ~0.98 |
| **PR-AUC** | ~0.94 |
| **Optimized Threshold** | ~0.50 |
| **Fraud Recall** | **High** |
| **False Positives** | Mild & Acceptable for security-oriented system |

> Metrics vary slightly depending on random sampling & SMOTE variability.

---

## 🧑‍💼 Ideal Use Cases
- Fraud detection teams and fintech products  
- Banking security monitoring systems  
- Transaction anomaly detection engines  
- ML portfolio / resume projects  

---

🤝 Contributing
PRs are welcome! Submit enhancements or issues.

👨‍💻 Author
Ayush Gangwar
📍 India
🔗 LinkedIn: https://www.linkedin.com/in/ayush-gangwar-8a856b272/

⭐ Support
If you like this project, please ⭐ star the repo.
