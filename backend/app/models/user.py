from datetime import datetime
from marshmallow import Schema, fields, validate
from app import db

class User(db.Model):
    """User model for storing user related details"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='user')  # 'user' or 'admin'
    is_active = db.Column(db.Boolean, default=False)
    is_verified = db.Column(db.Boolean, default=False)
    is_approved = db.Column(db.Boolean, default=False)
    verification_token = db.Column(db.String(100), nullable=True)
    token_expiry = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Define relationship with locations
    locations = db.relationship('Location', backref='user', lazy=True)
    
    def __repr__(self):
        return f'<User {self.email}>'


class UserSchema(Schema):
    """Schema for serializing/deserializing User objects"""
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=8), load_only=True)
    role = fields.Str(validate=validate.OneOf(['user', 'admin']), dump_only=True)
    is_active = fields.Bool(dump_only=True)
    is_verified = fields.Bool(dump_only=True)
    is_approved = fields.Bool(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
