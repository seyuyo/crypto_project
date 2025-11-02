from flask import Flask
import requests
import psycopg
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import os

app = Flask(__name__)

# Adatbázis konfiguráció
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "db"),
    "dbname": os.getenv("DB_NAME", "crypto"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD")
}

# Lekéri az aktuális coin árakat és eltárolja az adatbázisban.
def fetch_and_store_prices():
    # Az API, ahonnan az árakat lekérdezzük
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 10,
        "page": 1
    }

    data = requests.get(url, params=params).json()
    timestamp = datetime.utcnow()

    # PostgreSQL kapcsolat psycopg3-mal
    with psycopg.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cursor:
            for coin in data:
                cursor.execute("""
                    INSERT INTO price_raw (symbol, price, timestamp)
                    VALUES (%s, %s, %s)
                """, (coin["symbol"], coin["current_price"], timestamp))


scheduler = BackgroundScheduler()
scheduler.add_job(fetch_and_store_prices, "interval", minutes=5)
scheduler.start()


@app.route("/health")
def health():
    return {"status": "collector running"}


if __name__ == "__main__":
    fetch_and_store_prices()  # első futtatás az induláskor
    app.run(host="0.0.0.0" ,port=5000)
