from decimal import Decimal
from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, InputRequired, Length, Email, NumberRange, Regexp, ValidationError


def limpiar(valor):
    return valor.strip() if isinstance(valor, str) else valor


class ProductoForm(FlaskForm):
    """Campos reutilizables para registro y futura edición."""
    codigo = StringField("Código", filters=[limpiar], validators=[DataRequired(message="Este campo es obligatorio."), Length(min=2, max=20, message="Debe contener entre 2 y 20 caracteres.")])
    nombre = StringField("Nombre", filters=[limpiar], validators=[DataRequired(message="Este campo es obligatorio."), Length(min=2, max=100, message="Debe contener entre 2 y 100 caracteres.")])
    categoria = StringField("Categoría", filters=[limpiar], validators=[DataRequired(message="Este campo es obligatorio."), Length(min=2, max=60, message="Debe contener entre 2 y 60 caracteres.")])
    precio = DecimalField("Precio ($)", validators=[InputRequired(message="Ingrese un número."), NumberRange(min=0.01, max=999999.99, message="Ingrese un valor entre 0.01 y 999999.99.")])
    stock = IntegerField("Stock", validators=[InputRequired(message="Ingrese un número."), NumberRange(min=0, max=1000000, message="Ingrese un valor entre 0 y 1000000.")])
    submit = SubmitField("Guardar registro")

    def validate_precio(self, field):
        if field.data is not None and field.data.is_finite():
            if field.data != field.data.quantize(Decimal('0.01')):
                raise ValidationError("El precio debe tener como máximo dos decimales.")
