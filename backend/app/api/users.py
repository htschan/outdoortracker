from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from marshmallow import ValidationError

from app.models.user import User, UserSchema
from app import db

users_bp = Blueprint('users', __name__)

@users_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Get current user details"""
    try:
        # Debug: Print request headers
        print("Request headers:", request.headers)
        
        # Debug: Get and print JWT token
        token = request.headers.get('Authorization')
        print("Auth header:", token)
        
        user_id = get_jwt_identity()
        print("Decoded user ID:", user_id)
        
        # Convert string ID back to integer if needed
        try:
            user_id_int = int(user_id)
            user = User.query.get(user_id_int)
        except (ValueError, TypeError):
            return jsonify({'message': 'Invalid user ID format'}), 400
        
        if not user:
            return jsonify({'message': 'User not found'}), 404
        
        schema = UserSchema()
        result = schema.dump(user)
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'message': 'Failed to fetch user details', 'error': str(e)}), 500


@users_bp.route('/active', methods=['GET'])
@jwt_required()
def get_active_users():
    """Get list of active users (for the map view)"""
    try:
        # Get all active users except the current user
        current_user_id = get_jwt_identity()
        active_users = User.query.filter(
            User.is_active == True,
            User.id != current_user_id
        ).all()
        
        schema = UserSchema(many=True)
        result = schema.dump(active_users)
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'message': 'Failed to fetch active users', 'error': str(e)}), 500


@users_bp.route('/', methods=['GET'])
@jwt_required()
def get_all_users():
    """Admin only: Get all users"""
    try:
        # Check if user is admin
        claims = get_jwt()
        if claims.get('role') != 'admin':
            return jsonify({'message': 'Unauthorized access'}), 403
        
        users = User.query.all()
        schema = UserSchema(many=True)
        result = schema.dump(users)
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'message': 'Failed to fetch users', 'error': str(e)}), 500


@users_bp.route('/approve/<int:user_id>', methods=['PUT'])
@jwt_required()
def approve_user(user_id):
    """Admin only: Approve a pending user"""
    try:
        # Check if user is admin
        claims = get_jwt()
        if claims.get('role') != 'admin':
            return jsonify({'message': 'Unauthorized access'}), 403
        
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'message': 'User not found'}), 404
        
        # Approve the user
        user.is_approved = True
        user.is_active = True
        
        db.session.commit()
        
        return jsonify({'message': f'User {user.email} approved successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to approve user', 'error': str(e)}), 500
