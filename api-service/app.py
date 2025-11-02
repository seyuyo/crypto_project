from flask import Flask, jsonify
from flask_cors import CORS
import psycopg
import os


app = Flask(__name__)
CORS(app)
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "db"),
    "dbname": os.getenv("DB_NAME", "crypto"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD")
}

"""
Visszaadja az 1 órás és 24 órás átlagárakat coinonként.
Dashboard is ezt használja.
"""
@app.route("/trends")
def get_trends():
    with psycopg.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT symbol, avg_1h, avg_24h, timestamp 
                FROM trend_stats
                ORDER BY timestamp DESC;
            """)
            rows = cursor.fetchall()

    result = [
        {
            "symbol": r[0],
            "avg_1h": r[1],
            "avg_24h": r[2],
            "timestamp": r[3].isoformat()
        }
        for r in rows
    ]

    return jsonify(result)

@app.route("/health")
def health():
    return {"status": "api running"}

if __name__ == "__main__":
    app.run(host="0.0.0.0" ,port=5002)
