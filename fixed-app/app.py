from flask import Flask, request, jsonify
from database import get_user, create_user
from utils import format_response, calculate_discount

app = Flask(__name__)

@app.route('/user/<id>', methods=['GET'])
def get_user_route(id):
    try:
        user = get_user(int(id))  # Convert to int for safety
        if not user:
            return jsonify({'error': 'User not found'}), 404
        return jsonify(user)
    except (ValueError, DatabaseError) as e:
        return jsonify({'error': str(e)}), 404

@app.route('/user', methods=['POST'])
def create_user_route():
    try:
        data = request.json
        if not isinstance(data, dict):
            return jsonify({'error': 'Request body must be an object'}), 400

        username = data.get('username')
        email = data.get('email')

        if not username or not email:
            return jsonify({'error': 'Username and email are required'}), 400

        result = create_user(username, email)
        return jsonify(result)
    except (ValueError, DatabaseError) as e:
        return jsonify({'error': str(e)}), 500

@app.route('/discount', methods=['GET'])
def discount_route():
    try:
        price = request.args.get('price')
        if not price:
            return jsonify({'error': 'Price parameter is required'}), 400

        # Parse discount rate from query string (e.g., ?discount=10)
        discount_str = request.args.get('discount', '')
        try:
            discount_rate = float(discount_str) if discount_str else 0.1
        except ValueError:
            return jsonify({'error': 'Discount rate must be a number'}), 400

        # Validate discount rate is between 0 and 1
        if not (0 <= discount_rate <= 1):
            return jsonify({'error': 'Discount rate must be between 0 and 1'}), 400

        response = format_response(discount)
        return jsonify(response)
    except DatabaseError as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)