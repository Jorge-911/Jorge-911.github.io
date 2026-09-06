"""Comprueba rutas, recursos, condiciones y enlaces locales de la exportación."""
from pathlib import Path
from urllib.request import urlopen
from urllib.parse import urlsplit, unquote
from html.parser import HTMLParser
from flask import render_template
from app import app

class Enlaces(HTMLParser):
    def __init__(self):
        super().__init__(); self.urls = []
    def handle_starttag(self, tag, attrs):
        self.urls += [v for k, v in attrs if k in ('href', 'src') and v]

for ruta in ['/', '/productos', '/clientes', '/proveedores', '/facturacion']:
    with urlopen('http://127.0.0.1:5000' + ruta) as r:
        assert r.status == 200
        html = r.read().decode()
    assert '{{' not in html and '{%' not in html
    parser = Enlaces(); parser.feed(html)
    for url in parser.urls:
        if url.startswith('/'):
            assert urlopen('http://127.0.0.1:5000' + url).status == 200
    print('OK HTTP y recursos:', ruta)
with app.test_request_context('/'):
    for stock, esperado in [(5, 'Disponible'), (0, 'Agotado')]:
        html = render_template('productos.html', productos=[dict(codigo='p1', nombre='Prueba', categoria='Redes', precio=5, stock=stock)])
        assert esperado in html
    assert 'No hay productos registrados' in render_template('productos.html', productos=[])
print('OK condiciones: disponible, agotado y lista vacía')
for f in Path('avance10').glob('*.html'):
    parser = Enlaces(); parser.feed(f.read_text())
    for url in parser.urls:
        parsed = urlsplit(url)
        if not parsed.scheme and parsed.path:
            assert (f.parent / unquote(parsed.path)).is_file(), (f, url)
print('OK cinco páginas exportadas y sus enlaces/recursos locales')
print('Las dependencias externas (Bootstrap y YouTube) requieren Internet.')
