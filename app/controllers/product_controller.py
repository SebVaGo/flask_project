from flask import request
from app.services.product_service import ProductService
from app.utils.forms.product_form import ProductForm
from app.utils.forms.csrf_form import CSRFForm
from app.controllers.base_controller import ApiController, ViewController

product_service = ProductService()

class ProductController(ApiController, ViewController):
    
    def list_products(self):
        products = product_service.get_all_products()
        form = CSRFForm() 
        return self.render("admin/products.html", products=products, form=form)

    def new_product_form(self):
        form = ProductForm()
        categories = product_service.get_all_categories()
        form.categoria_id.choices = [(c.id, c.nombre) for c in categories]
        return self.render("admin/product_form.html", form=form)  

    def create_product(self):
        form = ProductForm()
        categories = product_service.get_all_categories()
        form.categoria_id.choices = [(c.id, c.nombre) for c in categories]

        errors = self.validate_form(form)
        if errors:            
            return self.json_response(False, "Errores de validación", errors=errors, status=400)

        data = {
            "nombre": form.nombre.data,
            "categoria_id": form.categoria_id.data,
            "precio": form.precio.data
        }

        result = product_service.create_product(data)
        return self.json_response(result["success"], result["message"], status=200 if result["success"] else 400)

    def delete_product(self, product_id):
        result = product_service.delete_product(product_id)
        return self.json_response(result["success"], result["message"], status=200 if result["success"] else 400)

    def edit_product(self, product_id):
        product = product_service.get_product_by_id(product_id)
        if not product:
            return self.json_response(False, "Producto no encontrado", status=404)

        form = ProductForm(obj=product)
        categories = product_service.get_all_categories()
        form.categoria_id.choices = [(c.id, c.nombre) for c in categories]

        if request.method == "GET":
            return self.render("admin/product_form.html", form=form, product=product) 
        errors = self.validate_form(form)
        if errors:
            return self.json_response(False, "Errores de validación", errors=errors, status=400)

        data = {
            "nombre": form.nombre.data,
            "categoria_id": form.categoria_id.data,
            "precio": form.precio.data
        }

        result = product_service.update_product(product_id, data)
        return self.json_response(result["success"], result["message"], status=200 if result["success"] else 400)
