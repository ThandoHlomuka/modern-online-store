"""
Database Configuration for Modern Online Store
Supports both SQLite (local) and PostgreSQL/Supabase (production)
"""

import os


def get_database_uri():
    """Get database URI from environment or use local SQLite"""
    # Check for Vercel PostgreSQL first
    database_url = os.environ.get('POSTGRES_URL') or os.environ.get('POSTGRES_URL_NON_POOLING')

    if database_url:
        return database_url

    # Check for Supabase/PostgreSQL connection string
    database_url = os.environ.get('DATABASE_URL') or os.environ.get('SUPABASE_DB_URL')

    if database_url:
        # Convert postgres:// to postgresql:// for SQLAlchemy
        if database_url.startswith('postgres://'):
            database_url = database_url.replace('postgres://', 'postgresql://', 1)
        return database_url

    # Fallback to local SQLite
    return 'sqlite:///store.db'


def get_supabase_config():
    """Get Supabase configuration"""
    return {
        'url': os.environ.get('SUPABASE_URL', os.environ.get('NEXT_PUBLIC_SUPABASE_URL', '')),
        'key': os.environ.get('SUPABASE_KEY', os.environ.get('SUPABASE_ANON_KEY', os.environ.get('NEXT_PUBLIC_SUPABASE_ANON_KEY', ''))),
        'storage_bucket': os.environ.get('SUPABASE_STORAGE_BUCKET', 'avatars')
    }


# Database configuration
DATABASE_URI = get_database_uri()
SUPABASE_CONFIG = get_supabase_config()

# Use PostgreSQL if DATABASE_URL is set, otherwise SQLite
USE_POSTGRES = 'postgresql' in DATABASE_URI
