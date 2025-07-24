from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from marshmallow import ValidationError
import datetime
import secrets
import bcrypt

from app.models.user import User, UserSchema
from app import db
from app.services.email import send_verification_email

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    try:
        # Load and validate user data
        schema = UserSchema()
        user_data = schema.load(request.json)
        
        # Check if email already exists
        if User.query.filter_by(email=user_data['email']).first():
            return jsonify({'message': 'Email already registered'}), 409
        
        # Hash password
        password_hash = bcrypt.hashpw(user_data['password'].encode('utf-8'), bcrypt.gensalt())
        
        # Generate verification token
        verification_token = secrets.token_urlsafe(32)
        token_expiry = datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        
        # Create new user
        new_user = User(
            name=user_data['name'],
            email=user_data['email'],
            password=password_hash.decode('utf-8'),
            role='user',  # Default role
            is_active=False,  # Inactive until verified and approved
            is_verified=False,  # Not verified yet
            is_approved=False,  # Not approved yet
            verification_token=verification_token,
            token_expiry=token_expiry
        )
        
        # Save to database
        db.session.add(new_user)
        db.session.commit()
        
        # Send verification email
        send_verification_email(new_user.email, verification_token)
        
        return jsonify({'message': 'Registration successful. Please check your email to verify your account.'}), 201
        
    except ValidationError as err:
        return jsonify({'message': 'Validation error', 'errors': err.messages}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Registration failed', 'error': str(e)}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """Authenticate user and return token"""
    try:
        # Get credentials
        email = request.json.get('email', None)
        password = request.json.get('password', None)
        
        # Find user
        user = User.query.filter_by(email=email).first()
        
        # Check if user exists and password is correct
        if not user or not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            return jsonify({'message': 'Invalid email or password'}), 401
        
        # Check if user is verified
        if not user.is_verified:
            return jsonify({'message': 'Email not verified. Please check your inbox.'}), 401
        
        # Check if user is approved
        if not user.is_approved:
            return jsonify({'message': 'Your account is pending admin approval.'}), 401
        
        # Create access token - convert user ID to string to avoid JWT issues
        access_token = create_access_token(
            identity=str(user.id),  # Convert to string to ensure compatibility
            additional_claims={'role': user.role}
        )
        
        return jsonify({'token': access_token, 'role': user.role}), 200
        
    except Exception as e:
        return jsonify({'message': 'Login failed', 'error': str(e)}), 500


@auth_bp.route('/test-token', methods=['GET'])
@jwt_required()
def test_token():
    """Test endpoint for JWT token verification"""
    try:
        # Get the JWT identity
        user_id = get_jwt_identity()
        claims = get_jwt()
        
        return jsonify({
            'message': 'Token is valid',
            'user_id': user_id,
            'claims': claims
        }), 200
    except Exception as e:
        return jsonify({'message': 'Token validation failed', 'error': str(e)}), 401

@auth_bp.route('/verify-email', methods=['POST'])
def verify_email():
    """Verify user email with token"""
    try:
        token = request.json.get('token', None)
        
        if not token:
            return jsonify({'message': 'No verification token provided'}), 400
        
        # Find user with this token
        user = User.query.filter_by(verification_token=token).first()
        
        if not user:
            return jsonify({'message': 'Invalid verification token'}), 400
        
        # Check if token has expired
        if user.token_expiry < datetime.datetime.utcnow():
            return jsonify({'message': 'Verification token has expired'}), 400
        
        # Mark user as verified
        user.is_verified = True
        user.verification_token = None
        user.token_expiry = None
        
        db.session.commit()
        
        return jsonify({'message': 'Email verified successfully. Your account is now pending admin approval.'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Email verification failed', 'error': str(e)}), 500
