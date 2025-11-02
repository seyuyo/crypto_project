from flask import Flask
import psycopg
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
import os

app = Flask(__name__)

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "db"),
    "dbname": os.getenv("DB_NAME", "crypto"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD")
}

def calculate_trends():
    now = datetime.utcnow()
    one_hour_ago = now - timedelta(hours=1)
    one_day_ago = now - timedelta(hours=24)

    with psycopg.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cursor:
            # Listázzuk milyen coin-ok vannak
            cursor.execute("SELECT DISTINCT symbol FROM price_raw")
            symbols = [row[0] for row in cursor.fetchall()]

            for symbol in symbols:
                # 1h átlag
                cursor.execute("""
                    SELECT AVG(price) 
                    FROM price_raw
                    WHERE symbol = %s AND timestamp >= %s
                """, (symbol, one_hour_ago))
                avg_1h = cursor.fetchone()[0]

                # 24h átlag
                cursor.execute("""
                    SELECT AVG(price) 
                    FROM price_raw
                    WHERE symbol = %s AND timestamp >= %s
                """, (symbol, one_day_ago))
                avg_24h = cursor.fetchone()[0]

                # stat mentése
                cursor.execute("""
                    INSERT INTO trend_stats (symbol, avg_1h, avg_24h, timestamp)
                    VALUES (%s, %s, %s, %s);
                """, (symbol, avg_1h, avg_24h, now))

scheduler = BackgroundScheduler()
scheduler.add_job(calculate_trends, "interval", minutes=5)
scheduler.start()

@app.route("/health")
def health():
    return {"status": "processor running"}

if __name__ == "__main__":
    calculate_trends()  # első futás induláskor
    app.run(host="0.0.0.0" ,port=5001)
