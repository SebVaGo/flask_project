from werkzeug.security import generate_password_hash
from app.config import db
from app.services.users.base_user_service import BaseUserService


class PasswordService(BaseUserService):

    def __init__(self):
        super().__init__()
    
    def create_password(self, session, user_id, password):
        password_hash = generate_password_hash(password)
        password_entry = self.password_model(id_usuario=user_id, password_hash=password_hash)
        session.add(password_entry)

    def update_password(self, session, user_id, new_password):
        password_entry = session.query(self.password_model).filter_by(id_usuario=user_id).first()
        password_hash = generate_password_hash(new_password)
        if password_entry:
            password_entry.password_hash = password_hash
        else:
            session.add(self.password_model(id_usuario=user_id, password_hash=password_hash))

    def extract_password(self, data, is_update):
        return data.pop("nueva_password" if is_update else "password", None)