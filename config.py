import os

# Find the absolute path to the directory where this config.py file lives
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = "attendance-secret-key"
    
    # Dynamically builds: C:\Users\...\Final-Project--Group--2\instance\database\database.db
    # Using 4 slashes (sqlite:////) combined with an absolute path handles Windows paths flawlessly
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "instance", "database", "database.db")
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False