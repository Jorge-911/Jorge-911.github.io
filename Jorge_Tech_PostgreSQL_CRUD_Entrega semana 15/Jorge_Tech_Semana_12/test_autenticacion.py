"""Prueba integrada del registro, hash, login, protección y logout.

Ejecutar con DATABASE_URL/.env configurado y con sql/esquema.sql aplicado.
El usuario temporal se elimina al finalizar.
"""
import re
import unittest

from werkzeug.security import check_password_hash

from app import app
from conexion.conexion import obtener_conexion

USUARIO_PRUEBA = "login_prueba_2026"
PASSWORD_PRUEBA = "ClaveSegura2026"


class AutenticacionPostgreSQLTest(unittest.TestCase):
    def setUp(self):
        app.config.update(TESTING=True)
        self.client = app.test_client()
        self.eliminar_usuario_prueba()

    def tearDown(self):
        self.eliminar_usuario_prueba()

    def eliminar_usuario_prueba(self):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        try:
            cursor.execute("DELETE FROM usuarios WHERE usuario = %s", (USUARIO_PRUEBA,))
            conexion.commit()
        finally:
            cursor.close()
            conexion.close()

    def token(self, ruta):
        respuesta = self.client.get(ruta)
        self.assertEqual(respuesta.status_code, 200)
        return re.search(r'name="csrf_token"[^>]*value="([^"]+)"', respuesta.text).group(1)

    def obtener_password_guardado(self):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        try:
            cursor.execute("SELECT password FROM usuarios WHERE usuario = %s", (USUARIO_PRUEBA,))
            fila = cursor.fetchone()
            return None if fila is None else fila["password"]
        finally:
            cursor.close()
            conexion.close()

    def test_registro_login_proteccion_y_logout(self):
        respuesta = self.client.get("/productos")
        self.assertEqual(respuesta.status_code, 302)
        self.assertIn("/login", respuesta.location)

        datos_registro = {
            "csrf_token": self.token("/registro"),
            "usuario": USUARIO_PRUEBA,
            "password": PASSWORD_PRUEBA,
            "confirmar_password": PASSWORD_PRUEBA,
        }
        respuesta = self.client.post("/registro", data=datos_registro, follow_redirects=True)
        self.assertIn("Usuario creado correctamente", respuesta.text)
        password_guardado = self.obtener_password_guardado()
        self.assertIsNotNone(password_guardado)
        self.assertNotEqual(password_guardado, PASSWORD_PRUEBA)
        self.assertTrue(check_password_hash(password_guardado, PASSWORD_PRUEBA))

        respuesta = self.client.post("/login", data={
            "csrf_token": self.token("/login"), "usuario": USUARIO_PRUEBA,
            "password": "ContrasenaIncorrecta",
        }, follow_redirects=True)
        self.assertIn("Usuario o contraseña incorrectos", respuesta.text)

        respuesta = self.client.post("/login", data={
            "csrf_token": self.token("/login"), "usuario": USUARIO_PRUEBA,
            "password": PASSWORD_PRUEBA,
        }, follow_redirects=True)
        self.assertIn(f"Bienvenido/a, {USUARIO_PRUEBA}", respuesta.text)
        self.assertIn(f"Usuario: {USUARIO_PRUEBA}", respuesta.text)
        self.assertEqual(self.client.get("/productos").status_code, 200)

        respuesta = self.client.get("/logout", follow_redirects=True)
        self.assertIn("La sesión se cerró correctamente", respuesta.text)
        respuesta = self.client.get("/productos")
        self.assertEqual(respuesta.status_code, 302)
        self.assertIn("/login", respuesta.location)


if __name__ == "__main__":
    unittest.main(verbosity=2)
