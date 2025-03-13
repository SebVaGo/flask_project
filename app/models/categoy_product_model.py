from app.config import db

class Category(db.Model):
    __tablename__ = "categories"
    __table_args__ = {'autoload_with': db.engine}  # 🔥 Reflection activo
