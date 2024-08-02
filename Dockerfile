# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /

# # Install system dependencies
# RUN apt-get update && apt-get install -y \
#     gcc \
#     libpq-dev \
#     python3-venv \
#     && rm -rf /var/lib/apt/lists/*

# Copy the current directory contents into the container at /
COPY . .

# Install any needed packages specified in requirements.txt
RUN python -m venv venv

RUN pip install --upgrade pip
# Activate the virtual environment and install dependencies
RUN /venv/bin/pip install -r requirements.txt
RUN /venv/bin/pip install alembic

# Make port 4000 available to the world outside this container
EXPOSE 4000

# Copy entrypoint script into the container
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Run the entrypoint script
ENTRYPOINT ["/entrypoint.sh"]
