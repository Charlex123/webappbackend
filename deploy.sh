#!/bin/bash

set -e

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

echo "Setting ownership of app directory"
sudo chown -R ec2-user:ec2-user $APP_DIR

cd $APP_DIR

echo "Setting up virtual environment"
python3 -m venv venv
source venv/bin/activate

echo "Installing application dependencies from requirements.txt"
pip install --upgrade pip
pip install -r requirements.txt

if command -v nginx > /dev/null; then
    echo "Uninstalling Nginx"
    sudo yum remove -y nginx
fi

echo "Installing Nginx"
sudo yum install -y nginx

echo "Stopping any existing Gunicorn process"
sudo pkill gunicorn || true
sudo rm -rf flaskapp.sock

echo "Starting Gunicorn"
sudo $APP_DIR/venv/bin/gunicorn --workers 3 --bind unix:$APP_DIR/flaskapp.sock app:app --daemon

if pgrep -f "bot.py" > /dev/null; then
    echo "Stopping existing bot.py process"
    pkill -f "bot.py"
fi

echo "Starting bot.py"
nohup $APP_DIR/venv/bin/python3 bot.py &

if sudo lsof -i :80 > /dev/null; then
    echo "Port 80 is in use, stopping the process"
    sudo kill $(sudo lsof -t -i :80)
fi

NGINX_CONF="/etc/nginx/conf.d/flaskapp.conf"
echo "Creating Nginx reverse proxy configuration"
sudo bash -c "cat > $NGINX_CONF <<EOF
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
EOF"

echo "Testing Nginx configuration"
sudo nginx -t

if [ $? -eq 0 ]; then
    echo "Restarting Nginx"
    sudo systemctl restart nginx

    echo "Checking DNS resolution for $DOMAIN"
    if nslookup $DOMAIN; then
        echo "DNS resolution successful, obtaining SSL certificate with Certbot"
        if ! command -v certbot > /dev/null; then
            echo "Installing Certbot"
            sudo yum install -y certbot python3-certbot-nginx
        fi

        echo "Obtaining SSL certificate with Certbot"
        sudo certbot --nginx --non-interactive --agree-tos --email $EMAIL -d $DOMAIN

        echo "Reloading Nginx with SSL configuration"
        sudo systemctl reload nginx
    else
        echo "DNS resolution failed for $DOMAIN, please check your DNS settings"
    fi

    echo "Deployment completed 🚀"
else
    echo "Nginx configuration test failed, not restarting Nginx"
fi
