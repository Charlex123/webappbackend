# Use the official Python image from the Docker Hub
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Expose port 5000 for Flask
EXPOSE 5000

# Define build arguments
ARG DATABASE_URL
ARG BOT_TOKEN
ARG CLOUDINARY_API_KEY
ARG CLOUDINARY_SECRET_KEY
ARG CLOUD_NAME
ARG POSTGRES_USER
ARG POSTGRES_PASSWORD
ARG POSTGRES_DB

# Set environment variables
ENV DATABASE_URL=$DATABASE_URL
ENV BOT_TOKEN=$BOT_TOKEN
ENV CLOUDINARY_API_KEY=$CLOUDINARY_API_KEY
ENV CLOUDINARY_SECRET_KEY=$CLOUDINARY_SECRET_KEY
ENV CLOUD_NAME=$CLOUD_NAME
ENV POSTGRES_USER=$POSTGRES_USER
ENV POSTGRES_PASSWORD=$POSTGRES_PASSWORD
ENV POSTGRES_DB=$POSTGRES_DB

# Define environment variable
ENV NAME webappbackend

# Run setup script to initialize Alembic and virtual environment
RUN chmod +x ./scripts/setup.sh && ./scripts/setup.sh

# Command to run both app.py and bot.py
CMD ["sh", "-c", "gunicorn -b 0.0.0.0:5000 app:app & python bot.py"]
