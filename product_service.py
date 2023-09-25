from flask import Flask, request, jsonify

app = Flask(__name__)

products = [
    {"id": 1, "name": "Milk", "price": 0.6, "quantity": 100},
    {"id": 2, "name": "Eggs", "price": 0.2, "quantity": 160},
    {"id": 3, "name": "Bread", "price": 0.3, "quantity": 100},
]

@app.route('/products', methods=['GET'])
def get_products():
    return jsonify(products)

@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = next((p for p in products if p["id"] == product_id), None)
    if product:
        return jsonify(product)
    else:
        return jsonify({"message": "Product not found"}), 404

@app.route('/products', methods=['POST'])
def add_product():
    data = request.get_json()
    if "name" in data and "price" in data and "quantity" in data:
        new_product = {
            "id": len(products) + 1,
            "name": data["name"],
            "price": data["price"],
            "quantity": data["quantity"],
        }
        products.append(new_product)
        return jsonify({"message": "Product added successfully"}), 201
    else:
        return jsonify({"message": "Invalid data. Make sure to include name, price, and quantity."}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5050)
