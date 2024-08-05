# Use the official Python image from the Docker Hub
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Copy the setup.sh script and make it executable
COPY ./scripts/setup.sh /app/scripts/setup.sh
RUN chmod +x /app/scripts/setup.sh

# Run setup script to initialize Alembic and virtual environment
RUN ./scripts/setup.sh

# Expose port 5000 for Flask
EXPOSE 5000

# Define environment variable
# ENV NAME webappbackend

# Command to run both app.py and bot.py
CMD ["sh", "-c", "gunicorn -b 0.0.0.0:5000 app:app & python bot.py"]
