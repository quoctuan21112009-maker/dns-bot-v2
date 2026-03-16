#!/bin/bash
set -e

echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Running migrations..."
# Note: If you have Alembic migrations, uncomment this:
# alembic upgrade head

echo "Build complete!"
