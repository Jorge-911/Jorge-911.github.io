"""Prueba HTTP real, validación/CSRF e independencia de dos procesos Flask."""
import os
import re
import sqlite3
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from http.cookiejar import CookieJar
from urllib.request import build_opener, HTTPCookieProcessor
from urllib.parse import urlencode

BASE = 'http://127.0.0.1:5000'
ROOT = Path(__file__).resolve().parent

def iniciar(db):
    env = dict(os.environ, JORGE_TECH_DB=str(db))
    proceso = subprocess.Popen([sys.executable, str(ROOT / 'app.py')], env=env,
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for _ in range(50):
        if proceso.poll() is not None:
            raise RuntimeError('No se pudo iniciar Flask. Libere el puerto 5000.')
        try:
            build_opener().open(BASE, timeout=1).close()
            return proceso
        except OSError:
            time.sleep(.1)
    proceso.terminate(); proceso.wait()
    raise RuntimeError('Flask no respondió.')

def detener(p):
    p.terminate(); p.wait(timeout=10)

def ejecutar():
    with tempfile.TemporaryDirectory() as directorio:
        db = Path(directorio) / 'ferreteria.db'
        def contar():
            conn = sqlite3.connect(db)
            try:return conn.execute('SELECT COUNT(*) FROM productos').fetchone()[0]
            finally:conn.close()
        p = iniciar(db)
        try:
            cliente = build_opener(HTTPCookieProcessor(CookieJar()))
            def get(ruta):
                with cliente.open(BASE + ruta) as r:
                    assert r.status == 200
                    return r.read().decode()
            def enviar(datos):
                with cliente.open(BASE + '/productos/nuevo', urlencode(datos).encode()) as r:
                    assert r.status == 200
                    return r.read().decode()
            token = re.search(r'name="csrf_token"[^>]*value="([^"]+)"', get('/productos/nuevo')).group(1)
            datos = dict(codigo='SQL-TEST', nombre="Monitor O'Connor", categoria='Pantallas', precio='25.50', stock='0', csrf_token=token)
            for cambios in [dict(csrf_token=''),dict(csrf_token='alterado'),dict(nombre=''),dict(precio='-1'),dict(stock='-1'),dict(stock='1.5'),dict(precio='NaN'),dict(precio='1.234')]:
                enviar(dict(datos, **cambios)); assert contar() == 0
            print('OK: datos inválidos y CSRF incorrecto no generan INSERT.')
            html = enviar(datos)
            assert contar() == 1 and 'Agotado' in html and '<table' in html
            assert 'Producto guardado correctamente en SQLite.' in html
            print('OK: POST válido → INSERT → SELECT → tabla HTML; stock cero aceptado.')
            enviar(dict(datos,codigo='sql-test'))
            assert contar() == 1
            print('OK: código duplicado rechazado por restricción UNIQUE.')
            payload="x'); DROP TABLE productos;--"
            enviar(dict(datos,codigo='SQL-TEXT',nombre=payload))
            assert contar() == 2
            conn=sqlite3.connect(db)
            try:
                assert conn.execute('SELECT nombre, precio_centavos FROM productos WHERE codigo = ?',('SQL-TEXT',)).fetchone() == (payload,2550)
            finally:conn.close()
            print('OK: SQL parametrizado guarda comillas como texto; dinero exacto en centavos.')
            for ruta in ['/','/productos','/clientes','/proveedores','/facturacion','/clientes/nuevo','/proveedores/nuevo','/facturacion/nuevo']:
                get(ruta)
            print('OK: rutas anteriores y formularios accesibles por HTTP.')
        finally:detener(p)
        p = iniciar(db)
        try:
            with build_opener().open(BASE + '/productos') as r:html=r.read().decode()
            assert contar() == 2 and 'SQL-TEST' in html and 'SQL-TEXT' in html
            print('OK: segundo proceso Flask recupera los dos registros del primer proceso.')
            print('OK: reinicializar CREATE TABLE IF NOT EXISTS conserva registros.')
        finally:detener(p)
    print('Pruebas terminadas. La base entregada no fue modificada.')

if __name__=='__main__':ejecutar()
