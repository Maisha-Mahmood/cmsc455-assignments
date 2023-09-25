from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Sample in-memory shopping cart data (replace with a database in a real application)
carts = {}


@app.route('/cart/<int:user_id>', methods=['GET'])
def get_cart(user_id):
    if user_id not in carts:
        return jsonify({"user_id": user_id, "cart": []})

    return jsonify(carts[user_id])


@app.route('/cart/<int:user_id>/add/<int:product_id>', methods=['POST'])
def add_to_cart(user_id, product_id):
    data = request.get_json()
    if not data or "quantity" not in data:
        return jsonify({"message": "Invalid data. Make sure to include 'quantity' in the request body."}), 400

    quantity = data["quantity"]

    # Simulate interaction with the Product Service to get product details (replace with actual code)
    product_details = get_product_details(product_id)

    if not product_details:
        return jsonify({"message": "Product not found"}), 404

    product_name = product_details.get("name")
    product_price = product_details.get("price")

    # Create or update the user's cart
    if user_id not in carts:
        carts[user_id] = []

    cart_item = {
        "product_id": product_id,
        "product_name": product_name,
        "quantity": quantity,
        "total_price": quantity * product_price
    }

    carts[user_id].append(cart_item)

    return jsonify({"message": f"{quantity} {product_name}(s) added to the cart"}), 201


@app.route('/cart/<int:user_id>/remove/<int:product_id>', methods=['POST'])
def remove_from_cart(user_id, product_id):
    data = request.get_json()
    if not data or "quantity" not in data:
        return jsonify({"message": "Invalid data. Make sure to include 'quantity' in the request body."}), 400

    quantity_to_remove = data["quantity"]

    if user_id not in carts:
        return jsonify({"message": "Cart not found"}), 404

    cart = carts[user_id]

    for item in cart:
        if item["product_id"] == product_id:
            if item["quantity"] <= quantity_to_remove:
                cart.remove(item)
                return jsonify({"message": f"{item['product_name']} removed from the cart"}), 200
            else:
                item["quantity"] -= quantity_to_remove
                item["total_price"] -= quantity_to_remove * item["total_price"]
                return jsonify({"message": f"{quantity_to_remove} {item['product_name']}(s) removed from the cart"}), 200

    return jsonify({"message": "Product not found in the cart"}), 404


# Simulated function to get product details (replace with actual code to call the Product Service)
def get_product_details(product_id):
    product_service_url = "https://product-service-ugfo.onrender.com"
    response = requests.get(f"{product_service_url}/products/{product_id}")
    if response.status_code == 200:
        return response.json()
    else:
        return None

if __name__ == '__main__':
    app.run(debug=True, port=5055)
