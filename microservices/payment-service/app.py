from flask import Flask, jsonify, request
import random
import time
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

@app.route("/")
def home():
    return jsonify({"service": "Payment Service Running"}), 200

@app.route("/checkout", methods=["POST"])
def checkout():
    data = request.get_json()
    amount = data.get("amount", 0)
    items = data.get("items", [])
    
    if not amount or not items:
        return jsonify({
            "status": "FAILED",
            "reason": "Invalid request - missing amount or items"
        }), 400
    
    # Simulate payment processing delay
    delay = random.randint(1, 3)
    time.sleep(delay)

    # 30% chance of payment failure for testing
    if random.random() < 0.3:
        logging.warning(f"Payment failed for amount: {amount}")
        return jsonify({
            "status": "FAILED",
            "reason": "Payment processing error",
            "amount": amount
        }), 500

    logging.info(f"Payment successful for amount: {amount}, items: {len(items)}")
    return jsonify({
        "status": "SUCCESS",
        "message": "Payment successful",
        "amount": amount,
        "items_count": len(items),
        "transaction_id": f"TXN-{int(time.time())}"
    }), 200

@app.route("/health")
def health():
    return jsonify({"status": "UP"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003)
