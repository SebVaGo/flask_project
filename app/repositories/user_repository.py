from app.models.user_model import User
from app.models.password_model import Password
from app.config import db

class UserRepository:

    @staticmethod
    def create_user_with_password(data, password_hash):
        try:
            user = User(**data)
            db.session.add(user)

            db.session.flush()

            password = Password(id_usuario=user.id, password_hash=password_hash)
            db.session.add(password)

            db.session.commit()

            db.session.expunge_all()

            return user
        except Exception as e:
            db.session.rollback()
            raise e
        finally :
            db.session.close()
        
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
        user = User.query.get(user_id)
        if not user:
            return None

        for key, value in data.items():
            if hasattr(user, key) and value:
                setattr(user, key, value)

        return user  
    
    @staticmethod
    def delete_by_id(user_id):
        user = User.query.get(user_id)
        if not user:
            return False 
        
        db.session.delete(user)
        db.session.commit()
        return True 
