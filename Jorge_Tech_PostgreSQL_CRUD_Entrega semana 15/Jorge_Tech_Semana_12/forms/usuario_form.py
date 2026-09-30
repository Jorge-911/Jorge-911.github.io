from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Length, Regexp


def limpiar(valor):
    return valor.strip() if isinstance(valor, str) else valor


class UsuarioForm(FlaskForm):
    """Registro de usuarios autorizados para Jorge Tech."""
    usuario = StringField("Nombre de usuario", filters=[limpiar], validators=[
        DataRequired(message="Este campo es obligatorio."),
        Length(min=3, max=50, message="Debe contener entre 3 y 50 caracteres."),
        Regexp(r"^[A-Za-z0-9_.-]+$", message="Use letras, números, punto, guion o guion bajo."),
    ])
    password = PasswordField("Contraseña", validators=[
        DataRequired(message="Este campo es obligatorio."),
        Length(min=8, max=128, message="La contraseña debe tener entre 8 y 128 caracteres."),
    ])
    confirmar_password = PasswordField("Confirmar contraseña", validators=[
        DataRequired(message="Confirme la contraseña."),
        EqualTo("password", message="Las contraseñas no coinciden."),
    ])
    submit = SubmitField("Crear usuario")
