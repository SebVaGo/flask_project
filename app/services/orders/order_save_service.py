from app.config import db
from app.models.order_model import OrderModel
from app.models.user_model import UserModel
from app.utils.db_session_manager import DBSessionManager
import logging

class OrderSaveService:
    def __init__(self):
        self.db_manager = DBSessionManager()
        self.order_model = OrderModel
        self.user_model = UserModel

    def get_next_order_id(self):
        last_order = self.order_model.query.order_by(self.order_model.orden_id.desc()).first()
        return (last_order.orden_id + 1) if last_order else 1

    def save_order(self, data, order_id=None):
        session = db.session
        try:
            is_update = order_id is not None

            # 1. Validar usuario
            usuario_id = data.get("usuario_id")
            usuario = self.user_model.query.get(usuario_id)
            if not usuario:
                return {"success": False, "message": "El usuario especificado no existe."}, 400

            # 2. Validar productos
            productos = data.get("products", [])
            if not productos:
                return {"success": False, "message": "No se proporcionaron productos para la orden."}, 400

            # 3. Si es actualización, validar que la orden existe y eliminar las líneas existentes
            if is_update:
                if not self._order_exists(session, order_id):
                    return {"success": False, "message": "Orden no encontrada"}, 404
                # Se eliminan las líneas actuales de la orden
                session.query(self.order_model).filter_by(orden_id=order_id).delete()
            else:
                order_id = self.get_next_order_id()

            # 4. Crear las nuevas líneas de orden
            orders_to_add = [
                self.order_model(
                    orden_id=order_id,
                    usuario_id=usuario_id,
                    producto_id=producto["producto_id"],
                    cantidad=producto["cantidad"]
                )
                for producto in productos
            ]
            session.add_all(orders_to_add)
            session.commit()

            message = "Orden actualizada exitosamente" if is_update else "Orden creada exitosamente"
            code = 200 if is_update else 201
            return {"success": True, "message": message, "orden_id": order_id}, code

        except Exception as e:
            session.rollback()
            logging.error(f"Error al guardar la orden: {str(e)}")
            return {"success": False, "message": f"Error al guardar la orden: {str(e)}"}, 500

        finally:
            session.close()

    def _order_exists(self, session, order_id):
        # Verifica si existe al menos una línea con el orden_id dado
        order = session.query(self.order_model).filter_by(orden_id=order_id).first()
        return bool(order)