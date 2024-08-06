# Use the official Python image from the Docker Hub
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip && \
    pip install -r requirements.txt
    
# Expose port 5000 for Flask
EXPOSE 5000

# Define environment variable
# ENV NAME webappbackend

# Command to run both app.py and bot.py
CMD ["sh", "-c", "gunicorn -b 0.0.0.0:5000 app:app & nohup python3 bot.py"]
