from flask import Flask, render_template, request, jsonify
import requests
import os
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# Use Kubernetes DNS for service discovery
CART_SERVICE_URL = os.getenv("CART_SERVICE_URL", "http://cart-service:5002")
PRODUCT_SERVICE_URL = os.getenv("PRODUCT_SERVICE_URL", "http://product-service:5001")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/products", methods=["GET"])
def get_products():
    try:
        response = requests.get(f"{PRODUCT_SERVICE_URL}/products", timeout=5)
        if response.status_code == 200:
            return jsonify(response.json()), 200
        return jsonify({"error": "Product service error"}), 500
    except requests.exceptions.RequestException as e:
        logging.error(f"Error connecting to product service: {str(e)}")
        return jsonify({"error": "Product service unavailable"}), 503

@app.route("/api/cart", methods=["GET"])
def get_cart():
    try:
        response = requests.get(f"{CART_SERVICE_URL}/cart", timeout=5)
        if response.status_code == 200:
            return jsonify(response.json()), 200
        return jsonify({"error": "Cart service error"}), 500
    except requests.exceptions.RequestException as e:
        logging.error(f"Error connecting to cart service: {str(e)}")
        return jsonify({"error": "Cart service unavailable"}), 503

@app.route("/api/cart", methods=["POST"])
def add_to_cart():
    data = request.get_json()
    product_id = data.get("product_id")
    
    if not product_id:
        return jsonify({"error": "product_id is required"}), 400
    
    try:
        response = requests.post(
            f"{CART_SERVICE_URL}/cart",
            json={"product_id": product_id},
            timeout=5
        )
        if response.status_code in [200, 201]:
            return jsonify(response.json()), 201
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        logging.error(f"Error connecting to cart service: {str(e)}")
        return jsonify({"error": "Cart service unavailable"}), 503

@app.route("/api/cart/<int:item_id>", methods=["DELETE"])
def remove_from_cart(item_id):
    try:
        response = requests.delete(
            f"{CART_SERVICE_URL}/cart/{item_id}",
            timeout=5
        )
        if response.status_code == 200:
            return jsonify(response.json()), 200
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        logging.error(f"Error connecting to cart service: {str(e)}")
        return jsonify({"error": "Cart service unavailable"}), 503

@app.route("/api/checkout", methods=["POST"])
def checkout():
    try:
        response = requests.post(
            f"{CART_SERVICE_URL}/checkout",
            timeout=10
        )
        if response.status_code == 200:
            return jsonify(response.json()), 200
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        logging.error(f"Error during checkout: {str(e)}")
        return jsonify({"error": "Checkout failed - service unavailable"}), 503

@app.route("/health")
def health():
    return jsonify({"status": "UP", "service": "UI Service"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
