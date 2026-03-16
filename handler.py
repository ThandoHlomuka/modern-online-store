"""
Vercel entry point - imports and exports the Flask app
"""
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(__file__))

# Set environment variables
os.environ['FLASK_ENV'] = 'production'
os.environ['DEBUG'] = 'False'

# Import the Flask app - this is what Vercel will use
from app import app

# Export for Vercel
handler = app
