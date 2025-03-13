from flask_sqlalchemy import SQLAlchemy
import os


db = SQLAlchemy() 

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost/flasktest'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "mi_clave_secreta") 



