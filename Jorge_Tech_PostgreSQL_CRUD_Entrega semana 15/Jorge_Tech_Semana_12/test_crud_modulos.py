"""Prueba CRUD de Clientes, Proveedores y Facturación con PostgreSQL.

Requiere DATABASE_URL configurado. Todos los registros temporales se eliminan
al finalizar la ejecución.
"""
import re
import unittest

from werkzeug.security import generate_password_hash

from app import app
from conexion.conexion import obtener_conexion

USUARIO, CLAVE = "crud_s15", "ClaveCrudS152026"
EMPRESA, CLIENTE, FACTURA, PRODUCTO = "Proveedor CRUD S15", "Cliente CRUD S15", "S15-900", "S15-PROD"


class CrudModulosPostgreSQLTest(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()
        self.limpiar()
        self.preparar_usuario()

    def tearDown(self):
        self.limpiar()

    def ejecutar(self, consulta, parametros=()):
        conexion = obtener_conexion(); cursor = conexion.cursor()
        try:
            cursor.execute(consulta, parametros); conexion.commit()
            return cursor.rowcount
        finally:
            cursor.close(); conexion.close()

    def uno(self, consulta, parametros=()):
        conexion = obtener_conexion(); cursor = conexion.cursor()
        try:
            cursor.execute(consulta, parametros); return cursor.fetchone()
        finally:
            cursor.close(); conexion.close()

    def limpiar(self):
        for consulta, parametro in [
            ("DELETE FROM facturas WHERE numero = %s", FACTURA),
            ("DELETE FROM productos WHERE codigo = %s", PRODUCTO),
            ("DELETE FROM clientes WHERE nombre = %s", CLIENTE),
            ("DELETE FROM proveedores WHERE empresa = %s", EMPRESA),
            ("DELETE FROM usuarios WHERE usuario = %s", USUARIO),
        ]:
            self.ejecutar(consulta, (parametro,))

    def preparar_usuario(self):
        self.ejecutar("INSERT INTO usuarios (usuario, password) VALUES (%s, %s)", (USUARIO, generate_password_hash(CLAVE)))
        token = self.token("/login")
        respuesta = self.client.post("/login", data={"csrf_token": token, "usuario": USUARIO, "password": CLAVE})
        self.assertEqual(respuesta.status_code, 302)

    def token(self, ruta):
        respuesta = self.client.get(ruta)
        self.assertEqual(respuesta.status_code, 200, ruta)
        return re.search(r'name="csrf_token"[^>]*value="([^"]+)"', respuesta.text).group(1)

    def post(self, ruta, datos):
        respuesta = self.client.post(ruta, data=datos, follow_redirects=True)
        self.assertEqual(respuesta.status_code, 200, ruta)
        return respuesta.text

    def test_crud_modulos_y_join(self):
        html = self.post("/proveedores/nuevo", {"csrf_token": self.token("/proveedores/nuevo"), "empresa": EMPRESA, "producto": "Accesorios", "contacto": "s15@example.com", "ciudad": "Puyo"})
        self.assertIn("Proveedor registrado correctamente", html)
        proveedor = self.uno("SELECT id FROM proveedores WHERE empresa = %s", (EMPRESA,))
        self.assertIsNotNone(proveedor)
        html = self.post(f"/proveedores/{proveedor['id']}/editar", {"csrf_token": self.token(f"/proveedores/{proveedor['id']}/editar"), "empresa": EMPRESA, "producto": "Periféricos", "contacto": "actualizado@example.com", "ciudad": "Quito"})
        self.assertIn("Proveedor modificado correctamente", html)

        html = self.post("/clientes/nuevo", {"csrf_token": self.token("/clientes/nuevo"), "nombre": CLIENTE, "servicio": "Soporte técnico", "telefono": "0991234567", "estado": "Pendiente"})
        self.assertIn("Cliente registrado correctamente", html)
        cliente = self.uno("SELECT id FROM clientes WHERE nombre = %s", (CLIENTE,))
        html = self.post(f"/clientes/{cliente['id']}/editar", {"csrf_token": self.token(f"/clientes/{cliente['id']}/editar"), "nombre": CLIENTE, "servicio": "Redes y conectividad", "telefono": "0991234567", "estado": "En proceso"})
        self.assertIn("Cliente modificado correctamente", html)

        html = self.post("/facturacion/nuevo", {"csrf_token": self.token("/facturacion/nuevo"), "cliente_id": cliente["id"], "numero": FACTURA, "detalle": "Servicio CRUD", "total": "30.00", "estado": "Pendiente"})
        self.assertIn("Factura registrada correctamente", html)
        self.assertIn(CLIENTE, self.client.get("/facturacion").text)
        factura = self.uno("SELECT id FROM facturas WHERE numero = %s", (FACTURA,))
        html = self.post(f"/facturacion/{factura['id']}/editar", {"csrf_token": self.token(f"/facturacion/{factura['id']}/editar"), "cliente_id": cliente["id"], "numero": FACTURA, "detalle": "Servicio CRUD actualizado", "total": "35.00", "estado": "Pagada"})
        self.assertIn("Factura modificada correctamente", html)

        html = self.post("/productos/nuevo", {"csrf_token": self.token("/productos/nuevo"), "proveedor_id": proveedor["id"], "codigo": PRODUCTO, "nombre": "Producto S15", "categoria": "Pruebas", "precio": "12.50", "stock": "3"})
        self.assertIn("Producto registrado correctamente", html)
        producto = self.uno("SELECT id FROM productos WHERE codigo = %s", (PRODUCTO,))
        html = self.post(f"/productos/{producto['id']}/editar", {"csrf_token": self.token(f"/productos/{producto['id']}/editar"), "proveedor_id": proveedor["id"], "codigo": PRODUCTO, "nombre": "Producto S15 actualizado", "categoria": "Pruebas", "precio": "14.00", "stock": "7"})
        self.assertIn("Producto modificado correctamente", html)
        self.assertIn(EMPRESA, self.client.get("/productos").text)

        self.assertIn("Factura eliminada correctamente", self.post(f"/facturacion/{factura['id']}/eliminar", {"csrf_token": self.token("/facturacion")}))
        self.assertIn("Producto eliminado correctamente", self.post(f"/productos/{producto['id']}/eliminar", {"csrf_token": self.token("/productos")}))
        self.assertIn("Cliente eliminado correctamente", self.post(f"/clientes/{cliente['id']}/eliminar", {"csrf_token": self.token("/clientes")}))
        self.assertIn("Proveedor eliminado correctamente", self.post(f"/proveedores/{proveedor['id']}/eliminar", {"csrf_token": self.token("/proveedores")}))


if __name__ == "__main__":
    unittest.main(verbosity=2)
