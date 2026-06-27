# GCP Crypto Data Pipeline

## Overview
This project builds an automated data pipeline on Google Cloud Platform that extracts cryptocurrency market data from CoinGecko API, processes it, and stores it in BigQuery for analytics.

---

## Pipeline Steps

1. **Extract** — Cloud Function calls CoinGecko API every hour via Cloud Scheduler
2. **Load** — Raw data (Bitcoin, Ethereum, Solana) inserted into BigQuery `crypto.market_data`
3. **Transform** — SQL query aggregates average price, max price, and market cap into `crypto.analytics`
4. **Visualise** — Looker Studio dashboard connects to BigQuery for live reporting

---

## BigQuery Schema

**`crypto.market_data`**

| Column | Type | Description |
|---|---|---|
| id | STRING | Coin identifier |
| name | STRING | Coin name |
| symbol | STRING | Ticker symbol |
| current_price | FLOAT | Price in USD at load time |
| market_cap | FLOAT | Market cap in USD |
| load_time | TIMESTAMP | UTC timestamp of ingestion |

---

## SQL Transformations

**Average price per coin:**
```sql
SELECT 
    id,
    name,
    AVG(current_price) AS average_price
FROM `the-first-project-495311.crypto.market_data`
GROUP BY id, name
```

**Analytics table:**
```sql
CREATE OR REPLACE TABLE `the-first-project-495311.crypto.analytics` AS
SELECT
    name,
    symbol,
    AVG(current_price) AS avg_price,
    MAX(current_price) AS max_price,
    AVG(market_cap)    AS avg_market_cap
FROM `the-first-project-495311.crypto.market_data`
GROUP BY name, symbol
```

---

## Setup & Deployment

### Prerequisites
- GCP account with billing enabled
- APIs enabled: Cloud Functions, BigQuery, Cloud Scheduler, Cloud Storage, Cloud Build

### Deploy the Cloud Function

1. Open Cloud Functions in GCP Console
2. Create a new function with HTTP trigger
3. Set runtime to Python 3.12
4. Paste `main.py` and `requirements.txt` from `cloud_function/`
5. Set entry point to `extract_crypto`
6. Deploy

### Automate with Cloud Scheduler

- Frequency: `0 * * * *` (every hour)
- Target: HTTP — paste your Cloud Function URL

---

## Key Learnings

- Building serverless data pipelines on GCP
- Streaming inserts into BigQuery using the Python client library
- Scheduling automated workflows with Cloud Scheduler
- Writing SQL transformations for analytics use cases
- Connecting BigQuery to Looker Studio for live dashboards

---

## Author

Temi
Analytics Engineer
