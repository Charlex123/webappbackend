#!/bin/bash

# Source the environment variables
source /etc/profile.d/webappbackend_env.sh

# Navigate to the project directory
cd /home/ec2-user/webappbackend

# alembic upgrade head

# Restart Docker services
docker-compose down
docker-compose up -d --build

# Restart Nginx
sudo service nginx restart


if pgrep -f "bot.py" > /dev/null; then
    echo "Stopping existing bot.py process"
    pkill -f "bot.py"
fi

echo "Starting bot.py"