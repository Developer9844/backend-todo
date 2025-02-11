from dotenv import load_dotenv
import os


database_url = os.getenv("DATABASE_URL")

class Config:
    SQLALCHEMY_DATABASE_URI = database_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False
