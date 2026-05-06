import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DEBUG = True
SECRET_KEY = "dev"
DB_PATH = os.path.join(BASE_DIR, "database.db")
