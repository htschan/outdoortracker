from datetime import datetime
from marshmallow import Schema, fields
from app import db

class Location(db.Model):
    """Location model for storing user location data"""
    __tablename__ = 'locations'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    altitude = db.Column(db.Float, nullable=True)
    accuracy = db.Column(db.Float, nullable=True)
    speed = db.Column(db.Float, nullable=True)
    heading = db.Column(db.Float, nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Location {self.id}: ({self.latitude}, {self.longitude})>'


class LocationSchema(Schema):
    """Schema for serializing/deserializing Location objects"""
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    latitude = fields.Float(required=True)
    longitude = fields.Float(required=True)
    altitude = fields.Float()
    accuracy = fields.Float()
    speed = fields.Float()
    heading = fields.Float()
    timestamp = fields.DateTime()
