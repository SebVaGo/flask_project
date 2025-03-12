from app.config import db

class Password(db.Model):
    __tablename__ = "passwords"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"<Password {self.id_usuario}>"

