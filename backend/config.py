import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "vyshnavi_secret_key_2026")
    DEBUG = False
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
    DB_NAME = "customer_feedback_db"
    COLLECTION_NAME = "feedback"

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
    MONGO_URI = os.getenv("MONGO_URI")

# The name 'config_dict' must be what app.py imports
config_dict = {
    "development": DevelopmentConfig,
    "production": ProductionConfig
}