#!/bin/bash

# Source the environment variables
source /etc/profile.d/webappbackend_env.sh

# Navigate to the project directory
cd /home/ec2-user/webappbackend

# Restart Docker services
docker-compose down
docker-compose up -d --build

# Restart Nginx
sudo service nginx restart
