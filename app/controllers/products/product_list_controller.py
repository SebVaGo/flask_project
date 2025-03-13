from app.controllers.products.base_product_controller import BaseProductController
from app.utils.forms.csrf_form import CSRFForm


class ProductListController(BaseProductController):

    def list_products(self):
        products = self.product_service.get_all_products()
        form = CSRFForm()
        return self.render("admin/products.html", products=products, form=form)
