# from flask import Blueprint, request, jsonify
# from app.mongo import mongo
# from datetime import datetime

# user_bp = Blueprint('user_bp', __name__)

# @user_bp.route('/register', methods=['POST'])
# def register_user():
#     data = request.json
#     username = data.get('username')
#     email = data.get('email')
#     password = data.get('password')  # Assume password is hashed before being sent

#     if not username or not email or not password:
#         return jsonify({'error': 'Missing required fields'}), 400

#     # Insert user into the database
#     mongo.db.users.insert_one({
#         'username': username,
#         'email': email,
#         'password_hash': password,  # Store hashed password
#         'created_at': datetime.utcnow(),
#         'last_login': None,
#         'is_active': True,
#         'is_admin': False
#     })

#     return jsonify({'message': 'User registered successfully'}), 201
