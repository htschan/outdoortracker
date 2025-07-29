FROM node:18-alpine AS development

WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# For development - we'll mount the source code as a volume
# The rest of the files will be mounted as volumes in docker-compose

# Set up for development mode
ENV NODE_ENV=development
EXPOSE 8080
CMD ["npm", "run", "dev"]

# Production build stage
FROM node:18-alpine AS build-stage

WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy project files
COPY . .

# Build the Vue.js application for production
ARG VITE_BUILD_TIME
ARG VITE_GIT_SHA
ENV VITE_BUILD_TIME=$VITE_BUILD_TIME
ENV VITE_GIT_SHA=$VITE_GIT_SHA
RUN npm run build

# Build the Vue.js application for production
RUN npm run build

# Production stage
FROM nginx:stable-alpine AS production-stage

# Copy built files from build-stage
COPY --from=build-stage /app/dist /usr/share/nginx/html

# Copy custom Nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
