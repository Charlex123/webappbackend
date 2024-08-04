#!/bin/bash

# Function to check if a command exists
command_exists () {
  type "$1" &> /dev/null ;
}

# Update packages
sudo yum update -y

# Install Docker if not already installed
if ! command_exists docker; then
  sudo yum install -y docker
  sudo service docker start
  sudo usermod -a -G docker ec2-user
fi

# Install PostgreSQL if not already installed
if ! command_exists psql; then
  sudo yum install -y postgresql postgresql-server postgresql-contrib
  sudo service postgresql initdb
  sudo service postgresql start
fi

# Install Docker Compose if not already installed
if ! command_exists docker-compose; then
  sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
  sudo chmod +x /usr/local/bin/docker-compose
fi

chmod +x setup_environment.sh

# Source environment variables
source ./setup_environment.sh

# # Create the directory if it doesn't exist
# sudo mkdir -p /etc/profile.d/

# # Create or overwrite the custom script to set environment variables
# sudo bash -c 'cat <<EOT > /etc/profile.d/webappbackend_env.sh
# export DATABASE_URL=${DATABASE_URL}
# export BOT_TOKEN=${BOT_TOKEN}
# export CLOUDINARY_API_KEY=${CLOUDINARY_API_KEY}
# export CLOUDINARY_SECRET_KEY=${CLOUDINARY_SECRET_KEY}
# export CLOUD_NAME=${CLOUD_NAME}
# export POSTGRES_USER=${POSTGRES_USER}
# export POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
# export POSTGRES_DB=${POSTGRES_DB}
# EOT'

# # Ensure the script is executable
# sudo chmod +x /etc/profile.d/webappbackend_env.sh

# # Source the new environment variables for the current session
# source /etc/profile.d/webappbackend_env.sh
