"""
Database Configuration for Modern Online Store
Uses SQLite for local development
"""

import os


def get_database_uri():
    """Get database URI from environment or use local SQLite"""
    # Check for PostgreSQL connection string (for production)
    database_url = os.environ.get('DATABASE_URL')

    if database_url:
        # Convert postgres:// to postgresql:// for SQLAlchemy
        if database_url.startswith('postgres://'):
            database_url = database_url.replace('postgres://', 'postgresql://', 1)
        return database_url

    # Fallback to local SQLite
    return 'sqlite:///store.db'


# Database configuration
DATABASE_URI = get_database_uri()

# Use PostgreSQL if DATABASE_URL is set, otherwise SQLite
USE_POSTGRES = 'postgresql' in DATABASE_URI
