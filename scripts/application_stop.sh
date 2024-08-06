#!/bin/bash
set -xe

# sudo systemctl stop codedeploy-agent
# sudo rm -rf /opt/codedeploy-agent/deployment-root
sudo systemctl start codedeploy-agent

cd /home/ec2-user/webappbackend

docker-compose down