#!/bin/bash

# Setup script for Outdoor Tracker

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Print a colorful message
print_message() {
  echo -e "${GREEN}=== $1 ===${NC}"
}

# Print a warning
print_warning() {
  echo -e "${YELLOW}WARNING: $1${NC}"
}

# Print an error
print_error() {
  echo -e "${RED}ERROR: $1${NC}"
}

# Print information
print_info() {
  echo -e "${BLUE}INFO: $1${NC}"
}

# Print success message
print_success() {
  echo -e "${GREEN}${BOLD}SUCCESS: $1${NC}"
}

# Check if Docker is installed and running
check_docker() {
  print_message "Checking Docker installation"
  
  # Check if Docker is installed
  if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed. Please install Docker first."
    print_info "Visit https://docs.docker.com/get-docker/ for installation instructions."
    exit 1
  fi
  
  # Check if Docker Compose is installed
  if ! command -v docker-compose &> /dev/null; then
    print_error "Docker Compose is not installed. Please install Docker Compose first."
    print_info "Visit https://docs.docker.com/compose/install/ for installation instructions."
    exit 1
  fi
  
  # Check if Docker daemon is running
  if ! docker info &> /dev/null; then
    print_error "Docker daemon is not running. Please start Docker service."
    print_info "You can start Docker with: sudo systemctl start docker"
    exit 1
  fi
  
  print_success "Docker and Docker Compose are installed and running."
}

# Setup development environment
setup_dev() {
  print_message "Setting up development environment"
  
  # Create .env file if it doesn't exist
  if [ ! -f .env ]; then
    if [ ! -f .env.example ]; then
      print_error "No .env.example file found. Cannot create configuration."
      exit 1
    fi
    
    cp .env.example .env
    print_success "Created .env file from example."
    print_info "You may want to edit .env with your custom settings."
  else
    print_warning ".env file already exists. Skipping creation."
  fi
  
  # Check if frontend directory exists
  if [ ! -d "frontend" ]; then
    print_error "Frontend directory not found. Project structure may be corrupted."
    exit 1
  fi
  
  # Check if backend directory exists
  if [ ! -d "backend" ]; then
    print_error "Backend directory not found. Project structure may be corrupted."
    exit 1
  fi
  
  # Stop any running containers
  print_info "Stopping any existing containers..."
  docker-compose down
  
  # Build and start development containers
  print_message "Building and starting development containers"
  if ! docker-compose up -d --build; then
    print_error "Failed to build and start containers. Check docker-compose logs for details."
    print_info "You can view logs with: docker-compose logs"
    exit 1
  fi
  
  # Check if containers are running
  print_info "Checking container status..."
  sleep 5
  if [ "$(docker-compose ps -q | wc -l)" -lt 3 ]; then
    print_warning "Not all containers are running. There might be issues with the setup."
    print_info "Check container logs with: docker-compose logs"
  else
    print_success "All containers are running!"
  fi
  
  echo ""
  echo -e "${GREEN}${BOLD}Development setup complete!${NC}"
  echo -e "${BOLD}Frontend:${NC} http://localhost:8080"
  echo -e "${BOLD}Backend API:${NC} http://localhost:5000/api"
  echo ""
  print_info "You can view logs with: docker-compose logs -f"
}

# Setup production environment
setup_prod() {
  print_message "Setting up production environment"
  
  # Check if docker-compose.prod.yml exists
  if [ ! -f "docker-compose.prod.yml" ]; then
    print_error "docker-compose.prod.yml not found. Cannot deploy to production."
    exit 1
  fi
  
  # Check if swarm is initialized
  docker node ls &> /dev/null
  if [ $? -ne 0 ]; then
    print_message "Initializing Docker Swarm"
    
    # Check if we're running on a Synology device
    if grep -q Synology /etc/issue 2>/dev/null; then
      print_info "Detected Synology environment"
    fi
    
    # Initialize swarm with advertised address if specified
    read -p "Do you want to specify an advertised address for Docker Swarm? (y/n): " use_addr
    if [[ "$use_addr" == "y" || "$use_addr" == "Y" ]]; then
      read -p "Enter the advertised address (IP or hostname): " swarm_addr
      docker swarm init --advertise-addr "$swarm_addr"
    else
      docker swarm init
    fi
    
    if [ $? -ne 0 ]; then
      print_error "Failed to initialize Docker Swarm"
      exit 1
    fi
    
    print_success "Docker Swarm initialized successfully"
  else
    print_message "Docker Swarm already initialized"
  fi
  
  # Create .env.prod file if it doesn't exist
  if [ ! -f .env.prod ]; then
    if [ ! -f .env.example ]; then
      print_error "No .env.example file found. Cannot create configuration."
      exit 1
    fi
    
    cp .env.example .env.prod
    print_success "Created .env.prod file from example."
    print_warning "Please edit .env.prod with your production settings before continuing."
    
    # Open the file in the default editor if available
    if command -v nano &> /dev/null; then
      read -p "Do you want to edit .env.prod now? (y/n): " edit_now
      if [[ "$edit_now" == "y" || "$edit_now" == "Y" ]]; then
        nano .env.prod
      else
        read -p "Press enter to continue after editing .env.prod manually..."
      fi
    else
      read -p "Press enter to continue after editing .env.prod..."
    fi
  fi
  
  # Build production images
  print_message "Building production images"
  if ! docker-compose -f docker-compose.prod.yml build; then
    print_error "Failed to build production images"
    exit 1
  fi
  
  # Deploy the stack
  print_message "Deploying to Docker Swarm"
  if ! docker stack deploy -c docker-compose.prod.yml --with-registry-auth outdoortracker; then
    print_error "Failed to deploy stack"
    exit 1
  fi
  
  print_success "Stack deployed successfully"
  
  # Check stack services
  print_message "Checking stack services"
  docker stack services outdoortracker
  
  echo ""
  echo -e "${GREEN}${BOLD}Production setup complete!${NC}"
  echo -e "Your Outdoor Tracker application should now be accessible at:"
  echo -e "${BOLD}Frontend:${NC} http://your-server-ip:8080"
  echo -e "${BOLD}Backend API:${NC} http://your-server-ip:5000/api"
  echo ""
  print_info "You can view stack status with: docker stack services outdoortracker"
  print_info "You can view logs with: docker service logs outdoortracker_frontend"
}

# Check for project requirements
check_requirements() {
  print_message "Checking project requirements"
  
  # Check for docker-compose.yml
  if [ ! -f "docker-compose.yml" ]; then
    print_error "docker-compose.yml not found. Project structure may be corrupted."
    exit 1
  fi
  
  # Check for frontend and backend directories
  if [ ! -d "frontend" ] || [ ! -d "backend" ]; then
    print_error "Frontend or backend directory not found. Project structure may be corrupted."
    exit 1
  fi
  
  # Check for .env.example
  if [ ! -f ".env.example" ]; then
    print_error ".env.example not found. Cannot create configuration."
    exit 1
  fi
  
  print_success "All project requirements are met."
}

# Clean up development environment
cleanup_dev() {
  print_message "Cleaning up development environment"
  
  read -p "This will remove all containers and volumes. Are you sure? (y/n): " confirm
  if [[ "$confirm" != "y" && "$confirm" != "Y" ]]; then
    print_info "Cleanup canceled."
    return
  fi
  
  docker-compose down -v
  print_success "Development environment cleaned up."
}

# Initialize the development database with default data
init_database() {
  print_message "Initializing database with default data"

  # Check if backend container is running
  if ! docker-compose ps | grep -q "backend.*Up"; then
    print_error "Backend container is not running. Please set up the development environment first."
    read -p "Press Enter to return to the main menu..."
    return
  fi

  print_info "Creating default admin user..."
  
  # Ask for admin user details
  read -p "Enter admin email [admin@outdoortracker.com]: " admin_email
  admin_email=${admin_email:-admin@outdoortracker.com}
  
  read -p "Enter admin name [Administrator]: " admin_name
  admin_name=${admin_name:-Administrator}
  
  read -p "Enter admin password [admin123]: " admin_password
  admin_password=${admin_password:-admin123}

  # Generate Python script to create admin user
  cat > init_db.py << EOL
import bcrypt
from datetime import datetime
from app import create_app, db
from app.models.user import User

app = create_app()
with app.app_context():
    # Check if admin user already exists
    if User.query.filter_by(email="${admin_email}").first():
        print("Admin user already exists!")
    else:
        # Hash password
        password_hash = bcrypt.hashpw("${admin_password}".encode('utf-8'), bcrypt.gensalt())
        
        # Create admin user
        admin_user = User(
            name="${admin_name}",
            email="${admin_email}",
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
EOL

  # Copy the script to the backend container
  if ! docker cp init_db.py $(docker-compose ps -q backend):/app/; then
    print_error "Failed to copy initialization script to container."
    rm init_db.py
    read -p "Press Enter to return to the main menu..."
    return
  fi

  # Run the script inside the backend container
  if ! docker-compose exec backend python init_db.py; then
    print_error "Failed to initialize database."
    rm init_db.py
    read -p "Press Enter to return to the main menu..."
    return
  fi

  # Clean up the script file
  rm init_db.py

  print_success "Database initialized successfully!"
  print_info "Created admin user with email: ${admin_email} and password: ${admin_password}"
  print_info "Created test user with email: user@outdoortracker.com and password: user123"
  
  read -p "Press Enter to return to the main menu..."
}

# Main menu
main_menu() {
  clear
  echo "==============================================="
  echo "             OUTDOOR TRACKER SETUP             "
  echo "==============================================="
  echo "          Real-time location tracking          "
  echo "==============================================="
  echo ""
  echo "Please select an option:"
  echo "1) Setup Development Environment"
  echo "2) Setup Production Environment"
  echo "3) Clean Up Development Environment"
  echo "4) Initialize Database with Default Data"
  echo "5) View Logs"
  echo "q) Quit"
  echo ""
  read -p "Enter your choice: " choice
  
  case $choice in
    1)
      setup_dev
      ;;
    2)
      setup_prod
      ;;
    3)
      cleanup_dev
      ;;
    4)
      init_database
      ;;
    5)
      docker-compose logs -f
      ;;
    q|Q)
      exit 0
      ;;
    *)
      print_error "Invalid option. Try again."
      sleep 1
      main_menu
      ;;
  esac
}

# Trap Ctrl+C
trap ctrl_c INT

function ctrl_c() {
  echo ""
  print_warning "Setup interrupted. Exiting..."
  exit 1
}

# Print banner
print_banner() {
  clear
  echo -e "${GREEN}===============================================${NC}"
  echo -e "${GREEN}             OUTDOOR TRACKER SETUP             ${NC}"
  echo -e "${GREEN}===============================================${NC}"
  echo -e "${BLUE}          Real-time location tracking          ${NC}"
  echo -e "${GREEN}===============================================${NC}"
  echo ""
}

# Start script
print_banner
check_docker
check_requirements
main_menu
