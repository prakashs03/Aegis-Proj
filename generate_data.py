import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

OUT_CSV = "data/historical_transactions.csv"

def random_card():
    return f"{random.randint(4000000000000000,4999999999999999)}"

def gen_row(i):
    base_time = datetime.utcnow() - timedelta(days=random.randint(0,30))
    txn_time = base_time + timedelta(seconds=random.randint(0,86400))
    amount = round(np.random.exponential(scale=50.0),2)
    country = random.choice(["IN","US","GB","CN","DE","FR","JP"])
    merchant = random.choice(["amazon","walmart","flipkart","local_shop","electronics_mall","airline"])
    card = random_card()
    label = 0
    if amount > 200 and country != "IN" and random.random() < 0.6:
        label = 1
    if random.random() < 0.005:
        label = 1
    return {
        "txn_id": f"tx{i:08d}",
        "timestamp": txn_time.isoformat(),
        "amount": amount,
        "country": country,
        "merchant": merchant,
        "card_num": card,
        "label": label
    }

def generate(n=20000):
    import os
    os.makedirs("data", exist_ok=True)
    rows = [gen_row(i) for i in range(n)]
    df = pd.DataFrame(rows)
    df.to_csv(OUT_CSV, index=False)
    print(f"Saved {OUT_CSV} with {len(df)} rows")

if __name__ == "__main__":
    generate(20000)
