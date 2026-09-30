from flask_wtf import FlaskForm
from wtforms import SubmitField


class EliminarForm(FlaskForm):
    """Formulario mínimo que protege DELETE con el token CSRF."""
    submit = SubmitField("Eliminar")
