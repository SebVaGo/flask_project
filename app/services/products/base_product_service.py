import logging
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
