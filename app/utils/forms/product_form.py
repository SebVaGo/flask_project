from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, FloatField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange

class ProductForm(FlaskForm):
    nombre = StringField("Nombre del Producto", validators=[DataRequired(), Length(max=100)])
    categoria_id = SelectField("Categoría", coerce=int, validators=[DataRequired()])
    precio = FloatField("Precio", validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField("Guardar Producto")
