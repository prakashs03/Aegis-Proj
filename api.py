from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import numpy as np
import pandas as pd
import uvicorn
import os
import tensorflow as tf

SCALER_PATH = 'models/scaler_and_features.joblib'
IF_PATH = 'models/if_model.joblib'
AE_PATH = 'models/ae_model.h5'

app = FastAPI(title='Aegis Fraud API')

class Txn(BaseModel):
    txn_id: str
    timestamp: str
    amount: float
    country: str
    merchant: str
    card_num: str = None

if not os.path.exists(SCALER_PATH):
    raise RuntimeError('Model artifacts not found. Run train_model.py first.')

scaler, FEATURES = joblib.load(SCALER_PATH)
if_model = joblib.load(IF_PATH)
ae = tf.keras.models.load_model(AE_PATH)

# thresholds - tune these after training
IF_ANOMALY_THRESH = 0.1
AE_RECON_THRESH = 0.05

def fe_single(txn):
    amount_log = np.log1p(txn['amount'])
    ts = pd.to_datetime(txn['timestamp'])
    hour = ts.hour
    hour_sin = np.sin(2*np.pi*hour/24)
    hour_cos = np.cos(2*np.pi*hour/24)
    vec = [amount_log, hour_sin, hour_cos]
    for f in FEATURES:
        if f.startswith('country_'):
            c = f.split('_',1)[1]
            vec.append(1 if txn.get('country')==c else 0)
        elif f.startswith('merchant_'):
            m = f.split('_',1)[1]
            vec.append(1 if txn.get('merchant')==m else 0)
    return np.array(vec, dtype=float).reshape(1,-1)

@app.post('/predict')
async def predict(txn: Txn):
    try:
        data = txn.dict()
        x = fe_single(data)
        x_scaled = scaler.transform(x)
        if_score = if_model.decision_function(x_scaled)[0]
        recon = ae.predict(x_scaled, verbose=0)
        mse = float(np.mean(np.square(recon - x_scaled)))
        label = 1 if (if_score < IF_ANOMALY_THRESH or mse > AE_RECON_THRESH) else 0
        return {'txn_id': data['txn_id'], 'if_score': float(if_score), 'ae_mse': mse, 'label': int(label)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
