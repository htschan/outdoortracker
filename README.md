# Outdoor Tracker

A real-time outdoor tracking application that allows users to share their location during outdoor activities like hiking or cycling.

## Features

- Real-time location tracking and sharing
- Mobile-friendly Progressive Web App (PWA)
- OpenStreetMap integration
- User authentication with email verification
- Admin approval for new users
- Docker containerization for easy deployment

## Tech Stack

### Frontend
- Vue.js 3
- Pinia for state management
- Vue Router for navigation
- Leaflet for maps
- PWA capabilities with service workers
- Socket.IO for real-time communication

### Backend
- Python Flask
- PostgreSQL database
- Flask-SocketIO for WebSockets
- JWT authentication
- SQLAlchemy ORM

### Infrastructure
- Docker Swarm for orchestration
- Nginx for serving frontend assets
- Gunicorn for Python application server
- Designed to run on a Synology server

## Development Setup

The application is designed to run completely in Docker containers. No local installation of dependencies is needed.

### Prerequisites

- Docker
- Docker Compose

### Running the Application

You can use the setup script for an automated setup process:

```bash
./setup.sh
```

This script will guide you through setting up either a development or production environment.

#### Manual Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd outdoortracker
   ```

2. Create a `.env` file from the example:
   ```bash
   cp .env.example .env
   ```

3. Start the application:
   ```bash
   docker-compose up -d
   ```

3. Access the application:
   - Frontend: http://localhost:8080
   - Backend API: http://localhost:5000/api

## Project Structure

```
outdoortracker/
├── docker-compose.yml        # Docker Compose configuration
├── frontend/                 # Vue.js frontend
│   ├── Dockerfile            # Frontend Docker configuration
│   ├── nginx.conf            # Nginx configuration for frontend
│   ├── package.json          # Frontend dependencies
│   └── ...                   # Vue.js application files
└── backend/                  # Python Flask backend
    ├── Dockerfile            # Backend Docker configuration
    ├── requirements.txt      # Python dependencies
    ├── app/                  # Application code
    │   ├── api/              # API endpoints
    │   ├── models/           # Database models
    │   ├── sockets/          # WebSocket handlers
    │   └── services/         # Helper services
    └── wsgi.py               # Application entry point
```

## Production Deployment

For production deployment on a Synology server:

1. Set up Docker Swarm on your Synology:
   ```bash
   # Initialize Docker Swarm on the manager node (your Synology)
   docker swarm init
   ```

2. Configure environment variables for production:
   ```bash
   # Create and edit the production .env file
   cp .env.example .env.prod
   # Edit the .env.prod file with your production settings
   ```

3. Deploy the stack using the production Docker Compose file:
   ```bash
   # Deploy the stack to the swarm
   docker stack deploy -c docker-compose.prod.yml --with-registry-auth outdoortracker
   ```

4. Verify the deployment:
   ```bash
   # Check the running services
   docker service ls
   ```

## Users and Roles

The application supports two user roles:

1. **User**: Regular users who can track their location and view others
2. **Admin**: Can manage and approve users

New users must verify their email and be approved by an admin before accessing the application.
