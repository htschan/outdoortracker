from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError

from app.models.location import Location, LocationSchema
from app.models.user import User
from app import db, socketio

locations_bp = Blueprint('locations', __name__)

@locations_bp.route('', methods=['POST'])
@jwt_required()
def add_location():
    """Add a new location for the current user"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'message': 'User not found'}), 404
        
        # Parse location data
        data = request.json
        lat = data.get('lat')
        lng = data.get('lng')
        accuracy = data.get('accuracy')
        altitude = data.get('altitude')
        speed = data.get('speed')
        heading = data.get('heading')
        
        # Create new location
        new_location = Location(
            user_id=user_id,
            latitude=lat,
            longitude=lng,
            accuracy=accuracy,
            altitude=altitude,
            speed=speed,
            heading=heading
        )
        
        # Save to database
        db.session.add(new_location)
        db.session.commit()
        
        # Update user status to active
        if not user.is_active:
            user.is_active = True
            db.session.commit()
        
        # Emit location update via SocketIO
        socketio.emit('location_update', {
            'userId': user_id,
            'lat': lat,
            'lng': lng,
            'accuracy': accuracy,
            'timestamp': new_location.timestamp.isoformat()
        })
        
        return jsonify({'message': 'Location updated successfully'}), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to update location', 'error': str(e)}), 500


@locations_bp.route('/user/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user_locations(user_id):
    """Get location history for a specific user"""
    try:
        # Pagination parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 100, type=int)
        
        # Get locations with pagination
        locations = Location.query.filter_by(user_id=user_id)\
            .order_by(Location.timestamp.desc())\
            .paginate(page=page, per_page=per_page, error_out=False)
        
        schema = LocationSchema(many=True)
        result = {
            'locations': schema.dump(locations.items),
            'total': locations.total,
            'pages': locations.pages,
            'current_page': page
        }
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'message': 'Failed to fetch locations', 'error': str(e)}), 500


@locations_bp.route('/latest/<int:user_id>', methods=['GET'])
@jwt_required()
def get_latest_location(user_id):
    """Get the latest location for a specific user"""
    try:
        location = Location.query.filter_by(user_id=user_id)\
            .order_by(Location.timestamp.desc())\
            .first()
        
        if not location:
            return jsonify({'message': 'No locations found for this user'}), 404
        
        schema = LocationSchema()
        result = schema.dump(location)
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'message': 'Failed to fetch location', 'error': str(e)}), 500
