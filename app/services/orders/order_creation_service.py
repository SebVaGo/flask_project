from app.config import db
from app.models.order_model import OrderModel
from app.models.user_model import UserModel
from app.utils.db_session_manager import DBSessionManager


class OrderCreationService:

    def __init__(self):
        self.db_manager = DBSessionManager()
        self.order_model = OrderModel
        self.user_model = UserModel

    def get_next_order_id(self):
        last_order = self.order_model.query.order_by(self.order_model.orden_id.desc()).first()
        return (last_order.orden_id + 1) if last_order else 1

    def create_order(self, data):
        usuario_id = data.get("usuario_id")
        usuario = self.user_model.query.get(usuario_id)

        if not usuario:
            return {"success": False, "message": "El usuario especificado no existe."}

        productos = data.get("products", [])
        if not productos:
            return {"success": False, "message": "No se proporcionaron productos para la orden."}

        orden_id = self.get_next_order_id()

        orders_to_add = [
            self.order_model(
                orden_id=orden_id,
                usuario_id=usuario_id,
                producto_id=producto["producto_id"],
                cantidad=producto["cantidad"]
            )
            for producto in productos
        ]

        try:
            db.session.add_all(orders_to_add)
            self.db_manager.commit()
            return {"success": True, "message": "Orden creada con éxito", "orden_id": orden_id}
        except Exception as e:
            return {"success": False, "message": f"Error al guardar la orden: {str(e)}"}
