import os
from dotenv import load_dotenv

#load_dotenv()

# # Connect to the database
# SQLALCHEMY_DATABASE_URI = 'your psycopg2 URI connection'
# # Turn off the Flask-SQLAlchemy event system and warning
# SQLALCHEMY_TRACK_MODIFICATIONS = False
ENV = "development"
DEVELOPMENT = True
SECRET_KEY = os.urandom(32)
SERVER_NAME = "localhost:5600"
DEBUG = True