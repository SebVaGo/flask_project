from app.config import db

class ClientType(db.Model):
    __tablename__ = "client_types"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(50), nullable=False, unique=True)

    def __repr__(self):
        return f"<ClientType {self.nombre}>"
    
