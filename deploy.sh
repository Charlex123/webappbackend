#!/bin/bash

echo "Deleting old app"
sudo rm -rf /var/www/

echo "Creating app folder"
sudo mkdir -p /var/www/flaskapp

echo "Moving files to app folder"
sudo cp -r /home/ec2-user/flaskapp/* /var/www/flaskapp

# Navigate to the app directory
cd /var/www/flaskapp/
sudo cp /home/ec2-user/flaskapp/.env .env

sudo yum update -y
echo "Installing Python and pip"
sudo yum install -y python3 python3-pip

# Install application dependencies from requirements.txt
echo "Install application dependencies from requirements.txt"
sudo pip3 install -r requirements.txt

# Update and install Nginx if not already installed
if ! command -v nginx > /dev/null; then
    echo "Installing Nginx"
    sudo amazon-linux-extras install nginx1.12 -y
fi

# Configure Nginx to act as a reverse proxy if not already configured
if [ ! -f /etc/nginx/conf.d/flaskapp.conf ]; then
    sudo rm -f /etc/nginx/nginx.conf
    sudo bash -c 'cat > /etc/nginx/nginx.conf <<EOF
server {
    listen 80;
    server_name webappbackend.fifareward.io;

    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/flaskapp/flaskapp.sock;
    }
}
EOF'

    sudo systemctl restart nginx
else
    echo "Nginx reverse proxy configuration already exists."
fi

# Stop any existing Gunicorn process
sudo pkill gunicorn
sudo rm -rf flaskapp.sock

# Start Gunicorn with the Flask application
echo "Starting Gunicorn"
sudo gunicorn --workers 3 --bind unix:flaskapp.sock server:app --user ec2-user --group ec2-user --daemon
echo "Started Gunicorn 🚀"

# Install Certbot and obtain SSL certificate
if ! command -v certbot > /dev/null; then
    echo "Installing Certbot"
    sudo yum install -y certbot python3-certbot-nginx
fi

echo "Obtaining SSL certificate with Certbot"
sudo certbot --nginx --non-interactive --agree-tos --email fifarewarddapp@gmail.com -d webappbackend.fifareward.io

echo "Reloading Nginx with SSL configuration"
sudo systemctl reload nginx

echo "Deployment completed 🚀"
