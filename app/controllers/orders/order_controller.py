from app.controllers.orders.order_crud_controller import OrderCrudController
from app.utils.decorators import admin_and_login_required_for_all_methods


@admin_and_login_required_for_all_methods
class OrderController(OrderCrudController):
    pass
