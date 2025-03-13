from app.config import db

class ClientType(db.Model):
    __tablename__ = "client_types"
    __table_args__ = {'autoload_with': db.engine}  # 🔥 Reflection activo
