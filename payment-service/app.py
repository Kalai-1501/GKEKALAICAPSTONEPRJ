from flask import Flask, jsonify
import random
import time

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"service": "Payment Service Running"}), 200

@app.route("/checkout", methods=["POST"])
def checkout():
    delay = random.randint(1, 5)
    time.sleep(delay)

    if random.random() < 0.3:
        return jsonify({
            "status": "FAILED",
            "reason": "Payment failed"
        }), 500

    return jsonify({
        "status": "SUCCESS",
        "message": "Payment successful"
    }), 200

@app.route("/health")
def health():
    return jsonify({"status": "UP"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003)
