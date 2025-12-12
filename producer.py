import requests, time, json, sqlite3
from generate_data import gen_row
from datetime import datetime

API_URL = 'http://api:8000/predict'  # in docker network use service name; locally use http://localhost:8000/predict
DB = 'results.db'

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS results (
            txn_id TEXT PRIMARY KEY,
            timestamp TEXT,
            amount REAL,
            country TEXT,
            merchant TEXT,
            if_score REAL,
            ae_mse REAL,
            label INTEGER,
            raw TEXT
        )
    ''')
    conn.commit()
    conn.close()

def send_one(i, api_url):
    tx = gen_row(i)
    tx['timestamp'] = datetime.utcnow().isoformat()
    try:
        r = requests.post(api_url, json=tx, timeout=5)
        if r.status_code==200:
            j = r.json()
            conn = sqlite3.connect(DB)
            c = conn.cursor()
            c.execute('''INSERT OR REPLACE INTO results
                (txn_id,timestamp,amount,country,merchant,if_score,ae_mse,label,raw)
                VALUES (?,?,?,?,?,?,?,?,?)''',
                (j['txn_id'], tx['timestamp'], tx['amount'], tx['country'], tx['merchant'],
                j['if_score'], j['ae_mse'], j['label'], json.dumps(tx))
            )
            conn.commit()
            conn.close()
            print('Sent', tx['txn_id'], 'label=', j['label'])
        else:
            print('API error', r.status_code, r.text)
    except Exception as e:
        print('Request error', e)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--api', default='http://localhost:8000/predict', help='API URL')
    parser.add_argument('--rate', type=float, default=0.2, help='seconds between txns')
    parser.add_argument('--count', type=int, default=1000, help='how many transactions to send')
    args = parser.parse_args()
    init_db()
    for i in range(args.count):
        send_one(i, args.api)
        time.sleep(args.rate)
