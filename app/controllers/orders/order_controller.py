from app.controllers.orders.order_create_controller import OrderCreateController
from app.controllers.orders.order_list_controller import OrderListController
from app.controllers.orders.order_manage_controller import OrderManageController
from app.controllers.orders.order_update_controller import OrderUpdateController


class OrderController(OrderCreateController, OrderListController, OrderManageController, OrderUpdateController):
    pass
