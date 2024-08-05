#!/bin/bash

set -xe


APP_DIR="/var/www/webappbackendapp"
EC2_USER_DIR="/home/ec2-user/webappbackend"
DOMAIN="webappbackend.fifareward.io"
EMAIL="fifarewarddapp@gmail.com"

#  Remove existing files that may cause conflicts
sudo rm -f /home/ec2-user/webappbackend/

# Update packages
sudo yum -y update

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

