from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, InputRequired, Length, Email, NumberRange, Regexp


def limpiar(valor):
    return valor.strip() if isinstance(valor, str) else valor


class ProveedorForm(FlaskForm):
    """Campos reutilizables para registro y futura edición."""
    empresa = StringField("Empresa", filters=[limpiar], validators=[DataRequired(message="Este campo es obligatorio."), Length(min=2, max=100, message="Debe contener entre 2 y 100 caracteres.")])
    producto = StringField("Productos o servicios", filters=[limpiar], validators=[DataRequired(message="Este campo es obligatorio."), Length(min=3, max=150, message="Debe contener entre 3 y 150 caracteres.")])
    contacto = StringField("Correo electrónico", filters=[limpiar], validators=[DataRequired(message="Este campo es obligatorio."), Length(max=120), Email(message="Ingrese un correo electrónico válido.")])
    ciudad = StringField("Ciudad", filters=[limpiar], validators=[DataRequired(message="Este campo es obligatorio."), Length(min=2, max=60, message="Debe contener entre 2 y 60 caracteres.")])
    submit = SubmitField("Guardar registro")
