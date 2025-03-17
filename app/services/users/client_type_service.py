import logging
from app.services.users.base_user_service import BaseUserService
from app.utils.db_session_manager import AltDBSessionManager

class ClientTypeService(BaseUserService):

    def __init__(self):
        super().__init__()

    def get_all_types(self):
        try:
            with AltDBSessionManager() as session:
                results = session.query(
                    self.client_type_model.id,
                    self.client_type_model.nombre
                ).all()
                return [{"id": row[0], "nombre": row[1]} for row in results]
        except Exception as e:
            logging.error(f"Error in get_all_types: {str(e)}")
            raise Exception("Ocurrió un error al obtener los tipos de cliente.")

    def get_client_types(self):
        tipos = self.get_all_types()
        return [(tipo["id"], tipo["nombre"]) for tipo in tipos]


    def validate_and_get_client_type(self, data, session):
        try:
            if "tipo_cliente_id" in data:
                tipo = session.query(self.client_type_model).get(data["tipo_cliente_id"])
                if not tipo:
                    return "El tipo de cliente no existe", None
                return None, tipo
            return None, None
        except Exception as e:
            logging.error(f"Error in validate_and_get_client_type: {str(e)}")
            raise Exception("Ocurrió un error al validar el tipo de cliente.")
