# Outdoor Tracker

A real-time outdoor tracking application that allows users to share their location during outdoor activities like hiking or cycling.

![Outdoor Tracker](https://via.placeholder.com/800x400?text=Outdoor+Tracker)

## Features

- **Real-time location tracking and sharing** - Track your activities and share them with friends
- **Live map view** - See where all active users are in real-time
- **Mobile-friendly Progressive Web App (PWA)** - Works on all devices with an app-like experience
- **OpenStreetMap integration** - High-quality maps without any API key requirements
- **User authentication with email verification** - Secure account creation process
- **Admin approval for new users** - Control who can join your instance
- **User management dashboard** - Admins can approve, activate/deactivate, and delete users
- **Docker containerization for easy deployment** - Simple setup in any environment
- **CI/CD with GitHub Actions** - Automated testing, security scanning, and deployment

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
- Git

### Running the Application

You can use the setup script for an automated setup process:

```bash
./setup.sh
```

This script will guide you through setting up either a development or production environment.

#### Manual Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/htschan/outdoortracker.git
   cd outdoortracker
   ```

2. Create a `.env` file from the example:
   ```bash
   cp .env.example .env
   ```

3. Configure environment variables:
   ```bash
   # Edit the .env file with your settings
   # At minimum, set DATABASE_URL, SECRET_KEY, JWT_SECRET_KEY
   nano .env
   ```

4. Start the application:
   ```bash
   docker-compose up -d
   ```

5. Initialize the database with test users:
   ```bash
   docker-compose exec backend python init_db.py
   ```

6. Access the application:
   - Frontend: http://localhost:8080
   - Backend API: http://localhost:5000/api

### Default Admin Credentials

After running the database initialization script, you can log in with:
- Email: outdoortracker@sorawit.ch
- Password: Axil&311

### Production Deployment

For production deployment, use the production Docker Compose file:

1. Configure production environment:
   ```bash
   cp .env.example .env.prod
   nano .env.prod
   ```

2. Start production services:
   ```bash
   docker-compose -f docker-compose.prod.yml --env-file .env.prod up -d
   ```

3. Set up HTTPS with a reverse proxy like Nginx or Traefik in front of the application.

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

### Option 1: Docker Compose Deployment

For a simple production deployment using Docker Compose:

1. Configure environment variables for production:
   ```bash
   # Create and edit the production .env file
   cp .env.example .env.prod
   # Edit the .env.prod file with your production settings
   ```

2. Deploy using the production Docker Compose file:
   ```bash
   # Start all services in production mode
   docker-compose -f docker-compose.prod.yml --env-file .env.prod up -d
   ```

### Option 2: Docker Swarm Deployment

For a scalable, production-ready deployment using Docker Swarm:

1. Navigate to the deployment directory:
   ```bash
   cd deploy
   ```

2. Configure your deployment environment:
   ```bash
   # Create and edit the Swarm environment file
   cp .env.swarm.example .env.swarm
   # Edit with your production settings
   nano .env.swarm
   ```

3. Run the deployment script:
   ```bash
   # Deploy to Docker Swarm
   ./swarm-deploy.sh
   ```

For detailed instructions on Docker Swarm deployment, see [Swarm Deployment Guide](deploy/SWARM-DEPLOYMENT.md)

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

## Contributing

If you would like to contribute to this project, please follow these steps:

1. Fork the repository on GitHub
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/outdoortracker.git`
3. Create a new branch (`git checkout -b feature/your-feature`)
4. Make your changes
5. Run tests to ensure functionality
6. Commit your changes (`git commit -m 'Add some feature'`)
7. Push to the branch (`git push origin feature/your-feature`)
8. Open a Pull Request on GitHub

### Code Style Guidelines

- Backend: Follow PEP 8 Python style guide
- Frontend: Follow Vue.js style guide and use ESLint configuration

### Development Process

1. Create an issue for the feature or bug you're working on
2. Reference the issue in your pull request
3. Add appropriate tests for your changes
4. Update documentation as needed

## Continuous Integration and Deployment

This project uses GitHub Actions for automated testing, security scanning, and deployment:

- **Build and Test**: Runs on every push and pull request
- **Security Scan**: Checks for vulnerabilities in code and dependencies
- **Deployment**: Automatically deploys to production when changes are merged to main

For more information on the CI/CD setup, see [GitHub Actions Documentation](docs/github-actions.md)

## License

This project is licensed under the MIT License - see below for details:

```
MIT License

Copyright (c) 2023 Hans Schanowitz

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
