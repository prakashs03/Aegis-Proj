import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
import joblib
import os
from tensorflow.keras import layers, models, callbacks

DATA_CSV = "data/historical_transactions.csv"
SCALER_PATH = "models/scaler_and_features.joblib"
IF_PATH = "models/if_model.joblib"
AE_PATH = "models/ae_model.h5"

def load_and_fe(df_path=DATA_CSV):
    df = pd.read_csv(df_path)
    df['amount_log'] = np.log1p(df['amount'])
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['hour'] = df['timestamp'].dt.hour
    df['hour_sin'] = np.sin(2*np.pi*df['hour']/24)
    df['hour_cos'] = np.cos(2*np.pi*df['hour']/24)
    top_countries = df['country'].value_counts().nlargest(10).index
    top_merchants = df['merchant'].value_counts().nlargest(20).index
    for c in top_countries:
        df[f"country_{c}"] = (df['country'] == c).astype(int)
    for m in top_merchants:
        df[f"merchant_{m}"] = (df['merchant'] == m).astype(int)
    features = ['amount_log','hour_sin','hour_cos'] + \
               [col for col in df.columns if col.startswith('country_') or col.startswith('merchant_')]
    X = df[features].fillna(0).values
    y = df['label'].values if 'label' in df.columns else None
    return X, y, features

def train():
    os.makedirs('models', exist_ok=True)
    X, y, feat = load_and_fe()
    scaler = StandardScaler()
    Xs = scaler.fit_transform(X)
    joblib.dump((scaler, feat), SCALER_PATH)
    print('Saved scaler/features')
    # IsolationForest
    if_model = IsolationForest(n_estimators=200, contamination=0.01, random_state=42)
    if_model.fit(Xs)
    joblib.dump(if_model, IF_PATH)
    print('Saved IsolationForest')
    # Autoencoder
    input_dim = Xs.shape[1]
    inp = layers.Input(shape=(input_dim,))
    x = layers.Dense(64, activation='relu')(inp)
    x = layers.Dense(32, activation='relu')(x)
    encoded = layers.Dense(min(16, input_dim//2), activation='relu')(x)
    x = layers.Dense(32, activation='relu')(encoded)
    x = layers.Dense(64, activation='relu')(x)
    out = layers.Dense(input_dim, activation='linear')(x)
    ae = models.Model(inp, out)
    ae.compile(optimizer='adam', loss='mse')
    es = callbacks.EarlyStopping(patience=5, restore_best_weights=True)
    ae.fit(Xs, Xs, epochs=30, batch_size=256, validation_split=0.1, callbacks=[es], verbose=1)
    ae.save(AE_PATH)
    print('Saved Autoencoder to', AE_PATH)
    # optional: print reconstruction error stats
    recon = ae.predict(Xs, verbose=0)
    mse = np.mean((recon - Xs)**2, axis=1)
    print('AE mse mean, 95th:', mse.mean(), np.percentile(mse,95))

if __name__ == '__main__':
    train()
