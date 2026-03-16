"""
WSGI entry point for Vercel deployment
"""
import os
import sys

# Add the project root to the path
sys.path.insert(0, os.path.dirname(__file__))

# Set required environment variables
os.environ['FLASK_ENV'] = os.environ.get('FLASK_ENV', 'production')
os.environ['DEBUG'] = os.environ.get('DEBUG', 'False')

# Import the Flask app
from app import app

# Export for Vercel
handler = app
