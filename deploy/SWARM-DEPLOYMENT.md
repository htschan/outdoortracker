# Docker Swarm Deployment Guide

This guide explains how to deploy the Outdoor Tracker application on a Docker Swarm cluster.

## Prerequisites

- Docker Engine v20.10.0 or later with Swarm mode enabled
- At least one server with Docker installed
- A domain name pointing to your server (for SSL/TLS)
- Basic knowledge of Docker and Docker Swarm

## Deployment Files

- `swarm-stack.yml`: The Docker Swarm stack definition
- `.env.swarm.example`: Example environment variables for deployment
- `swarm-deploy.sh`: Helper script for deployment

## Preparing the Environment

1. Initialize Docker Swarm on your manager node:
   ```bash
   docker swarm init --advertise-addr <MANAGER-IP>
   ```

2. If you have multiple nodes, add worker nodes to the swarm:
   ```bash
   # On worker nodes, run the command shown after initializing the swarm
   docker swarm join --token <TOKEN> <MANAGER-IP>:2377
   ```

3. Add a label to the node that will host the database:
   ```bash
   docker node update --label-add db=true <NODE-ID>
   ```

## Configuration

1. Copy the example environment file:
   ```bash
   cd deploy
   cp .env.swarm.example .env.swarm
   ```

2. Edit the `.env.swarm` file with your specific configuration:
   ```bash
   nano .env.swarm
   ```

3. Configure the following important settings:
   - `DOMAIN`: Your domain name (e.g., outdoortracker.example.com)
   - `MYREG_URL`: Your private registry URL (without http/https prefix)
   - `DB_PASSWORD`: A secure password for the PostgreSQL database
   - `SECRET_KEY` and `JWT_SECRET_KEY`: Secure random strings for encryption
   - `MAIL_*`: Email server configuration
   - `ACME_EMAIL`: Email for Let's Encrypt notifications
   - `TRAEFIK_DASHBOARD_AUTH`: Credentials for accessing the Traefik dashboard

## Deployment Options

### Option 1: Using the Deployment Script

1. Make the script executable:
   ```bash
   chmod +x swarm-deploy.sh
   ```

2. Run the deployment script:
   ```bash
   ./swarm-deploy.sh
   ```

### Option 2: Manual Deployment

1. Load environment variables:
   ```bash
   export $(cat .env.swarm | grep -v '^#' | xargs)
   ```

2. Deploy the stack:
   ```bash
   docker stack deploy -c swarm-stack.yml outdoortracker
   ```

## Monitoring the Deployment

1. Check the status of your services:
   ```bash
   docker service ls
   ```

2. View service logs:
   ```bash
   docker service logs outdoortracker_backend
   docker service logs outdoortracker_frontend
   ```

3. Access the Traefik dashboard at `https://traefik.<your-domain>` using the credentials configured in `.env.swarm`.

## Scaling Services

To scale a specific service:
```bash
docker service scale outdoortracker_backend=3
```

## Updating the Application

1. Build new Docker images with updated tags
2. Update the `TAG` variable in `.env.swarm`
3. Redeploy using the deployment script or manually:
   ```bash
   docker stack deploy -c swarm-stack.yml outdoortracker
   ```

## Troubleshooting

### Check Service Status

```bash
docker service ps outdoortracker_backend --no-trunc
```

### View Detailed Logs

```bash
docker service logs --tail 100 --follow outdoortracker_backend
```

### Restart a Service

```bash
docker service update --force outdoortracker_backend
```

### Remove and Redeploy the Stack

```bash
docker stack rm outdoortracker
# Wait for all services to be removed
docker stack deploy -c swarm-stack.yml outdoortracker
```
