# 6. Warstwa Konfiguracji (Configuration Layer)
import logging
import os

# app basic data
APP_NAME = "FM CLI"
APP_VERSION = "0.2"

# Get application stage from environment
app_stage = os.getenv('STAGE')

# Base directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Database directory
DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'app', 'database', 'fm.db' if app_stage == 'PRODUCTION' else 'fm_dev.db')}"

# Logging configuration
LOGGING_CONFIG = {
    'filename': 'app.log',
    'filemode': 'a',
    'format': '%(asctime)s,%(msecs)d %(name)s %(levelname)s in %(module)s:\n%(message)s',
    'datefmt': '%H:%M:%S',
    'level': logging.DEBUG,
}

def setup_logging():
    logging.basicConfig(**LOGGING_CONFIG)
