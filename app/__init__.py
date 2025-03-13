from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import Config, db
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)
    Bootstrap(app)
    app.config.from_object(Config)
    app.config["SECRET_KEY"] = "mi_clave_secreta"

    # 🔥 Inicializar SQLAlchemy
    db.init_app(app)
    migrate = Migrate(app, db)  # Migraciones (si las usas)

    # 🔥 Activar el contexto de la aplicación (CRÍTICO para Reflection)
    with app.app_context():
        # Importa modelos aquí para evitar errores fuera del contexto
        from app.models.user_model import User
        from app.models.password_model import Password
        from app.models.order_model import Order
        from app.models.product_model import Product
        from app.models.categoy_product_model import Category
        from app.models.client_tipe_model import ClientType

        # (Opcional) Verificar que Reflection funciona:
        print("Campos cargados en Product:", Product.__table__.columns.keys())

    # 🔹 Registra los Blueprints
    from app.routers.user_router import user_bp
    from app.routers.login_router import login_bp
    from app.routers.admin_router import admin_bp
    from app.routers.order_router import order_bp

    app.register_blueprint(user_bp, url_prefix="/")
    app.register_blueprint(login_bp, url_prefix="/")
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(order_bp, url_prefix="/")

    csrf.init_app(app)

    return app
