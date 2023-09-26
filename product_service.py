# Maisha Mahmood
# CMSC 455 - Product Service

from flask import Flask, request, jsonify

app = Flask(__name__)

products_list = [
    {"id": 1, "name": "Milk", "price": 0.6, "quantity": 100},
    {"id": 2, "name": "Eggs", "price": 0.2, "quantity": 160},
    {"id": 3, "name": "Bread", "price": 0.3, "quantity": 100},
    {"id": 4, "name": "Yogurt", "price": 0.35, "quantity": 150},
]

#Gets all the products
@app.route('/products', methods=['GET'])
def get_products():
    return jsonify(products_list)

#Gets one specific product with the ID
@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = next((x for x in products_list if x["id"] == product_id), None)
    if product:
        return jsonify(product)
    else:
        return jsonify({"Error": "Product was not found"}), 404

#Adds a new product to the list
@app.route('/products', methods=['POST'])
def add_product():
    products_data = request.get_json()
    if "name" in products_data and "price" in products_data and "quantity" in products_data:
        added_product = {
            "id": len(products_list) + 1,
            "name": products_data["name"],
            "price": products_data["price"],
            "quantity": products_data["quantity"],
        }
        products_list.append(added_product)
        return jsonify({"message": "Product was added successfully!"}), 201
    else:
        return jsonify({"Error": "Invalid data."}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5050)
