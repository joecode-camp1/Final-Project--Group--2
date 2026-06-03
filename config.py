class Config:
    SECRET_KEY = "attendance-secret-key"

    SQLALCHEMY_DATABASE_URI = "sqlite:///instance/database/database.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False