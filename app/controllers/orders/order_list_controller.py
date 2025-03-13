from app.controllers.orders.base_order_controller import BaseOrderController
from app.utils.forms.csrf_form import CSRFForm


class OrderListController(BaseOrderController):
    """Maneja la visualización de órdenes."""

    def list_orders(self):
        """Muestra la lista de órdenes."""
        orders = self.order_query_service.get_all_orders()
        form = CSRFForm()
        return self.render("admin/orders.html", orders=orders, form=form)
