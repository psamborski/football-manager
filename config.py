# 6. Warstwa Konfiguracji (Configuration Layer)
import os

# Get application stage from environment
app_stage = os.getenv('STAGE')

# Base directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Database directory
DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'app', 'database', 'fm.db' if app_stage == 'PRODUCTION' else 'fm_dev.db')}"
