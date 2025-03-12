from app.models.password_model import Password
from app.config import db

class PasswordRepository:

    @staticmethod
    def create_password(id_usuario, password_hash):
        password = Password(id_usuario=id_usuario, password_hash=password_hash)
        db.session.add(password)
        db.session.commit()
        return password

    @staticmethod
    def get_password_by_user_id(user_id):
        return Password.query.filter_by(id_usuario=user_id).first()

    @staticmethod
    def update_password(user_id, new_password_hash):
        password = Password.query.filter_by(id_usuario=user_id).first()
        if password:
            password.password_hash = new_password_hash
            db.session.commit()
        return password
    
    
