import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Flask application configuration."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'kaori-secret-key-change-in-production')
    SUPABASE_URL = os.getenv('SUPABASE_URL', 'https://qfiyvwfqtskdlzoqjybg.supabase.co')
    SUPABASE_KEY = os.getenv('SUPABASE_KEY', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFmaXl2d2ZxdHNrZGx6b3FqeWJnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODI0OTA4MjUsImV4cCI6MjA5ODA2NjgyNX0.ZCORpp8wc_lFvGrz4eHY6StwC201xnsHxXDXTJj2ICU')
    SUPABASE_SERVICE_KEY = os.getenv('SUPABASE_SERVICE_KEY', '')
    DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
