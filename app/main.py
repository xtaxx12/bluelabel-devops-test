from flask import Flask, jsonify
from app.db import get_connection
from app.config import Config

app = Flask(__name__)


@app.route("/")
def root():
    return jsonify(
        service="BlueLabel DevOps API",
        version="1.0.0",
        status="running",
        env=Config.APP_ENV,
        endpoints=["/health", "/info"]
    )


@app.route("/health")
def health():
    # Health check endpoint
    return jsonify(status="ok", env=Config.APP_ENV)


@app.route("/info")
def info():
    # Obtiene mensaje desde la base de datos
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT message FROM info LIMIT 1;")
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return jsonify(message=row[0] if row else "no data")
    except Exception as e:
        return jsonify(error="Database connection failed", details=str(e)), 503


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
