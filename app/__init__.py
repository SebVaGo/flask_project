from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from app.config import Config, db
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from app.utils.db_session_manager import AltDBSessionManager

csrf = CSRFProtect()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    Bootstrap(app)

    app.config.from_object(Config)
    app.config["SECRET_KEY"] = "mi_clave_secreta"
    app.secret_key = "mi_clave_secreta"

    db.init_app(app)
    migrate = Migrate(app, db)

    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    with app.app_context():
        from app.models.user_model import UserModel
        from app.models.password_model import PasswordModel
        from app.models.order_model import OrderModel
        from app.models.product_model import ProductModel
        from app.models.categoy_product_model import CategoryModel
        from app.models.client_tipe_model import ClientTypeModel

        @login_manager.user_loader
        def load_user(user_id):
            try:
                with AltDBSessionManager() as session:
                    user = session.query(UserModel).filter(UserModel.id == int(user_id)).first()
                    if user:
                        session.expunge(user)
                    return user
            except:
                return None

    from app.routers.user_router import user_bp
    from app.routers.auth_router import auth_bp
    from app.routers.admin_router import admin_bp
    from app.routers.order_router import order_bp

    app.register_blueprint(user_bp, url_prefix="/") 
    app.register_blueprint(auth_bp, url_prefix="/")
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(order_bp, url_prefix="/")

    csrf.init_app(app)

    return app