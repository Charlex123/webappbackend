#!/bin/bash
set -xe

APP_DIR="/var/www/webappbackendapp"
EC2_USER_DIR="/home/ec2-user/webappbackend"
DOMAIN="webappbackend.fifareward.io"
EMAIL="fifarewarddapp@gmail.com"

# Function to check if a command exists
command_exists () {
  type "$1" &> /dev/null ;
}

# Update packages
sudo yum update -y

# Install coreutils if nohup is not available
if ! command -v nohup &> /dev/null
then
    echo "nohup could not be found. Installing coreutils..."
    sudo yum install -y coreutils
fi

# Install nginx if nginx is not available
if ! command -v nginx &> /dev/null
then
    echo "nginx could not be found. Installing nginx..."
    sudo yum install -y nginx
fi


# Install PostgreSQL if not already installed
if ! command -v psql &> /dev/null
then
    echo "PostgreSQL could not be found. Installing PostgreSQL..."
    sudo yum install -y ppostgresql15.x86_64 postgresql15-server
    sudo service postgresql initdb
    sudo service postgresql start
fi

echo "Creating app folder"
sudo mkdir -p ${APP_DIR}

echo "Moving files to app folder"
sudo cp -r ${EC2_USER_DIR}/* ${APP_DIR}

echo "Setting ownership of app directory"
sudo chown -R ec2-user:ec2-user ${APP_DIR}

# Ensure the ec2-user has ownership of the directory
sudo chown -R ec2-user:ec2-user /home/ec2-user/webappbackend

# Navigate to the webappbackend directory
cd /home/ec2-user/webappbackend

# Install virtualenv if not already installed
if ! command -v venv &> /dev/null
then
    # Create and activate a virtual environment
    python3 -m venv venv
    source venv/bin/activate
fi

# Upgrade pip and install required packages
pip install --upgrade pip
pip install -r requirements.txt

alembic upgrade head

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

