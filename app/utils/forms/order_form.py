# app/utils/forms/order_form.py
from wtforms import Form, IntegerField, FieldList, FormField
from wtforms.validators import DataRequired, NumberRange, InputRequired

class ProductForm(Form):
    producto_id = IntegerField('producto_id', validators=[DataRequired()])
    cantidad = IntegerField('cantidad', validators=[DataRequired(), NumberRange(min=1)])

class OrderForm(Form):
    usuario_id = IntegerField('usuario_id', validators=[DataRequired()])
    products = FieldList(FormField(ProductForm), validators=[DataRequired()])

class UpdateQuantityForm(Form):
    cantidad = IntegerField("cantidad", validators=[
        DataRequired(message="Cantidad requerida."),
        NumberRange(min=1, message="La cantidad debe ser al menos 1.")
    ])
