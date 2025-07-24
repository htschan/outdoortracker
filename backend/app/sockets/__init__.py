from flask import request
from flask_socketio import emit, join_room, leave_room, disconnect
from flask_jwt_extended import decode_token
from jwt.exceptions import InvalidTokenError

from app.models.user import User
from app import db

def register_socket_events(socketio):
    @socketio.on('connect')
    def handle_connect():
        """Handle new WebSocket connection"""
        try:
            # Get token from the connection's auth param
            token = request.args.get('token') or getattr(request, 'auth', {}).get('token')
            
            if not token:
                return False  # Reject connection
            
            # Verify token and get user ID
            decoded_token = decode_token(token)
            user_id = decoded_token['sub']
            
            # Update user's active status
            user = User.query.get(user_id)
            if user:
                user.is_active = True
                db.session.commit()
                
                # Join a room specific to this user
                join_room(f'user_{user_id}')
                
                # Join the broadcast room for all users
                join_room('all_users')
                
                return True  # Accept connection
            
            return False  # Reject connection if user not found
            
        except InvalidTokenError:
            return False  # Reject connection on invalid token
        except Exception as e:
            print(f"Socket connection error: {str(e)}")
            return False
    
    
    @socketio.on('disconnect')
    def handle_disconnect():
        """Handle WebSocket disconnection"""
        try:
            # Get token from the connection's auth param
            token = request.args.get('token') or getattr(request, 'auth', {}).get('token')
            
            if token:
                # Verify token and get user ID
                decoded_token = decode_token(token)
                user_id = decoded_token['sub']
                
                # Update user's active status
                user = User.query.get(user_id)
                if user:
                    user.is_active = False
                    db.session.commit()
                    
                    # Leave rooms
                    leave_room(f'user_{user_id}')
                    leave_room('all_users')
        except Exception:
            pass  # Silently handle errors on disconnect
    
    
    @socketio.on('update_location')
    def handle_location_update(data):
        """Handle location update from client"""
        try:
            # Get token from the connection's auth param
            token = request.args.get('token') or getattr(request, 'auth', {}).get('token')
            
            if not token:
                disconnect()  # Disconnect if no token
                return
            
            # Verify token and get user ID
            decoded_token = decode_token(token)
            user_id = decoded_token['sub']
            
            # Prepare the location data
            location_data = {
                'userId': user_id,
                'lat': data.get('lat'),
                'lng': data.get('lng'),
                'accuracy': data.get('accuracy'),
                'timestamp': data.get('timestamp')
            }
            
            # Broadcast to all connected clients
            emit('location_update', location_data, room='all_users', include_self=False)
            
        except InvalidTokenError:
            disconnect()  # Disconnect on invalid token
        except Exception as e:
            print(f"Socket location update error: {str(e)}")
            disconnect()
