import streamlit as st
import pandas as pd
import sqlite3
import time

DB = 'results.db'

st.set_page_config(page_title='Aegis Dashboard', layout='wide')
st.title('Aegis - Live Fraud Dashboard')

# Connect to SQLite DB
conn = sqlite3.connect(DB, check_same_thread=False)

# Load data safely
@st.cache_data(ttl=3)
def load_data(limit=1000):
    try:
        df = pd.read_sql_query(
            "SELECT * FROM results ORDER BY rowid DESC LIMIT ?", 
            conn, 
            params=(limit,)
        )
        return df
    except Exception:
        return pd.DataFrame()

# Sidebar
refresh = st.sidebar.slider('Refresh seconds', min_value=1, max_value=10, value=3)
st.sidebar.write('Data: producer → API → results.db')

# Load data
df = load_data()

# ❗ Stop refreshing if 200 transactions reached
if len(df) >= 200:
    st.success("Loaded 200 transactions. Dashboard is now static (no auto-refresh).")

else:
    # Continue refreshing until 200 loaded
    time.sleep(refresh)
    st.experimental_rerun()

# If no data found
if df.empty:
    st.info("No transactions yet. Run producer.py to stream transactions.")
    st.stop()

# Top metrics
st.metric("Total transactions", len(df))
flagged = df[df['label'] == 1]
st.metric("Flagged transactions", len(flagged))

col1, col2 = st.columns(2)

# Latest flagged
with col1:
    st.subheader("Latest flagged")
    if len(flagged) == 0:
        st.info("No fraudulent transactions detected yet.")
    else:
        st.dataframe(
            flagged[['txn_id', 'timestamp', 'amount', 'country', 'merchant', 'if_score', 'ae_mse']].head(50)
        )

# Flagged by country (SAFE VERSION)
with col2:
    st.subheader("Flagged by country")
    if len(flagged) == 0:
        st.info("No flagged data available.")
    else:
        country_counts = flagged['country'].value_counts().head(10)
        st.bar_chart(country_counts)

# Recent transactions
st.subheader("Recent txns")
st.dataframe(df[['txn_id', 'timestamp', 'amount', 'country', 'merchant', 'label']].head(200))
