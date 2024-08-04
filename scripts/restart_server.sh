#!/bin/bash

# Define the path for the custom environment variable script
ENV_VARS_FILE="/etc/profile.d/webappbackend_env.sh"

# Create or overwrite the custom script to set environment variables
echo "#!/bin/bash" > $ENV_VARS_FILE
echo "export DATABASE_URL=${DATABASE_URL} >> $ENV_VARS_FILE
echo "export BOT_TOKEN=${BOT_TOKEN} >> $ENV_VARS_FILE
echo "export CLOUDINARY_API_KEY=${CLOUDINARY_API_KEY}" >> $ENV_VARS_FILE
echo "export CLOUDINARY_SECRET_KEY=${CLOUDINARY_SECRET_KEY}" >> $ENV_VARS_FILE
echo "export CLOUD_NAME=${CLOUD_NAME}" >> $ENV_VARS_FILE
echo "export POSTGRES_USER=${POSTGRES_USER}" >> $ENV_VARS_FILE
echo "export POSTGRES_PASSWORD=${POSTGRES_PASSWORD}" >> $ENV_VARS_FILE
echo "export POSTGRES_DB=${POSTGRES_DB}" >> $ENV_VARS_FILE


# Ensure the script is executable
chmod +x $ENV_VARS_FILE

# Source the new environment variables for the current session
source $ENV_VARS_FILE

# Navigate to the project directory
cd /home/ec2-user/webappbackend

# Restart Docker services
docker-compose down
docker-compose up -d --build
