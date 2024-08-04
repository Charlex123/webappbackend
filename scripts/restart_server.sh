#!/bin/bash

# Define the path for the custom environment variable script
ENV_VARS_FILE="/etc/profile.d/webappbackend_env.sh"

# Create or overwrite the custom script to set environment variables
cat <<EOF > $ENV_VARS_FILE
#!/bin/bash
export DATABASE_URL=${DATABASE_URL}
export BOT_TOKEN=${BOT_TOKEN}
export CLOUDINARY_API_KEY=${CLOUDINARY_API_KEY}
export CLOUDINARY_SECRET_KEY=${CLOUDINARY_SECRET_KEY}
export CLOUD_NAME=${CLOUD_NAME}
export POSTGRES_USER=${POSTGRES_USER}
export POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
export POSTGRES_DB=${POSTGRES_DB}
EOF

# Ensure the script is executable
chmod +x $ENV_VARS_FILE

# Source the new environment variables for the current session
source $ENV_VARS_FILE

# Navigate to the project directory
cd /home/ec2-user/webappbackend

# Restart Docker services
docker-compose down
docker-compose up -d --build
