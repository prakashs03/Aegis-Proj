# Aegis – Real-time Transaction Fraud Detection

Aegis is an end-to-end **real-time credit card fraud detection system** built using  
**Python, Machine Learning, FastAPI, Streaming, SQLite, and Streamlit**.

This project demonstrates how modern payment systems detect fraud **instantly** rather than relying on slow batch processing.

---

## 🚀 Project Overview

Aegis processes each incoming transaction in real time and classifies it as **normal or fraudulent** using anomaly detection models.

### The system includes:
- **Data Generator** – creates synthetic credit card transactions  
- **Feature Engineering Pipeline**  
- **ML Models** – Isolation Forest + Autoencoder  
- **FastAPI Real-time Prediction Service**  
- **Producer Stream Simulator**  
- **SQLite Database** (`results.db`)  
- **Streamlit Dashboard for Visualization**  

---

## 🎯 Objective

The main objective of this project is to detect fraudulent credit card transactions **in real time**.  
Traditional systems identify fraud after the transaction is completed, but this system aims to flag it instantly using ML, reducing financial loss and increasing security.

---

## 🧠 Machine Learning Models

### **1. Isolation Forest**
- Unsupervised anomaly detection  
- Finds unusual patterns in transactions  
- Fast and efficient  

### **2. Autoencoder (Optional)**
- Learns normal transaction behavior  
- High reconstruction error = suspicious  

---

## 🏗️ System Architecture

```
Data Generator → Feature Engineering → ML Models → FastAPI API → Producer Stream → SQLite DB → Streamlit Dashboard
```

This forms a complete real-time fraud detection pipeline.

---

## 📂 Folder Structure

```
Aegis_Fraud_Detection/
│
├── api.py                   # FastAPI service for real-time predictions
├── producer.py              # Sends transactions to API in real time
├── dashboard.py             # Streamlit dashboard
├── generate_data.py         # Creates training dataset
├── train_model.py           # Isolation Forest & Autoencoder training
│
├── data/                    # Training dataset
├── models/                  # Saved ML models
├── results.db               # SQLite DB storing predictions
│
├── requirements.txt         # Python dependencies
│
└── README.md                # Project documentation
```

---

## ⚙️ Setup & Usage

### **1️⃣ Install dependencies**
```bash
pip install -r requirements.txt
```

### **2️⃣ Generate dataset**
```bash
python generate_data.py
```

### **3️⃣ Train ML models**
```bash
python train_model.py
```

### **4️⃣ Start FastAPI**
```bash
uvicorn api:app --reload --port 8000
```

### **5️⃣ Start streaming producer**
```bash
python producer.py --count 200 --rate 0.2
```

### **6️⃣ Launch Streamlit dashboard**
```bash
streamlit run dashboard.py
```

---

## 📊 Dashboard Features

- Total transactions processed  
- Fraud cases detected  
- Latest flagged transactions  
- Fraud distribution by country  
- Recent transactions table  
- Auto-stop refresh at 200 transactions  

---

## 🧪 Sample Output (From Your Run)

- **200 transactions processed**
- **20 frauds detected**
- Fraud reports visible in dashboard  
- Live chart for fraud by country  

---

## 🔮 Future Enhancements

- Replace producer with Kafka  
- Cloud deployment (AWS/GCP/Azure)  
- SMS/Email fraud alerts  
- Larger training dataset  
- Improved Autoencoder architecture  

---

## 🏁 Conclusion

Aegis integrates ML, APIs, streaming, and analytics into one complete real-time fraud detection system.  
This replicates how real banking systems detect suspicious activity instantly.

---

## 👤 Author

**Jayaprakash Srinivasan**  
Real-time ML & Python Developer  
GitHub: github.com/prakashs03
