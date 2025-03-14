from app.utils.db_session_manager import DBSessionManager
from app.models.categoy_product_model import CategoryModel
from app.models.order_model import OrderModel
from app.models.product_model import ProductModel

class BaseProductService:
    def __init__(self):
        self.db_manager = DBSessionManager()
        self.category_model = CategoryModel
        self.order_model = OrderModel
        self.product_model = ProductModel

    def get_existing_product(self, session, product_id):
        product = session.query(self.product_model).get(product_id)
        if not product:
            return None, {"success": False, "message": "Producto no encontrado"}, 404
        return product, None, None