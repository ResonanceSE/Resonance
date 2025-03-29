#!/bin/bash

# Create necessary directories
mkdir -p nginx

# Stop any existing containers
docker-compose -f docker-compose.preview.yml down

# Build and start the containers
docker-compose -f docker-compose.preview.yml up --build -d

echo "Preview environment is starting..."
echo "Frontend will be available at: http://localhost"
echo "Backend API will be available at: http://localhost/api"
echo ""
echo "Admin login:"
echo "Username: kkhamwiset"
echo "Password: Ohm890zaza"