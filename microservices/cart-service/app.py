from flask import Flask, jsonify, request
import requests
import os

# ✅ CREATE APP FIRST
app = Flask(__name__)

# Use Kubernetes DNS for service discovery, fallback to localhost for local testing
PRODUCT_SERVICE_URL = os.getenv("PRODUCT_SERVICE_URL", "http://product-service:5001")
PAYMENT_SERVICE_URL = os.getenv("PAYMENT_SERVICE_URL", "http://payment-service:5003")

cart = []

@app.route("/")
def home():
    return jsonify({"service": "Cart Service Running"}), 200


@app.route("/cart", methods=["GET"])
def get_cart():
    return jsonify(cart), 200


@app.route("/cart", methods=["POST"])
def add_to_cart():
    data = request.get_json()
    product_id = data.get("product_id")

    res = requests.get(f"{PRODUCT_SERVICE_URL}/products/{product_id}")

    if res.status_code != 200:
        return jsonify({"error": "Product not found"}), 404

    product = res.json()
    cart.append(product)

    return jsonify({"message": "Added to cart", "product": product}), 201


@app.route("/cart/<int:item_id>", methods=["DELETE"])
def remove_from_cart(item_id):
    global cart
    if 0 <= item_id < len(cart):
        removed_item = cart.pop(item_id)
        return jsonify({"message": "Removed from cart", "item": removed_item}), 200
    return jsonify({"error": "Item not found in cart"}), 404


@app.route("/checkout", methods=["POST"])
def checkout():
    if not cart:
        return jsonify({"error": "Cart is empty"}), 400

    total_amount = sum(item.get("price", 0) for item in cart)
    
    try:
        payment_response = requests.post(
            f"{PAYMENT_SERVICE_URL}/checkout",
            json={"amount": total_amount, "items": cart},
            timeout=10
        )
        
        if payment_response.status_code == 200:
            payment_data = payment_response.json()
            cart_data = cart.copy()
            cart.clear()
            return jsonify({
                "status": "SUCCESS",
                "message": "Order completed",
                "order": {
                    "items": cart_data,
                    "total_amount": total_amount,
                    "payment_status": payment_data.get("status")
                }
            }), 200
        else:
            return jsonify({
                "status": "FAILED",
                "message": "Payment failed",
                "error": payment_response.json()
            }), 400
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Payment service unavailable: {str(e)}"}), 503


@app.route("/health")
def health():
    return jsonify({"status": "UP"}), 200


# ✅ RUN APP
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
