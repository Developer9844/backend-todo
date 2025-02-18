from dotenv import load_dotenv
import os

load_dotenv()

database_url = os.getenv("DATABASE_URL")
redis_url = os.getenv("REDIS_URL")

class Config:
    SQLALCHEMY_DATABASE_URI = database_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    REDIS_URL = redis_url
