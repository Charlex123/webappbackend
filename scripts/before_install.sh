#!/bin/bash

set -xe


APP_DIR="/var/www/webappbackendapp"
EC2_USER_DIR="/home/ec2-user/webappbackend"
DOMAIN="webappbackend.fifareward.io"
EMAIL="fifarewarddapp@gmail.com"

#  Remove existing files that may cause conflicts
sudo rm -rf /home/ec2-user/webappbackend

# Update packages
sudo yum -y update
# sudo yum -y install ruby
# sudo yum -y install wget
cd /home/ec2-user
# wget https://aws-codedeploy-ap-south-1.s3.ap-south-1.amazonaws.com/latest/install
# sudo chmod +x ./install
# sudo ./install auto

# Install Docker if not already installed
if ! command -v docker &> /dev/null; then
  sudo yum install -y docker
  sudo service docker start
  sudo usermod -a -G docker ec2-user
fi

# Install Docker Compose if not already installed
if ! command -v docker-compose &> /dev/null; then
  sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
  sudo chmod +x /usr/local/bin/docker-compose
fi

# Install coreutils if nohup is not available
if ! command -v unzip &> /dev/null
then
    echo "unzip could not be found. Installing coreutils..."
    sudo yum install -y unzip
fi

echo "Deleting old app"
sudo rm -rf ${APP_DIR}

# echo "deleting old codedeploy-agent details"

# sudo rm -rf /opt/codedeploy-agent/deployment-root

