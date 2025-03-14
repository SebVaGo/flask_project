from app.services.orders.order_delete_service import OrderManagementService
from app.services.orders.order_get_service import OrderQueryService
from app.services.orders.order_save_service import OrderSaveService


class OrderService(OrderManagementService, OrderQueryService, OrderSaveService):
    def __init__(self):
        super().__init__()