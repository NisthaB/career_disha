import os

DEBUG = True
SECRET_KEY = 'a1b2c3'
STATIC_F = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/')
CACHE_TYPE = "null"
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:abc123@localhost:5432/career_disha_db'
TEMPLATES_AUTO_RELOAD = True

