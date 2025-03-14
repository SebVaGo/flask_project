from flask import request, flash, render_template
from app.controllers.base_controller import ApiController, ViewController
from app.services.orders.order_get_service import OrderQueryService
from app.services.orders.order_delete_service import OrderManagementService
from app.services.orders.order_save_service import OrderSaveService
from app.services.products.product_service import ProductService


class BaseOrderController(ApiController, ViewController):

    def __init__(self):
        super().__init__()
        self.order_query_service = OrderQueryService()
        self.order_management_service = OrderManagementService()
        self.order_save_service = OrderSaveService()
        self.product_query_service = ProductService()

    def render_order_form(self, form, template="admin/orders.html"):
        return self.render(template, form=form)
