#!/bin/bash

APP_DIR="/var/www/flaskapp"
EC2_USER_DIR="/home/ec2-user/flaskapp"
DOMAIN="webappbackend.fifareward.io"
EMAIL="fifarewarddapp@gmail.com"

echo "Deleting old app"
sudo rm -rf $APP_DIR

echo "Creating app folder"
sudo mkdir -p $APP_DIR

echo "Moving files to app folder"
sudo cp -r $EC2_USER_DIR/* $APP_DIR

# Navigate to the app directory
cd $APP_DIR
sudo cp $EC2_USER_DIR/.env .env

sudo yum update -y
echo "Installing Python and pip"
sudo yum install -y python3 python3-pip

# Install application dependencies from requirements.txt
echo "Installing application dependencies from requirements.txt"
sudo pip3 install -r requirements.txt

# Uninstall Nginx if it is already installed
if command -v nginx > /dev/null; then
    echo "Uninstalling Nginx"
    sudo yum remove -y nginx
fi

# Install Nginx
echo "Installing Nginx"
sudo yum install -y nginx

# Stop any existing Gunicorn process
sudo pkill gunicorn
sudo rm -rf flaskapp.sock

# Start Gunicorn with the Flask application
echo "Starting Gunicorn"
sudo gunicorn --workers 3 --bind unix:$APP_DIR/flaskapp.sock app:app --user www-data --group www-data --daemon
echo "Started Gunicorn 🚀"

# Install Certbot and obtain SSL certificate
if ! command -v certbot > /dev/null; then
    echo "Installing Certbot"
    sudo yum install -y certbot python3-certbot-nginx
fi

echo "Obtaining SSL certificate with Certbot"
sudo certbot --nginx --non-interactive --agree-tos --email $EMAIL -d $DOMAIN

echo "Reloading Nginx with SSL configuration"
sudo systemctl reload nginx

echo "Deployment completed 🚀"
