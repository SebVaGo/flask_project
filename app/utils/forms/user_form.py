from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Optional, Regexp

def validate_phone(form, field):
    if not field.data.isdigit():
        raise ValueError("El teléfono solo debe contener números.")

class UserForm(FlaskForm):
    primer_nombre = StringField("Primer Nombre", validators=[
        DataRequired(message="El primer nombre es obligatorio."),
        Length(min=1, max=50, message="El primer nombre debe tener entre 1 y 50 caracteres.")
    ])

    segundo_nombre = StringField("Segundo Nombre", validators=[
        Optional(),  # No es obligatorio
        Length(max=50, message="El segundo nombre no puede tener más de 50 caracteres.")
    ])

    apellido_paterno = StringField("Apellido Paterno", validators=[
        DataRequired(message="El apellido paterno es obligatorio."),
        Length(min=1, max=50, message="El apellido paterno debe tener entre 1 y 50 caracteres.")
    ])

    apellido_materno = StringField("Apellido Materno", validators=[
        DataRequired(message="El apellido materno es obligatorio."),
        Length(min=1, max=50, message="El apellido materno debe tener entre 1 y 50 caracteres.")
    ])

    correo = EmailField("Correo", validators=[
        DataRequired(message="El correo es obligatorio."),
        Email(message="El formato del correo no es válido.")
    ])

    telefono = StringField("Teléfono", validators=[
        DataRequired(message="El teléfono es obligatorio."),
        Regexp(r'^\d{9,15}$', message="El teléfono debe contener entre 7 y 15 dígitos.")
    ])

    password = PasswordField("Contraseña", validators=[
        DataRequired(message="La contraseña es obligatoria."),
        Length(min=6, message="La contraseña debe tener al menos 6 caracteres.")
    ])

    submit = SubmitField("Registrar")
    

class UserUpdateForm(FlaskForm):
    primer_nombre = StringField("Primer Nombre", validators=[
        DataRequired(message="El primer nombre es obligatorio."),
        Length(min=1, max=50, message="Debe tener entre 1 y 50 caracteres.")
    ])

    segundo_nombre = StringField("Segundo Nombre", validators=[
        Optional(),
        Length(max=50, message="No puede tener más de 50 caracteres.")
    ])

    apellido_paterno = StringField("Apellido Paterno", validators=[
        DataRequired(message="El apellido paterno es obligatorio."),
        Length(min=1, max=50, message="Debe tener entre 1 y 50 caracteres.")
    ])

    apellido_materno = StringField("Apellido Materno", validators=[
        DataRequired(message="El apellido materno es obligatorio."),
        Length(min=1, max=50, message="Debe tener entre 1 y 50 caracteres.")
    ])

    correo = EmailField("Correo", validators=[
        DataRequired(message="El correo es obligatorio."),
        Email(message="El formato del correo no es válido."),
        Length(max=100, message="No puede tener más de 100 caracteres.")
    ])

    telefono = StringField("Teléfono", validators=[
        DataRequired(message="El teléfono es obligatorio."),
        Regexp(r'^\d{9,9}$', message="El teléfono debe contener 9 dígitos.")
    ])

    submit = SubmitField("Actualizar")
