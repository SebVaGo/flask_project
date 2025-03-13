from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, FloatField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange, Regexp

class ProductForm(FlaskForm):
    nombre = StringField(
        "Nombre del Producto",
        validators=[
            DataRequired(message="El nombre del producto es obligatorio."),
            Length(max=100, message="El nombre no puede superar los 100 caracteres.")
        ]
    )

    categoria_id = SelectField(
        "Categoría",
        coerce=int,
        validators=[DataRequired(message="Debe seleccionar una categoría.")]
    )

    precio = FloatField(
        "Precio",
        validators=[
            DataRequired(message="El precio es obligatorio."),
            NumberRange(min=0, message="El precio debe ser un número positivo."),
        ]
    )

    submit = SubmitField("Guardar Producto")
