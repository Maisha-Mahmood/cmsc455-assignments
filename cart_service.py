# Maisha Mahmood
# CMSC 455 - Cart Service

from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

PRODUCT_URL = 'https://product-service-ugfo.onrender.com'

carts = {
    1: [  
        {
            "product_id": 1,
            "product_name": "Milk",
            "quantity": 3,
            "price": 0.6 
        },
        {
            "product_id": 2,
            "product_name": "Eggs",
            "quantity": 2,
            "price": 0.2 
        },
    ],
    2: [  
        {
            "product_id": 1,
            "product_name": "Milk",
            "quantity": 1,
            "price": 0.6 
        },
        {
            "product_id": 3,
            "product_name": "Bread",
            "quantity": 2,
            "price": 0.6 
        },
    ],
}

#Gets cart information for a specific user based on the user id
@app.route('/cart/<int:user_id>', methods=['GET'])
def get_cart(user_id):
    response = requests.get(f'{PRODUCT_URL}/products/{user_id}')
    
    if response.status_code == 200:
        cart_contents = response.json()
        return jsonify({'user_id': user_id, 'cart': cart_contents})
    else:
        return jsonify({'Error': 'Failed to get cart info'}), 500

#Adds a new product to the user's cart
@app.route('/cart/<int:user_id>/add/<int:product_id>', methods=['POST'])
def add_to_cart(user_id, product_id):
    products_data = request.get_json()
    
    if not products_data or "quantity" not in products_data:
        return jsonify({"Error": "Invalid data."}), 400
    
    amount = products_data["quantity"]
    response = requests.get(f'{PRODUCT_URL}/products/{product_id}')
    
    if response.status_code == 200:
        products_data = response.json()
        products_name = products_data.get("name")
        products_price = products_data.get("price")
        
        # Create or update the user's cart
        if user_id not in carts:
            carts[user_id] = []
        
        cart_products = {
            "product_id": product_id,
            "product_name": products_name,
            "quantity": amount,
            "total_price": amount * products_price
        }
        
        carts[user_id].append(cart_products)
        
        return jsonify({"message": f"{amount} {products_name}(s) sucessfully added to the cart"}), 201
    else:
        return jsonify({"Error": "Product was not found"}), 404

#Removes a certain product from the cart.
@app.route('/cart/<int:user_id>/remove/<int:product_id>', methods=['POST'])
def remove_from_cart(user_id, product_id):
    products_data = request.get_json()
    
    if not products_data or "quantity" not in products_data:
        return jsonify({"Error": "Invalid data."}), 400
    
    amount_removing = products_data["quantity"]
    
    if user_id not in carts:
        return jsonify({"message": "Cart not found"}), 404
    
    cart = carts[user_id]
    
    for i in cart:
        if i["product_id"] == product_id:
            if i["quantity"] <= amount_removing:
                cart.remove(i)
                return jsonify({"message": f"{i['product_name']} removed from the cart"}), 200
            else:
                i["quantity"] -= amount_removing
                i["total_price"] -= amount_removing * (i["total_price"] / i["quantity"])
                return jsonify({"message": f"{amount_removing} {i['product_name']}(s) succesfully removed from the cart"}), 200
    
    return jsonify({"Error": "Product was not found in the cart"}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5055)
