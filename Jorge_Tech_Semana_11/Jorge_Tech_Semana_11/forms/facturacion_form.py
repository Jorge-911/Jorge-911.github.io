from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, InputRequired, Length, Email, NumberRange, Regexp


def limpiar(valor):
    return valor.strip() if isinstance(valor, str) else valor


class FacturacionForm(FlaskForm):
    """Campos reutilizables para registro y futura edición."""
    numero = StringField("Número de factura", filters=[limpiar], validators=[DataRequired(message="Este campo es obligatorio."), Length(min=2, max=20, message="Debe contener entre 2 y 20 caracteres.")])
    cliente = StringField("Cliente", filters=[limpiar], validators=[DataRequired(message="Este campo es obligatorio."), Length(min=3, max=100, message="Debe contener entre 3 y 100 caracteres.")])
    detalle = StringField("Detalle", filters=[limpiar], validators=[DataRequired(message="Este campo es obligatorio."), Length(min=5, max=200, message="Debe contener entre 5 y 200 caracteres.")])
    total = DecimalField("Total ($)", validators=[InputRequired(message="Ingrese un número."), NumberRange(min=0.01, max=999999.99, message="Ingrese un valor entre 0.01 y 999999.99.")])
    estado = SelectField("Estado", choices=['Pendiente', 'Pagada'], validators=[DataRequired(message="Seleccione una opción.")], validate_choice=True)
    submit = SubmitField("Guardar registro")
