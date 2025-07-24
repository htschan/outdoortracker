#!/bin/bash
# Deploy script for Outdoor Tracker on Docker Swarm

set -e

# Change to the script's directory
cd "$(dirname "$0")"

# Check if .env.swarm exists, if not, create from example
if [ ! -f .env.swarm ]; then
    echo "Creating .env.swarm from example..."
    cp .env.swarm.example .env.swarm
    echo "Please edit .env.swarm with your configuration values and run this script again."
    exit 1
fi

# Source environment variables
source .env.swarm

# Check if Docker Swarm is initialized
if ! docker info | grep -q "Swarm: active"; then
    echo "Docker Swarm is not initialized. Initializing..."
    docker swarm init
fi

# Check if nodes have required labels
NODE_ID=$(docker node ls --filter "role=manager" --format "{{.ID}}" | head -n1)
if ! docker node inspect $NODE_ID --format "{{.Spec.Labels}}" | grep -q "db"; then
    echo "Adding db label to manager node..."
    docker node update --label-add db=true $NODE_ID
fi

# Build or pull images
echo "Building or pulling Docker images..."

if [ -n "$DOCKER_REGISTRY" ]; then
    # Pull from registry
    echo "Pulling images from $DOCKER_REGISTRY..."
    docker pull ${DOCKER_REGISTRY}outdoortracker-frontend:${TAG:-latest}
    docker pull ${DOCKER_REGISTRY}outdoortracker-backend:${TAG:-latest}
else
    # Build locally
    echo "Building images locally..."
    docker build -t outdoortracker-frontend:${TAG:-latest} ../frontend
    docker build -t outdoortracker-backend:${TAG:-latest} ../backend
fi

# Create required networks if they don't exist
if ! docker network ls | grep -q "outdoortracker_frontend"; then
    echo "Creating frontend overlay network..."
    docker network create --driver overlay --attachable outdoortracker_frontend
fi

if ! docker network ls | grep -q "outdoortracker_backend"; then
    echo "Creating backend overlay network..."
    docker network create --driver overlay --attachable outdoortracker_backend
fi

# Deploy the stack
echo "Deploying Outdoor Tracker stack..."
env $(cat .env.swarm | grep -v '^#') docker stack deploy -c swarm-stack.yml outdoortracker

echo "Deployment complete! Your application should be running at https://$DOMAIN"
echo "Traefik dashboard is available at https://traefik.$DOMAIN (login with credentials in .env.swarm)"

# Show running services
echo ""
echo "Docker services:"
docker service ls --filter "name=outdoortracker"

# Wait for services to start
echo ""
echo "Waiting for services to start..."
sleep 5

# Check service logs
echo ""
echo "Backend service logs:"
docker service logs --tail 10 outdoortracker_backend

echo ""
echo "Frontend service logs:"
docker service logs --tail 10 outdoortracker_frontend
