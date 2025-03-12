from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.config import Config, db

from app.models.user_model import User 
from app.models.password_model import Password
from app.models.order_model import Order
from app.models.product_model import Product
from app.models.categoy_product_model import Category
from app.models.client_tipe_model import ClientType
from app.models.order_detail_model import OrderDetail


from app.routers.user_router import user_bp
from flask_bootstrap import Bootstrap
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect()


def create_app():
    app = Flask(__name__)
    Bootstrap(app) 
    app.config.from_object(Config)  
    app.config["SECRET_KEY"] = "mi_clave_secreta"  
    db.init_app(app)

    app.register_blueprint(user_bp, url_prefix="/")
    csrf.init_app(app)

    migrate = Migrate(app, db) 
    
    return app
