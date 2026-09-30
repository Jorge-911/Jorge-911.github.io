from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, InputRequired, Length, Email, NumberRange, Regexp


def limpiar(valor):
    return valor.strip() if isinstance(valor, str) else valor


class ClienteForm(FlaskForm):
    """Campos reutilizables para registro y futura edición."""
    nombre = StringField("Nombre completo", filters=[limpiar], validators=[DataRequired(message="Este campo es obligatorio."), Length(min=3, max=100, message="Debe contener entre 3 y 100 caracteres.")])
    servicio = SelectField("Servicio", choices=['Soporte técnico', 'Redes y conectividad', 'Productos tecnológicos'], validators=[DataRequired(message="Seleccione una opción.")], validate_choice=True)
    telefono = StringField("Teléfono", filters=[limpiar], validators=[DataRequired(message="Este campo es obligatorio."), Regexp(r"^0[0-9]{8,9}$", message="Ingrese 9 o 10 dígitos, comenzando por 0.")])
    estado = SelectField("Estado", choices=['Pendiente', 'En proceso', 'Atendido'], validators=[DataRequired(message="Seleccione una opción.")], validate_choice=True)
    submit = SubmitField("Guardar registro")
