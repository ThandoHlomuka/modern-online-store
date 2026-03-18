"""
Database Configuration for Modern Online Store
Uses PostgreSQL exclusively
"""

import os


def get_database_uri():
    """Get PostgreSQL database URI from environment"""
    # Check for PostgreSQL connection string in order of priority
    database_url = (
        os.environ.get('DATABASE_URL') or
        os.environ.get('POSTGRES_URL') or
        os.environ.get('POSTGRES_URL_NON_POOLING') or
        os.environ.get('SUPABASE_DB_URL') or
        os.environ.get('supabasedb_POSTGRES_URL') or
        os.environ.get('supabasedb_POSTGRES_URL_NON_POOLING')
    )

    if not database_url:
        raise ValueError(
            "No PostgreSQL database configured. "
            "Please set DATABASE_URL, POSTGRES_URL, or SUPABASE_DB_URL environment variable."
        )

    # Convert postgres:// to postgresql:// for SQLAlchemy compatibility
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)

    # Strip problematic Supabase/Vercel query parameters
    # Specifically 'supa=xxx' which causes psycopg2.ProgrammingError: invalid connection option "supa"
    if '?' in database_url:
        base_url, query_string = database_url.split('?', 1)
        params = [p for p in query_string.split('&') if not p.startswith('supa=')]
        if params:
            database_url = f"{base_url}?{'&'.join(params)}"
        else:
            database_url = base_url

    return database_url


# Database configuration - will raise error if no database URL is set
DATABASE_URI = get_database_uri()

# Always using PostgreSQL
USE_POSTGRES = True
