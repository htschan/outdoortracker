import bcrypt
from datetime import datetime
from app import create_app, db
from app.models.user import User

app = create_app()
with app.app_context():
    # Check if admin user already exists
    if User.query.filter_by(email="outdoortracker@sorawit.ch").first():
        print("Admin user already exists!")
    else:
        # Hash password
        password_hash = bcrypt.hashpw("Axil&311".encode('utf-8'), bcrypt.gensalt())
        
        # Create admin user
        admin_user = User(
            name="admin",
            email="outdoortracker@sorawit.ch",
            password=password_hash.decode('utf-8'),
            role='admin',
            is_active=True,
            is_verified=True,
            is_approved=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        # Save to database
        db.session.add(admin_user)
        db.session.commit()
        print("Admin user created successfully!")

    # Check for test user and create if needed
    if not User.query.filter_by(email="user@outdoortracker.com").first():
        # Hash password
        password_hash = bcrypt.hashpw("user123".encode('utf-8'), bcrypt.gensalt())
        
        # Create regular user
        test_user = User(
            name="Test User",
            email="user@outdoortracker.com",
            password=password_hash.decode('utf-8'),
            role='user',
            is_active=True,
            is_verified=True,
            is_approved=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        # Save to database
        db.session.add(test_user)
        db.session.commit()
        print("Test user created successfully!")
    else:
        print("Test user already exists!")
