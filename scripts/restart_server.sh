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

# Start the web server and bot script
nohup gunicorn -b 0.0.0.0:5000 app:app &
nohup python3 bot.py &
