from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
socketio = SocketIO()

def create_app(config_object=None):
    """Application factory pattern"""
    app = Flask(__name__)
    
    # Load configuration
    if config_object:
        app.config.from_object(config_object)
    else:
        # Default to using config.py
        from config import get_config
        app.config.from_object(get_config())
    
    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    
    # Setup CORS
    CORS(app, resources={r"/api/*": {"origins": "*", "supports_credentials": True, "allow_headers": ["Content-Type", "Authorization"]}}, expose_headers=["Authorization"])
    
    # Health check endpoint
    @app.route('/api/health')
    def health_check():
        return jsonify({"status": "healthy", "message": "Service is running"}), 200
    
    # Initialize SocketIO
    socketio.init_app(app, cors_allowed_origins="*", async_mode='gevent')
    
    # Register blueprints
    from app.api.auth import auth_bp
    from app.api.users import users_bp
    from app.api.locations import locations_bp
    from app.api.admin import admin_bp
    
    # Add a debug endpoint to print headers
    @app.route('/api/debug/headers')
    def debug_headers():
        headers = {k: v for k, v in request.headers.items()}
        token = request.headers.get('Authorization', 'No Authorization header')
        return jsonify({
            'headers': headers,
            'token': token
        })
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(users_bp, url_prefix='/api/users')
    app.register_blueprint(locations_bp, url_prefix='/api/locations')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    
    # Setup socket.io events
    from app.sockets import register_socket_events
    register_socket_events(socketio)
    
    # Create database tables if they don't exist (development only)
    with app.app_context():
        db.create_all()
    
    return app
