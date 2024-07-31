#!/bin/bash

set -e

APP_DIR="/var/www/flaskapp"
EC2_USER_DIR="/home/ec2-user/flaskapp"
DOMAIN="webappbackend.fifareward.io"
EMAIL="fifarewarddapp@gmail.com"
host='$host'
remote_addr='$remote_addr'
request_uri='$request_uri'
proxy_add_x_forwarded_for='$proxy_add_x_forwarded_for'
scheme='$scheme'


echo "Deleting old app"
sudo rm -rf ${APP_DIR}

echo "Creating app folder"
sudo mkdir -p ${APP_DIR}

echo "Moving files to app folder"
sudo cp -r ${EC2_USER_DIR}/* ${APP_DIR}

echo "Setting ownership of app directory"
sudo chown -R ec2-user:ec2-user ${APP_DIR}

cd ${APP_DIR}

echo "Installing application dependencies from requirements.txt"
sudo yum install -y python3-pip  # Ensure pip is installed
sudo python3 -m pip install -r requirements.txt

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
sudo gunicorn --workers 3 --bind unix:${APP_DIR}/flaskapp.sock app:app --daemon

if pgrep -f "bot.py" > /dev/null; then
    echo "Stopping existing bot.py process"
    pkill -f "bot.py"
fi

echo "Starting bot.py"
nohup python3 bot.py &

if sudo lsof -i :80 > /dev/null; then
    echo "Port 80 is in use, stopping the process"
    sudo kill $(sudo lsof -t -i :80)
fi

NGINX_CONF="/etc/nginx/conf.d/webappbackend.fifareward.io.conf"
echo "Creating Nginx reverse proxy configuration"
sudo bash -c "cat > ${NGINX_CONF} <<EOF
server {
    server_name webappbackend.fifareward.io www.webappbackend.fifareward.io;

    location / {
        proxy_pass http://54.161.105.37/:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    access_log /var/log/nginx/access_log;
    error_log /var/log/nginx/error_log;

    listen [::]:443 ssl ipv6only=on;
    listen 443 ssl;
    ssl_certificate /etc/letsencrypt/live/webappbackend.fifareward.io/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/webappbackend.fifareward.io/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;
}

server {
    if ($host = www.webappbackend.fifareward.io) {
        return 301 https://$host$request_uri;
    }

    if (${host} = webappbackend.fifareward.io) {
        return 301 https://$host$request_uri;
    }

    listen 80;
    listen [::]:80;
    server_name webappbackend.fifareward.io www.webappbackend.fifareward.io;
    return 404;
}
EOF"

echo "Testing Nginx configuration"
sudo nginx -t

if [ $? -eq 0 ]; then
    echo "Restarting Nginx"
    sudo systemctl restart nginx

    echo "Checking DNS resolution for ${DOMAIN}"
    if nslookup ${DOMAIN}; then
        echo "DNS resolution successful, obtaining SSL certificate with Certbot"
        if ! command -v certbot > /dev/null; then
            echo "Installing Certbot"
            sudo yum install -y certbot python3-certbot-nginx
        fi

        echo "Obtaining SSL certificate with Certbot"
        sudo certbot --nginx --non-interactive --agree-tos --email ${EMAIL} -d ${DOMAIN}

        echo "Reloading Nginx with SSL configuration"
        sudo systemctl reload nginx
    else
        echo "DNS resolution failed for ${DOMAIN}, please check your DNS settings"
    fi

    echo "Deployment completed 🚀"
else
    echo "Nginx configuration test failed, not restarting Nginx"
fi
