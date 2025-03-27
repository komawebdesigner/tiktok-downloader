#!/bin/bash

# Activate virtual environment if exists
if [ -d "venv" ]; then
    echo "🔹 Activating virtual environment..."
    source venv/bin/activate
else
    echo "🔹 No virtual environment found. Creating one..."
    python3 -m venv venv
    source venv/bin/activate
fi

# Install dependencies
echo "🔹 Installing dependencies..."
pip install -r requirements.txt

# Export Flask app environment variables
export FLASK_APP=app.py
export FLASK_ENV=development  # Change to "production" for deployment

# Run Flask app with Gunicorn (Production) or Flask built-in server
echo "🚀 Starting Flask app..."
if command -v gunicorn &> /dev/null
then
    gunicorn -w 4 -b 0.0.0.0:5000 app:app
else
    flask run --host=0.0.0.0 --port=5000
fi
