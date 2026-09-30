from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Length


def limpiar(valor):
    return valor.strip() if isinstance(valor, str) else valor


class LoginForm(FlaskForm):
    """Formulario de acceso con validaciones Flask-WTF y CSRF."""
    usuario = StringField("Usuario", filters=[limpiar], validators=[
        DataRequired(message="Ingrese su usuario."),
        Length(min=3, max=50, message="El usuario debe tener entre 3 y 50 caracteres."),
    ])
    password = PasswordField("Contraseña", validators=[DataRequired(message="Ingrese su contraseña.")])
    recordar = BooleanField("Mantener la sesión iniciada")
    submit = SubmitField("Iniciar sesión")
