from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  # Instancia de SQLAlchemy

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost/flasktest'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

