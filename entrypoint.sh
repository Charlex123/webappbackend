#!/bin/sh

# Initialize Alembic if not already initialized
if [ ! -d "/migrations" ]; then
  echo "Initializing Alembic..."
  /venv/bin/alembic init migrations
  # Adjust the alembic.ini file if needed (e.g., set database URL)
  sed -i "s#postgresql://postgres01:postgres@db:5432/postgres#${DATABASE_URL}#g" alembic.ini
fi

# Run database migrations with Alembic
echo "Running Alembic migrations..."
/venv/bin/alembic upgrade head

# Start the bot and Flask app
/venv/bin/python bot.py &
/venv/bin/python app.py
