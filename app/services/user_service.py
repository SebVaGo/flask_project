from flask import request
from app.repositories.user_repository import UserRepository
from app.repositories.password_repository import PasswordRepository
from werkzeug.security import generate_password_hash
from flask_wtf.csrf import validate_csrf

class UserService: 
    @staticmethod
    def create_user(data):

        """Validación de email existente"""
        emai_existente = UserRepository.get_user_by_email(data["correo"])
        if emai_existente:
            return {"message": "El correo ya está en uso."}, 400
        
        """Hash de contraseña"""
        data = request.form.to_dict()  
        password_hash = generate_password_hash(data.pop("password")) 

        """Crea un nuevo usuario."""
        user = UserRepository.create_user(data)

        """Crea la contraseña del usuario."""
        if user:
            PasswordRepository.create_password(user.id, password_hash)
            return {"message": "Usuario registrado exitosamente"}, 201
        
        return {"message": "Error al registrar usuario"}, 500
    
    @staticmethod
    def get_all_users():
        users = UserRepository.get_all_users()
        return users 
        
    @staticmethod
    def get_user_by_id(user_id):
        return UserRepository.get_user_by_id(user_id)
    
    @staticmethod
    def actualizar_usuario(user_id, data):
        """Actualiza los datos de un usuario y devuelve el resultado"""
        try:
            usuario_actualizado = UserRepository.update_by_id(user_id, data)
            if usuario_actualizado:
                return {"success": True, "message": "Usuario actualizado correctamente."}
            else:
                return {"success": False, "message": "No se pudo actualizar el usuario."}
        except Exception as e:
            return {"success": False, "message": f"Error: {str(e)}"}
        
    @staticmethod
    def delete_user(user_id):
        """Elimina físicamente un usuario de la base de datos"""
        try:
            usuario_eliminado = UserRepository.delete_by_id(user_id)  # 🔥 Llama al repositorio

            if usuario_eliminado:  # 🔥 Debe retornar True o False, no una tupla
                return {"success": True, "message": "Usuario eliminado correctamente."}
            else:
                return {"success": False, "message": "No se pudo eliminar el usuario."}

        except Exception as e:
            return {"success": False, "message": f"Error interno: {str(e)}"}
