#!/bin/bash
set -xe

# Source the environment variables
source /etc/profile.d/webappbackend_env.sh

# Navigate to the project directory
cd /home/ec2-user/webappbackend

if pgrep -f "bot.py" > /dev/null; then
    echo "Stopping existing bot.py process"
    pkill -f "bot.py"
fi

# Restart Docker services
docker-compose down
docker-compose up -d --build

