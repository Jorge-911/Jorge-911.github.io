"""Comprueba rutas, recursos, condiciones y enlaces locales de la exportación."""
from pathlib import Path
from urllib.parse import urlsplit, unquote
from html.parser import HTMLParser
from flask import render_template
from app import app
from forms.eliminar_form import EliminarForm

class Enlaces(HTMLParser):
    def __init__(self):
        super().__init__(); self.urls = []
    def handle_starttag(self, tag, attrs):
        self.urls += [v for k, v in attrs if k in ('href', 'src') and v]

cliente = app.test_client()
for ruta in ['/', '/login', '/registro', '/static/css/style.css', '/static/js/script.js', '/static/img/tecnologia.svg']:
    respuesta = cliente.get(ruta)
    assert respuesta.status_code == 200, ruta
    assert '{{' not in respuesta.text and '{%' not in respuesta.text
    print('OK ruta pública o recurso:', ruta)
for ruta in ['/dashboard', '/productos', '/clientes', '/proveedores', '/facturacion']:
    respuesta = cliente.get(ruta)
    assert respuesta.status_code == 302 and '/login' in respuesta.location, ruta
    print('OK protección de ruta:', ruta)
with app.test_request_context('/'):
    for stock, esperado in [(5, 'Disponible'), (0, 'Agotado')]:
        html = render_template('productos.html', productos=[dict(id=1, codigo='p1', nombre='Prueba', categoria='Redes', proveedor='Proveedor de prueba', precio=5, stock=stock)], form_eliminar=EliminarForm())
        assert esperado in html
    assert 'No hay productos registrados' in render_template('productos.html', productos=[], form_eliminar=EliminarForm())
print('OK condiciones: disponible, agotado y lista vacía')
for f in Path('avance10').glob('*.html'):
    parser = Enlaces(); parser.feed(f.read_text())
    for url in parser.urls:
        parsed = urlsplit(url)
        if not parsed.scheme and parsed.path:
            assert (f.parent / unquote(parsed.path)).is_file(), (f, url)
print('OK cinco páginas exportadas y sus enlaces/recursos locales')
print('Las dependencias externas (Bootstrap y YouTube) requieren Internet.')
