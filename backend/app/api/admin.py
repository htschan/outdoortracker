from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt
from marshmallow import ValidationError

from app.models.user import User, UserSchema
from app import db

admin_bp = Blueprint('admin', __name__)

def require_admin(fn):
    """Decorator to check if user is admin"""
    def wrapper(*args, **kwargs):
        # Check if user is admin
        claims = get_jwt()
        if claims.get('role') != 'admin':
            return jsonify({'message': 'Unauthorized access. Admin rights required.'}), 403
        return fn(*args, **kwargs)
    wrapper.__name__ = fn.__name__
    return wrapper

@admin_bp.route('/users', methods=['GET'])
@jwt_required()
@require_admin
def get_all_users():
    """Get all users with detailed information"""
    try:
        users = User.query.all()
        schema = UserSchema(many=True)
        result = schema.dump(users)
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'message': 'Failed to fetch users', 'error': str(e)}), 500

@admin_bp.route('/users/<int:user_id>/approve', methods=['PUT'])
@jwt_required()
@require_admin
def approve_user(user_id):
    """Approve a pending user"""
    try:
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'message': 'User not found'}), 404
        
        user.is_approved = True
        db.session.commit()
        
        return jsonify({
            'message': f'User {user.email} approved successfully',
            'user': UserSchema().dump(user)
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to approve user', 'error': str(e)}), 500

@admin_bp.route('/users/<int:user_id>/toggle-active', methods=['PUT'])
@jwt_required()
@require_admin
def toggle_active(user_id):
    """Activate or deactivate a user"""
    try:
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'message': 'User not found'}), 404
        
        # Toggle active status
        user.is_active = not user.is_active
        db.session.commit()
        
        status = "activated" if user.is_active else "deactivated"
        
        return jsonify({
            'message': f'User {user.email} {status} successfully',
            'user': UserSchema().dump(user)
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Failed to toggle active status', 'error': str(e)}), 500

@admin_bp.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
@require_admin
def delete_user(user_id):
    """Delete a user"""
    try:
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'message': 'User not found'}), 404
        
        email = user.email
        
        # Delete all related records like locations
        db.session.delete(user)
        db.session.commit()
        
        return jsonify({'message': f'User {email} deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to delete user', 'error': str(e)}), 500
