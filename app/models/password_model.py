from app.config import db

class Password(db.Model):
    __tablename__ = "passwords"
    __table_args__ = {'autoload_with': db.engine}  # 🔥 Reflection activo
