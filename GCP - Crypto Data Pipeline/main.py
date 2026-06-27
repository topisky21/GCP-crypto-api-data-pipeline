import os
from flask import Flask
import requests
from google.cloud import bigquery
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def run_pipeline(url):
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "ids": "bitcoin,ethereum,solana"
    }
    data = requests.get(url, params=params).json()

    client = bigquery.Client()
    rows = []
    for coin in data:
        rows.append({
            "id": coin["id"],
            "name": coin["name"],
            "symbol": coin["symbol"],
            "current_price": coin["current_price"],
            "market_cap": coin["market_cap"],
            "load_time": datetime.utcnow().isoformat()
        })

    client.insert_rows_json(
        "the-first-project-495311.crypto.market_data",
        rows
    )
    return "Pipeline executed successfully"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)