import psycopg2
from config import load_config

def get_connection():
    """Return a connection to the PostgreSQL database"""
    config = load_config()
    return psycopg2.connect(**config)