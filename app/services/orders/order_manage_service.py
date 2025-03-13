from app.config import db
from app.models.order_model import OrderModel
from app.utils.db_session_manager import DBSessionManager


class OrderManagementService:

    def __init__(self):
        self.db_manager = DBSessionManager()
        self.order_model = OrderModel

    def update_order_quantity(self, orden_id, producto_id, nueva_cantidad):
        order = self.order_model.query.filter_by(orden_id=orden_id, producto_id=producto_id).first()

        if not order:
            return {"success": False, "message": "La orden especificada no existe."}

        try:
            order.cantidad = nueva_cantidad
            self.db_manager.commit()
            return {"success": True, "message": "Cantidad actualizada correctamente."}
        except Exception as e:
            return {"success": False, "message": f"Error al actualizar la cantidad: {str(e)}"}

    def delete_order_product(self, orden_id, producto_id):
        order = self.order_model.query.filter_by(orden_id=orden_id, producto_id=producto_id).first()

        if not order:
            return {"success": False, "message": "Producto en la orden no encontrado."}

        try:
            db.session.delete(order)
            self.db_manager.commit()
            return {"success": True, "message": "Producto eliminado correctamente."}
        except Exception as e:
            return {"success": False, "message": f"Error al eliminar el producto: {str(e)}"}
