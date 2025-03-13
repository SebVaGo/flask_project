from app.controllers.orders.order_create_controller import OrderCreateController
from app.controllers.orders.order_list_controller import OrderListController
from app.controllers.orders.order_manage_controller import OrderManageController


class OrderController(OrderCreateController, OrderListController, OrderManageController):
    pass
