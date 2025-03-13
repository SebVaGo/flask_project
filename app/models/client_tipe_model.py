from app.config import db

class ClientTypeModel(db.Model):
    __tablename__ = "client_types"
    __table_args__ = {'autoload_with': db.engine}  
