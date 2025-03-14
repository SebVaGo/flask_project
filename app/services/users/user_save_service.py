import logging
from app.config import db
from app.models.user_model import UserModel


class UserSaveService:

    def __init__(self, client_type_service, password_service):
        self.client_type_service = client_type_service
        self.password_service = password_service

    def _validate_email(self, session, email, user_id=None):

        if email:
            query = session.query(UserModel).filter_by(correo=email)
            if user_id is not None:
                query = query.filter(UserModel.id != user_id)
            if query.first():
                return "El correo ya está en uso."
        return None

    def _validate_client_type(self, data):

        if "tipo_cliente_id" in data:
            tipo_cliente = self.client_type_service.get_type_by_id(data["tipo_cliente_id"])
            if not tipo_cliente:
                return "El tipo de cliente no existe"
        return None

    def save_user(self, data, user_id=None):

        session = db.session
        try:
            is_update = user_id is not None

            # 1. Obtener (o validar) usuario si es actualización
            usuario, error, status_code = self._get_user_if_update(session, user_id)
            if error:
                return error, status_code

            # 2. Validar email y tipo de cliente
            error, status_code = self._check_email_and_client(session, data, user_id)
            if error:
                return error, status_code

            # 3. Extraer la contraseña según sea update o create
            nueva_password = self._extract_password(data, is_update)

            # 4. Actualizar usuario existente o crear uno nuevo
            if is_update:
                self._update_existing_user(usuario, data)
            else:
                usuario = self._create_new_user(session, data)

            # 5. Manejar contraseña
            if nueva_password:
                self._update_password(session, usuario, nueva_password, is_update)

            session.commit()
            mensaje = "Usuario actualizado correctamente." if is_update else "Usuario registrado exitosamente"
            return {"success": True, "message": mensaje}, 200 if is_update else 201

        except Exception as e:
            session.rollback()
            logging.error(f"Error en operación de usuario: {str(e)}")
            return {"success": False, "message": "Error interno del servidor"}, 500
        finally:
            session.close()

    def _get_user_if_update(self, session, user_id):

        if user_id is not None:
            usuario = session.query(UserModel).get(user_id)
            if not usuario:
                return None, {"success": False, "message": "Usuario no encontrado."}, 404
            return usuario, None, None
        return None, None, None

    def _check_email_and_client(self, session, data, user_id=None):

        email_error = self._validate_email(session, data.get("correo"), user_id)
        if email_error:
            return {"success": False, "message": email_error}, 400

        client_error = self._validate_client_type(data)
        if client_error:
            return {"success": False, "message": client_error}, 400

        return None, None

    def _extract_password(self, data, is_update):

        return data.pop("nueva_password" if is_update else "password", None)

    def _update_existing_user(self, usuario, data):

        for key, value in data.items():
            if hasattr(usuario, key) and value is not None:
                setattr(usuario, key, value)

    def _create_new_user(self, session, data):

        usuario = UserModel(**data, status="activo")
        session.add(usuario)
        session.flush()
        return usuario

    def _update_password(self, session, usuario, nueva_password, is_update):
 
        if is_update:
            self.password_service.update_password(session, usuario.id, nueva_password)
        else:
            self.password_service.create_password(session, usuario.id, nueva_password)
