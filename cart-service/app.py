from flask import Flask, jsonify, request
import requests

# ✅ CREATE APP FIRST
app = Flask(__name__)

PRODUCT_SERVICE_URL = "http://host.docker.internal:5001"

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

    return jsonify({"message": "Added to cart"}), 201


@app.route("/health")
def health():
    return jsonify({"status": "UP"}), 200


# ✅ RUN APP
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
