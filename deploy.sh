#!/bin/bash

set -e

APP_DIR="/var/www/flaskapp"
EC2_USER_DIR="/home/ec2-user/flaskapp"
DOMAIN="webappbackend.fifareward.io"
EMAIL="fifarewarddapp@gmail.com"

echo "Deleting old app"
sudo rm -rf ${APP_DIR}

echo "Creating app folder"
sudo mkdir -p ${APP_DIR}

echo "Moving files to app folder"
sudo cp -r ${EC2_USER_DIR}/* ${APP_DIR}

echo "Setting ownership of app directory"
sudo chown -R ec2-user:ec2-user ${APP_DIR}

cd ${APP_DIR}

echo "Creating .env file"
cat << EOF > .env
ENV=${ENV}
POSTGRES_USER=${POSTGRES_USER}
POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
POSTGRES_DB=${POSTGRES_DB}
DATABASE_URL=${DATABASE_URL}
BOT_TOKEN=${BOT_TOKEN}
CLOUDINARY_API_KEY: ${CLOUDINARY_API_KEY}
CLOUDINARY_SECRET_KEY: ${CLOUDINARY_SECRET_KEY}
CLOUD_NAME: ${CLOUD_NAME}
EOF

echo "Installing application dependencies from requirements.txt"
sudo yum install -y python3-pip  # Ensure pip is installed
sudo pip3 install virtualenv
virtualenv venv
source venv/bin/activate
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
sudo venv/bin/gunicorn --workers 3 --bind unix:${APP_DIR}/flaskapp.sock app:app --daemon

if pgrep -f "bot.py" > /dev/null; then
    echo "Stopping existing bot.py process"
    pkill -f "bot.py"
fi

echo "Starting bot.py"
nohup venv/bin/python bot.py &

if sudo lsof -i :80 > /dev/null; then
    echo "Port 80 is in use, stopping the process"
    sudo kill $(sudo lsof -t -i :80)
fi

echo "Creating Nginx configuration from template"
export DOLLAR='$'
envsubst < ./configs/nginx/nginx.conf.template | sudo tee /etc/nginx/conf.d/webappbackend.fifareward.io.conf > /dev/null

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
