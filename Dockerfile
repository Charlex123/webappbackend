# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip
RUN pip install virtualenv
RUN virtualenv venv
RUN /app/venv/bin/pip install -r requirements.txt

# Make port 4000 available to the world outside this container
EXPOSE 4000

# Run bot.py and app.py
CMD ["sh", "-c", "/app/venv/bin/python bot.py & /app/venv/bin/python app.py"]
