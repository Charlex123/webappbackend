#!/bin/bash

# Define the path for the custom environment variable script
ENV_VARS_FILE="/etc/profile.d/webappbackend_env.sh"

# Source the new environment variables for the current session
source $ENV_VARS_FILE

# Navigate to the project directory
cd /home/ec2-user/webappbackend

# Restart Docker services
docker-compose down
docker-compose up -d --build
