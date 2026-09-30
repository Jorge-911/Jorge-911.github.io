"""Prueba integrada del CRUD de Productos contra PostgreSQL configurado.

Ejecutar con DATABASE_URL/.env configurado. El registro temporal se elimina al
terminar, incluso si una aserción falla.
"""
import re
import unittest

from werkzeug.security import generate_password_hash

from app import app
from conexion.conexion import obtener_conexion

CODIGO = "CRUD-TEST-01"
USUARIO_PRUEBA = "crud_prueba"
PASSWORD_PRUEBA = "ClaveCrud2026"


class CrudProductosPostgreSQLTest(unittest.TestCase):
    def setUp(self):
        app.config.update(TESTING=True)
        self.client = app.test_client()
        self.limpiar_producto()
        self.preparar_sesion()
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        try:
            cursor.execute("SELECT id FROM proveedores ORDER BY id LIMIT 1")
            fila = cursor.fetchone()
            if fila is None:
                self.fail("No hay proveedores. Ejecute sql/esquema.sql.")
            self.proveedor_id = fila["id"]
        finally:
            cursor.close()
            conexion.close()

    def tearDown(self):
        self.limpiar_producto()
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        try:
            cursor.execute("DELETE FROM usuarios WHERE usuario = %s", (USUARIO_PRUEBA,))
            conexion.commit()
        finally:
            cursor.close()
            conexion.close()

    def preparar_sesion(self):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        try:
            cursor.execute("DELETE FROM usuarios WHERE usuario = %s", (USUARIO_PRUEBA,))
            cursor.execute(
                "INSERT INTO usuarios (usuario, password) VALUES (%s, %s)",
                (USUARIO_PRUEBA, generate_password_hash(PASSWORD_PRUEBA)),
            )
            conexion.commit()
        finally:
            cursor.close()
            conexion.close()
        respuesta = self.client.get("/login")
        token = re.search(r'name="csrf_token"[^>]*value="([^"]+)"', respuesta.text).group(1)
        respuesta = self.client.post("/login", data={
            "csrf_token": token, "usuario": USUARIO_PRUEBA, "password": PASSWORD_PRUEBA,
        })
        self.assertEqual(respuesta.status_code, 302)

    def limpiar_producto(self):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        try:
            cursor.execute("DELETE FROM productos WHERE codigo = %s", (CODIGO,))
            conexion.commit()
        finally:
            cursor.close()
            conexion.close()

    def token(self, ruta):
        respuesta = self.client.get(ruta)
        self.assertEqual(respuesta.status_code, 200)
        return re.search(r'name="csrf_token"[^>]*value="([^"]+)"', respuesta.text).group(1)

    def consultar(self):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        try:
            cursor.execute("SELECT id, nombre, precio, stock FROM productos WHERE codigo = %s", (CODIGO,))
            return cursor.fetchone()
        finally:
            cursor.close()
            conexion.close()

    def test_flujo_crud_completo(self):
        datos = {
            "csrf_token": self.token("/productos/nuevo"),
            "proveedor_id": self.proveedor_id,
            "codigo": CODIGO,
            "nombre": "Producto de prueba PostgreSQL",
            "categoria": "Pruebas",
            "precio": "15.50",
            "stock": "4",
        }
        respuesta = self.client.post("/productos/nuevo", data=datos, follow_redirects=True)
        self.assertEqual(respuesta.status_code, 200)
        self.assertIn("Producto registrado correctamente", respuesta.text)
        creado = self.consultar()
        self.assertIsNotNone(creado)
        self.assertEqual(creado["stock"], 4)

        datos.update({
            "csrf_token": self.token(f"/productos/{creado['id']}/editar"),
            "nombre": "Producto actualizado PostgreSQL",
            "precio": "21.75",
            "stock": "9",
        })
        respuesta = self.client.post(f"/productos/{creado['id']}/editar", data=datos, follow_redirects=True)
        self.assertIn("Producto modificado correctamente", respuesta.text)
        actualizado = self.consultar()
        self.assertEqual(actualizado["nombre"], "Producto actualizado PostgreSQL")
        self.assertEqual(str(actualizado["precio"]), "21.75")
        self.assertEqual(actualizado["stock"], 9)

        respuesta = self.client.post(
            f"/productos/{creado['id']}/eliminar",
            data={"csrf_token": self.token("/productos")},
            follow_redirects=True,
        )
        self.assertIn("Producto eliminado correctamente", respuesta.text)
        self.assertIsNone(self.consultar())


if __name__ == "__main__":
    unittest.main(verbosity=2)
