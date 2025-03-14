import logging
from app.config import db
from app.services.orders.base_order_service import BaseOrderService
from app.services.orders.order_get_service import OrderQueryService


class OrderManagementService(BaseOrderService):

    def __init__(self):
        super().__init__()
        self.order_query_service = OrderQueryService()

    def delete_order_product(self, orden_id, producto_id=None):
        session = db.session
        try:
            if producto_id is not None:
                # Eliminar un producto específico de la orden.
                order_item = self.order_query_service.get_order_item(
                    session, orden_id, producto_id
                )
                if not order_item:
                    return (
                        {"success": False, "message": "Producto en la orden no encontrado."},
                        404,
                    )
                session.delete(order_item)
                message = "Producto eliminado correctamente de la orden."
            else:
                order_items = self.order_query_service.get_all_order_items(session, orden_id)
                if not order_items:
                    return {"success": False, "message": "Orden no encontrada."}, 404
                for item in order_items:
                    session.delete(item)
                message = "Orden eliminada correctamente."

            self.db_manager.commit()
            return {"success": True, "message": message}, 200

        except Exception as e:
            session.rollback()
            logging.error(f"Error al eliminar la orden o el producto: {str(e)}")
            return {"success": False, "message": "Error interno del servidor"}, 500

        finally:
            session.close()
