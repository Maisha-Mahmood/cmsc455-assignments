
from flask import Flask, jsonify
import requests

app = Flask(__name__)

PRODUCT_SERVICE_URL = 'https://product-service-ugfo.onrender.com'  
@app.route('/cart/<int:user_id>', methods=['GET'])
def get_cart(user_id):
    response = requests.get(f'{PRODUCT_SERVICE_URL}/products/{user_id}')
    if response.status_code == 200:
        products = response.json()
        return jsonify({'user_id': user_id, 'cart': []}) 
    else:
        return jsonify({'message': 'Failed to retrieve cart'}), 500

@app.route('/cart/<int:user_id>/add/<int:product_id>', methods=['POST'])
def add_to_cart(user_id, product_id):
    response = requests.get(f'{PRODUCT_SERVICE_URL}/products/{product_id}')
    if response.status_code == 200:
        product_data = response.json()
        return jsonify({'message': 'Product added to cart'}), 201 
    else:
        return jsonify({'message': 'Failed to add product to cart'}), 500

@app.route('/cart/<int:user_id>/remove/<int:product_id>', methods=['POST'])
def remove_from_cart(user_id, product_id):
    return jsonify({'message': 'Product removed from cart'}), 200  
if __name__ == '__main__':
    app.run(debug=True)