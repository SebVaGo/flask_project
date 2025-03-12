from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Optional, Regexp

class BaseUserForm(FlaskForm):

    primer_nombre = StringField("Primer Nombre", validators=[
        DataRequired(message="El primer nombre es obligatorio."),
        Length(min=1, max=50, message="El primer nombre debe tener entre 1 y 50 caracteres."),
        Regexp(r"^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$", message="El primer nombre solo puede contener letras y espacios.")
    ])

    segundo_nombre = StringField("Segundo Nombre", validators=[
        Optional(),
        Length(max=50, message="El segundo nombre no puede tener más de 50 caracteres."),
        Regexp(r"^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]*$", message="El segundo nombre solo puede contener letras y espacios.")
    ])

    apellido_paterno = StringField("Apellido Paterno", validators=[
        DataRequired(message="El apellido paterno es obligatorio."),
        Length(min=1, max=50, message="El apellido paterno debe tener entre 1 y 50 caracteres."),
        Regexp(r"^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$", message="El apellido paterno solo puede contener letras y espacios.")
    ])

    apellido_materno = StringField("Apellido Materno", validators=[
        DataRequired(message="El apellido materno es obligatorio."),
        Length(min=1, max=50, message="El apellido materno debe tener entre 1 y 50 caracteres."),
        Regexp(r"^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$", message="El apellido materno solo puede contener letras y espacios.")
    ])

    correo = StringField("Correo", validators=[
        DataRequired(message="El correo es obligatorio."),
        Email(message="El formato del correo no es válido."),
        Length(max=100, message="El correo no puede tener más de 100 caracteres.")
    ])

    telefono = StringField("Teléfono", validators=[
        DataRequired(message="El teléfono es obligatorio."),
        Regexp(r'^\d{9}$', message="El teléfono debe contener exactamente 9 dígitos numéricos.")
    ])

class UserForm(BaseUserForm):
    password = PasswordField("Contraseña", validators=[
        DataRequired(message="La contraseña es obligatoria."),
        Length(min=8, message="La contraseña debe tener al menos 8 caracteres."),
        Regexp(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)', 
               message="La contraseña debe contener al menos una minúscula, una mayúscula y un número.")
    ])
    
    submit = SubmitField("Registrar")

class UserUpdateForm(BaseUserForm):
    submit = SubmitField("Actualizar Usuario")
