#!/bin/sh

# Initialize Alembic if not already initialized
if [ ! -d "/migrations" ]; then
  echo "Initializing Alembic..."
  /venv/bin/alembic init migrations
fi

# Run database migrations with Alembic
echo "Running Alembic migrations..."
/venv/bin/alembic upgrade head

# Start the bot and Flask app
/venv/bin/python bot.py &
/venv/bin/python app.py
