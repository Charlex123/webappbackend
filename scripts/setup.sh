#!/bin/bash

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate

# Install required packages
pip install -r requirements.txt

# Initialize Alembic (ensure your alembic.ini is configured)
alembic upgrade head
