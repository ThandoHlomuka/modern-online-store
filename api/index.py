"""
Vercel Serverless Function Entry Point
This file serves as the main entry point for Vercel deployment
"""

import sys
import os

# Add parent directory to path to import app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

# Vercel expects the Flask app to be imported as 'app'
# The handler is defined in app.py
