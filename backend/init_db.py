import bcrypt
from datetime import datetime
from app import create_app, db
from app.models.user import User
import getpass

app = create_app()
with app.app_context():
    # Prompt for admin credentials
    print("\n=== Admin User Setup ===")
    while True:
        admin_email = input("Admin email: ").strip()
        if admin_email:
            break
        print("Admin email cannot be empty!")
    admin_name = input("Admin name [admin]: ") or "admin"
    admin_password = getpass.getpass("Admin password: ")
    if not admin_password:
        print("Password cannot be empty!")
        exit(1)

    # Check if admin user already exists
    if User.query.filter_by(email=admin_email).first():
        print("Admin user already exists!")
    else:
        # Hash password
        password_hash = bcrypt.hashpw(admin_password.encode('utf-8'), bcrypt.gensalt())
        # Create admin user
        admin_user = User(
            name=admin_name,
            email=admin_email,
            password=password_hash.decode('utf-8'),
            role='admin',
            is_active=True,
            is_verified=True,
            is_approved=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.session.add(admin_user)
        db.session.commit()
        print("Admin user created successfully!")

    # Prompt for test user credentials
    print("\n=== Test User Setup ===")
    test_email = input("Test user email [user@outdoortracker.com]: ") or "user@outdoortracker.com"
    test_name = input("Test user name [Test User]: ") or "Test User"
    test_password = getpass.getpass("Test user password: ")
    if not test_password:
        print("Password cannot be empty!")
        exit(1)

    # Check for test user and create if needed
    if not User.query.filter_by(email=test_email).first():
        password_hash = bcrypt.hashpw(test_password.encode('utf-8'), bcrypt.gensalt())
        test_user = User(
            name=test_name,
            email=test_email,
            password=password_hash.decode('utf-8'),
            role='user',
            is_active=True,
            is_verified=True,
            is_approved=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.session.add(test_user)
        db.session.commit()
        print("Test user created successfully!")
    else:
        print("Test user already exists!")
