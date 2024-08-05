#!/bin/bash

set -xe


APP_DIR="/var/www/webappbackendapp"
EC2_USER_DIR="/home/ec2-user/webappbackend"
DOMAIN="webappbackend.fifareward.io"
EMAIL="fifarewarddapp@gmail.com"

sudo service codedeploy-agent stop

# Update packages
sudo yum update -y

# Install coreutils if nohup is not available
if ! command -v unzip &> /dev/null
then
    echo "unzip could not be found. Installing coreutils..."
    sudo yum install -y unzip
fi

echo "Deleting old app"
sudo rm -rf ${APP_DIR}

echo "deleting old codedeploy-agent details"

sudo rm -rf /opt/codedeploy-agent/deployment-root

echo "Creating app folder"
sudo mkdir -p ${APP_DIR}

echo "Moving files to app folder"
sudo cp -r ${EC2_USER_DIR}/* ${APP_DIR}

echo "Setting ownership of app directory"
sudo chown -R ec2-user:ec2-user ${APP_DIR}