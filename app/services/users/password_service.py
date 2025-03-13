from werkzeug.security import generate_password_hash

from app.config import db

from app.models.password_model import PasswordModel


class PasswordService:
    
    @staticmethod
    def create_password(user_id, password):
        password_hash = generate_password_hash(password)
        password_entry = PasswordModel(id_usuario=user_id, password_hash=password_hash)
        db.session.add(password_entry)

    @staticmethod
    def update_password(user_id, new_password):
        password_entry = PasswordModel.query.filter_by(id_usuario=user_id).first()
        password_hash = generate_password_hash(new_password)
        if password_entry:
            password_entry.password_hash = password_hash
        else:
            db.session.add(PasswordModel(id_usuario=user_id, password_hash=password_hash))

