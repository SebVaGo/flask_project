import logging

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
        
    def add_product_to_order(self, orden_id, producto_id, quantity):
        session = db.session
        try:
            # Verificar si ya existe un registro para este producto en la orden
            order_item = self._get_order_item(session, orden_id, producto_id)

            if order_item:
                # Si ya existe, se incrementa la cantidad
                order_item.cantidad += quantity
                message = "Cantidad del producto actualizada correctamente."
            else:
                new_item = self.order_model(
                    orden_id=orden_id,
                    producto_id=producto_id,
                    cantidad=quantity 
                )
                session.add(new_item)
                message = "Producto agregado a la orden exitosamente."

            self.db_manager.commit()
            return {"success": True, "message": message}, 200
        except Exception as e:
            logging.error(f"Error al agregar el producto a la orden: {str(e)}")
            return {"success": False, "message": f"Error al agregar producto: {str(e)}"}, 500


    def delete_order_product(self, orden_id, producto_id=None):
        session = db.session
        try:
            if producto_id is not None:
                # Eliminar un producto específico de la orden.
                order_item = self._get_order_item(session, orden_id, producto_id)
                if not order_item:
                    return {"success": False, "message": "Producto en la orden no encontrado."}, 404
                session.delete(order_item)
                message = "Producto eliminado correctamente de la orden."
            else:
                order_items = self._get_all_order_items(session, orden_id)
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
            return {"success": False, "message": f"Error al eliminar: {str(e)}"}, 500

        finally:
            session.close()

    def _get_order_item(self, session, orden_id, producto_id):
        return session.query(self.order_model).filter_by(
            orden_id=orden_id, producto_id=producto_id
        ).first()
    
    def _get_all_order_items(self, session, orden_id):
        return session.query(self.order_model).filter_by(orden_id=orden_id).all()
    
