from marshmallow import Schema, fields, validate, ValidationError

def validate_phone(value):
    """ Valida que el número de teléfono tenga exactamente 9 dígitos numéricos. """
    if not value.isdigit():
        raise ValidationError("El teléfono solo debe contener números.")
    if len(value) != 9:
        raise ValidationError("El teléfono debe tener exactamente 9 dígitos.")


class UserSchema(Schema): 
    primer_nombre = fields.String(
        required=True,
        validate=validate.Length(min=1, max=50, error="El primer nombre debe tener entre 1 y 50 caracteres."),
        error_messages={"required": "El primer nombre es obligatorio."}
    )
    
    segundo_nombre = fields.String(
        missing='',
        validate=validate.Length(max=50, error="El segundo nombre no puede tener más de 50 caracteres.")
    )

    apellido_paterno = fields.String(
        required=True,
        validate=validate.Length(min=1, max=50, error="El apellido paterno debe tener entre 1 y 50 caracteres."),
        error_messages={"required": "El apellido paterno es obligatorio."}
    )

    apellido_materno = fields.String(
        required=True,
        validate=validate.Length(min=1, max=50, error="El apellido materno debe tener entre 1 y 50 caracteres."),
        error_messages={"required": "El apellido materno es obligatorio."}
    )

    correo = fields.Email(
        required=True,
        error_messages={
            "required": "El correo es obligatorio.",
            "invalid": "El formato del correo no es válido."
        }
    )

    telefono = fields.String(
        required=True,
        validate=validate_phone,
        error_messages={"required": "El teléfono es obligatorio."}
    )

    password = fields.String(
        required=True,
        validate=validate.Length(min=6, error="La contraseña debe tener al menos 6 caracteres."),
        error_messages={"required": "La contraseña es obligatoria."}
    )

