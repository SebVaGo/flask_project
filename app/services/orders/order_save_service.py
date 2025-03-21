import logging
from app.config import db
from app.services.orders.base_order_service import BaseOrderService


class OrderSaveService(BaseOrderService):
    def __init__(self):
        super().__init__()

    def save_order(self, data, order_id=None):
        session = db.session
        try:
            is_update = order_id is not None

            # 1. Validar usuario
            usuario_id = data.get("usuario_id")
            usuario = self.user_model.query.get(usuario_id)
            if not usuario:
                logging.warning("Usuario no existe o no válido")
                return {"success": False, "message": "El usuario especificado no existe."}, 400

            # 2. Validar productos
            productos = data.get("products", [])
            if not productos:
                logging.warning("No se proporcionaron productos para la orden")
                return {
                    "success": False,
                    "message": "No se proporcionaron productos para la orden."
                }, 400

            # 3. Manejo de actualización
            if is_update:
                if not self._order_exists(session, order_id):
                    logging.warning(f"Orden {order_id} no encontrada para actualización")
                    return {"success": False, "message": "Orden no encontrada"}, 404
                # Eliminar líneas actuales de la orden
                session.query(self.order_model).filter_by(orden_id=order_id).delete()
            else:
                order_id = self._get_next_order_id()

            # 4. Crear las nuevas líneas de orden
            orders_to_add = [
                self.order_model(
                    orden_id=order_id,
                    usuario_id=usuario_id,
                    producto_id=producto["producto_id"],
                    cantidad=producto["cantidad"],
                )
                for producto in productos
            ]
            session.add_all(orders_to_add)
            session.commit()

            message = (
                "Orden actualizada exitosamente"
                if is_update
                else "Orden creada exitosamente"
            )
            code = 200 if is_update else 201
            return {"success": True, "message": message, "orden_id": order_id}, code

        except Exception as e:
            session.rollback()
            logging.error(f"Error al guardar la orden: {str(e)}")
            return {"success": False, "message": "Error interno del servidor"}, 500
        finally:
            session.close()

    def _order_exists(self, session, order_id):
        try:
            order = session.query(self.order_model).filter_by(orden_id=order_id).first()
            return bool(order)
        except Exception as e:
            logging.error(f"Error in _order_exists: {str(e)}")
            return False
