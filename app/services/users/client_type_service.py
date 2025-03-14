from app.services.users.base_user_service import BaseUserService

class ClientTypeService(BaseUserService):

    def __init__(self):
        super().__init__()

    def get_all_types(self):
        return self.client_type_model.query.all()

    def get_type_by_id(self, tipo_cliente_id):
        return self.client_type_model.query.get(tipo_cliente_id)
    
    def validate_client_type(self, data):
        
        if "tipo_cliente_id" in data:
            tipo_cliente = self.get_type_by_id(data["tipo_cliente_id"])
            if not tipo_cliente:
                return "El tipo de cliente no existe"
        return None