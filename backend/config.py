
from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    # SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/vandytime')
    # FIREBASE_ADMIN_CREDENTIALS = os.getenv('FIREBASE_ADMIN_CREDENTIALS', 'serviceAccountKey.json')
