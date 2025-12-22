from flask import Flask, jsonify
from app.db import get_connection
from app.config import Config

app = Flask(__name__)

@app.route("/health")
def health():
    return jsonify(status="ok", env=Config.APP_ENV)

@app.route("/info")
def info():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT message FROM info LIMIT 1;")
    row = cursor.fetchone()
    cursor.close()
    conn.close()

    return jsonify(message=row[0] if row else "no data")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
