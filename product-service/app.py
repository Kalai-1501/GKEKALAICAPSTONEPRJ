from flask import Flask, jsonify
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

products = [
    {"id": 1, "name": "Laptop", "price": 80000},
    {"id": 2, "name": "Phone", "price": 30000},
    {"id": 3, "name": "Headphones", "price": 2000}
]

@app.route("/")
def home():
    return jsonify({"service": "Product Service Running"}), 200

@app.route("/products", methods=["GET"])
def get_products():
    return jsonify(products), 200

@app.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    for product in products:
        if product["id"] == product_id:
            return jsonify(product), 200
    return jsonify({"error": "Product not found"}), 404

@app.route("/health")
def health():
    return jsonify({"status": "UP"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
