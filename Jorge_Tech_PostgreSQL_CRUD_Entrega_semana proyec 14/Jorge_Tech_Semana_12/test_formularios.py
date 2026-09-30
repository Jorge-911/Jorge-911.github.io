"""Pruebas de rutas públicas/protegidas y validaciones Flask-WTF."""
import unittest

from werkzeug.datastructures import MultiDict

from app import app
from forms.cliente_form import ClienteForm
from forms.facturacion_form import FacturacionForm
from forms.login_form import LoginForm
from forms.producto_form import ProductoForm
from forms.proveedor_form import ProveedorForm
from forms.usuario_form import UsuarioForm


class FormulariosTest(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def crear_formulario(self, clase, datos):
        with app.test_request_context("/"):
            return clase(formdata=MultiDict(datos), meta={"csrf": False})

    def test_rutas_publicas_y_proteccion(self):
        for ruta in ["/", "/login", "/registro", "/static/css/style.css", "/static/js/script.js", "/static/img/tecnologia.svg"]:
            with self.client.get(ruta) as respuesta:
                self.assertEqual(respuesta.status_code, 200, ruta)
        for ruta in ["/dashboard", "/productos", "/clientes", "/proveedores", "/facturacion"]:
            respuesta = self.client.get(ruta)
            self.assertEqual(respuesta.status_code, 302, ruta)
            self.assertIn("/login", respuesta.location)

    def test_validaciones_de_formularios(self):
        producto = self.crear_formulario(ProductoForm, {
            "proveedor_id": "1", "codigo": "JT-100", "nombre": "Teclado", "categoria": "Accesorios", "precio": "20.50", "stock": "2",
        })
        producto.proveedor_id.choices = [(1, "Proveedor de prueba")]
        self.assertTrue(producto.validate())
        self.assertFalse(self.crear_formulario(ProductoForm, {"codigo": "", "precio": "-1", "stock": "-2"}).validate())

        self.assertTrue(self.crear_formulario(ClienteForm, {
            "nombre": "Cliente de prueba", "servicio": "Soporte técnico", "telefono": "0991234567", "estado": "Pendiente",
        }).validate())
        self.assertTrue(self.crear_formulario(ProveedorForm, {
            "empresa": "Proveedor de prueba", "producto": "Accesorios", "contacto": "ventas@example.com", "ciudad": "Quito",
        }).validate())
        self.assertTrue(self.crear_formulario(FacturacionForm, {
            "numero": "F-100", "cliente": "Cliente de prueba", "detalle": "Servicio de prueba", "total": "15.25", "estado": "Pagada",
        }).validate())
        self.assertTrue(self.crear_formulario(LoginForm, {"usuario": "usuario1", "password": "ClaveSegura"}).validate())
        self.assertTrue(self.crear_formulario(UsuarioForm, {
            "usuario": "usuario1", "password": "ClaveSegura", "confirmar_password": "ClaveSegura",
        }).validate())
        self.assertFalse(self.crear_formulario(UsuarioForm, {
            "usuario": "a", "password": "corta", "confirmar_password": "distinta",
        }).validate())


if __name__ == "__main__":
    unittest.main(verbosity=2)
