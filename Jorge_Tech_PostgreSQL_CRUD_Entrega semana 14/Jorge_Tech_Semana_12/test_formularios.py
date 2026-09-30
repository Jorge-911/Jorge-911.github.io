"""Pruebas con CSRF real habilitado y almacenamiento temporal aislado."""
import re
import unittest
from copy import deepcopy
from app import app, clientes_lista, proveedores_lista, facturas

CASOS = [
 ('/clientes/nuevo', '/clientes', clientes_lista, dict(nombre='Cliente de prueba', servicio='Soporte técnico', telefono='0991234567', estado='Pendiente'), [('nombre',' '),('telefono','abc'),('estado','Inventado')]),
 ('/proveedores/nuevo', '/proveedores', proveedores_lista, dict(empresa='Proveedor de prueba', producto='Accesorios', contacto='ventas@example.com', ciudad='Quito'), [('empresa',''),('contacto','correo-invalido'),('ciudad','A')]),
 ('/facturacion/nuevo', '/facturacion', facturas, dict(numero='TEST-F01', cliente='Cliente de prueba', detalle='Servicio de prueba', total='15.25', estado='Pagada'), [('numero',''),('total','-3'),('total','abc'),('total','NaN'),('estado','Inventado'),('numero','F-001')]),
]

class FormulariosTest(unittest.TestCase):
 def setUp(self):
  app.config['TESTING']=True
  self.client=app.test_client()
  self.originales=[deepcopy(c[2]) for c in CASOS]
 def tearDown(self):
  for caso,original in zip(CASOS,self.originales):caso[2][:]=original
 def token(self,ruta,client=None):
  response=(client or self.client).get(ruta)
  self.assertEqual(response.status_code,200)
  return re.search(r'name="csrf_token"[^>]*value="([^"]+)"',response.text).group(1)
 def test_rutas_y_recursos(self):
  for ruta in ['/','/productos','/clientes','/proveedores','/facturacion','/static/css/style.css','/static/js/script.js','/static/img/tecnologia.svg']:
   with self.client.get(ruta) as response:
    self.assertEqual(response.status_code,200,ruta)
 def test_validaciones_y_csrf(self):
  for ruta,listado,registros,validos,invalidos in CASOS:
   with self.subTest(ruta=ruta):
    token=self.token(ruta); cantidad=len(registros)
    for datos in [{},dict(validos,csrf_token='alterado'),dict(validos)]:
     response=self.client.post(ruta,data=datos)
     self.assertEqual(response.status_code,200)
     self.assertIn('token no es válido',response.text)
     self.assertEqual(len(registros),cantidad)
    response=self.client.post(ruta,data={'csrf_token':token})
    self.assertIn('invalid-feedback',response.text)
    self.assertEqual(len(registros),cantidad)
    for campo,valor in invalidos:
     with self.subTest(campo=campo,valor=valor):
      response=self.client.post(ruta,data=dict(validos,**{campo:valor,'csrf_token':token}))
      self.assertEqual(response.status_code,200)
      self.assertIn('invalid-feedback',response.text)
      self.assertEqual(len(registros),cantidad)
    otro=app.test_client();token_otro=self.token(ruta,otro)
    self.client.post(ruta,data=dict(validos,csrf_token=token_otro))
    self.assertEqual(len(registros),cantidad)
    response=self.client.post(ruta,data=dict(validos,csrf_token=token))
    self.assertEqual(response.status_code,302)
    self.assertTrue(response.location.endswith(listado))
    self.assertEqual(len(registros),cantidad+1)
    response=self.client.get(listado)
    self.assertIn('Registro guardado correctamente',response.text)
    self.assertIn(next(iter(validos.values())),response.text)
    self.client.get(listado)
    self.assertEqual(len(registros),cantidad+1)

if __name__=='__main__':unittest.main(verbosity=2)
