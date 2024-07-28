#!/bin/bash

APP_DIR="/var/www/flaskapp"
EC2_USER_DIR="/home/ec2-user/flaskapp"
NGINX_CONF="/etc/nginx/nginx.conf"
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

# Update and install Nginx if not already installed
if ! command -v nginx > /dev/null; then
    echo "Installing Nginx"
    sudo yum install -y nginx
fi

# Configure Nginx to act as a reverse proxy
sudo bash -c "cat > $NGINX_CONF <<EOF
user nginx;
worker_processes auto;
error_log /var/log/nginx/error.log;
pid /run/nginx.pid;

events {
    worker_connections 1024;
}

http {
    log_format  main  '\$remote_addr - \$remote_user [\$time_local] "\$request" '
                      '\$status \$body_bytes_sent "\$http_referer" '
                      '"\$http_user_agent" "\$http_x_forwarded_for"';

    access_log  /var/log/nginx/access.log  main;

    sendfile            on;
    tcp_nopush          on;
    tcp_nodelay         on;
    keepalive_timeout   65;
    types_hash_max_size 2048;

    include             /etc/nginx/mime.types;
    default_type        application/octet-stream;

    include /etc/nginx/conf.d/*.conf;

    server {
        listen 80;
        server_name $DOMAIN;

        location / {
            proxy_pass http://unix:$APP_DIR/flaskapp.sock;
            proxy_http_version 1.1;
            proxy_set_header Upgrade \$http_upgrade;
            proxy_set_header Connection 'upgrade';
            proxy_set_header Host \$host;
            proxy_cache_bypass \$http_upgrade;
        }
    }
}
EOF"

sudo systemctl restart nginx

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
