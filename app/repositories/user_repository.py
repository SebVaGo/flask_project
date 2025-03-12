from app.models.user_model import User
from app.config import db

class UserRepository:
    @staticmethod
    def create_user(data):
        user = User(**data)
        db.session.add(user)
        db.session.commit()
        return user
    
    @staticmethod
    def get_user_by_id(user_id):
        return User.query.get(user_id)
    
    @staticmethod
    def get_user_by_email(correo):
        return User.query.filter_by(correo=correo).first()
    
    @staticmethod
    def get_all_users():
        return User.query.all()
    
    @staticmethod
    def update_by_id(user_id, data):
        """ Actualiza un usuario por ID """
        user = User.query.get(user_id)
        if not user:
            return None

        for key, value in data.items():
            if hasattr(user, key) and value:
                setattr(user, key, value)

        db.session.commit()
        return user
    
    @staticmethod
    def delete_by_id(user_id):
        user = User.query.get(user_id)
        if not user:
            return False 
        
        db.session.delete(user)
        db.session.commit()
        return True 
