from flask import Flask, request, jsonify
from database import get_user, create_user
from utils import format_response, calculate_discount

app = Flask(__name__)

@app.route('/user/<id>', methods=['GET'])
def get_user_route(id):
    user = get_user(id)
    return jsonify(user)

@app.route('/user', methods=['POST'])
def create_user_route():
    data = request.json
    username = data['username']
    email = data['email']
    result = create_user(username, email)
    return jsonify(result)

@app.route('/discount', methods=['GET'])
def discount_route():
    price = request.args.get('price')
    discount = calculate_discount(price, 0.1)
    response = format_response(discount)
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)