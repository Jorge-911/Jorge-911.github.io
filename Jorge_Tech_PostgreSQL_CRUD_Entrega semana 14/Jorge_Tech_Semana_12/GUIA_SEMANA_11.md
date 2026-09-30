# Jorge Tech — Semana 11 / Avance 11 de 16

Continuación del avance 10 de Jorge Manobanda. Se conservan las cinco rutas,
las plantillas, los componentes, los estilos, la página original y la evidencia
estática de GitHub Pages. Se añaden formularios Flask-WTF para los cuatro módulos.

## Ejecutar en Windows

Descomprimir y abrir una terminal dentro de la carpeta que contiene app.py.
Requiere Python 3.9 o superior. Crear y activar un entorno nuevo:

```bat
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
python app.py
```

En Linux/macOS, activar con `source .venv/bin/activate`.
Abrir http://127.0.0.1:5000. Entrar en un módulo y pulsar Registrar.
No abrir los HTML de templates directamente ni ejecutar el proyecto dentro del ZIP.
El venv.rar heredado no es necesario para ejecutar este avance.

Las dependencias se instalaron en un entorno virtual aislado con Flask-WTF y
email-validator, y requirements.txt se obtuvo mediante pip freeze.

## Formularios y rutas

| Módulo | Clase / archivo | Ruta GET y POST | Datos |
| --- | --- | --- | --- |
| Productos | ProductoForm / forms/producto_form.py | /productos/nuevo | Código, nombre, categoría, precio y stock |
| Clientes | ClienteForm / forms/cliente_form.py | /clientes/nuevo | Nombre, servicio, teléfono y estado |
| Proveedores | ProveedorForm / forms/proveedor_form.py | /proveedores/nuevo | Empresa, productos, correo y ciudad |
| Facturación | FacturacionForm / forms/facturacion_form.py | /facturacion/nuevo | Número, cliente, detalle, total y estado |

Cada clase hereda de FlaskForm. Cada módulo tiene su plantilla formulario_*.html
que hereda de base.html. components/formulario.html comparte el marcado y evita
repeticiones. Las clases admiten datos iniciales para una futura edición; las rutas
de edición no forman parte del alcance de esta semana.

## Validación y procesamiento

- DataRequired y Length para textos obligatorios; se eliminan espacios exteriores.
- Email para correo y Regexp para teléfonos nacionales de 9 o 10 dígitos.
- NumberRange para precio/total positivos y stock entero desde cero.
- InputRequired se usa en números para aceptar stock 0, que DataRequired rechazaría.
- SelectField limita los estados y servicios a las opciones admitidas.
- Se rechazan códigos de producto y números de factura duplicados.
- form.validate_on_submit() debe aprobar antes de agregar datos a las listas.
- Tras guardar, se redirige al listado y se muestra un mensaje. Actualizar ese
  listado no vuelve a enviar el POST.
- Los errores aparecen debajo de cada campo; novalidate permite observar la
  validación del servidor incluso cuando el navegador podría bloquear el envío.

## CSRF y SECRET_KEY

app.py utiliza SECRET_KEY del entorno, o genera una clave aleatoria al iniciar
para facilitar la ejecución local. No hay una clave privada fija en el repositorio.
Cada formulario incluye form.hidden_tag(). FlaskForm valida el token en el POST
con la protección CSRF habilitada. Un token ausente, alterado o de otra sesión
impide registrar los datos y produce un aviso en el formulario.
Al reiniciar, recargar los formularios para obtener una nueva sesión/token.
Para una clave estable, definir SECRET_KEY en el entorno antes de iniciar Flask.
Esta aplicación está preparada para la ejecución local de la actividad.

## Datos temporales

Las listas de ejemplo se definen en app.py fuera de las funciones de ruta, de modo
que los registros nuevos permanezcan entre peticiones del mismo proceso.
Se pierden al reiniciar. No hay conexión a una base de datos ni archivos de persistencia.
Los datos son de demostración; el módulo de facturación no emite documentos fiscales.
La carpeta forms separa la validación de la futura capa de persistencia.

## Comprobar antes de entregar

```bat
python test_formularios.py
```

Incluye pruebas de los cuatro módulos: GET, campos vacíos, formatos/rangos
incorrectos, opciones manipuladas, duplicados, CSRF ausente/alterado/de otra sesión,
registros válidos, redirección y ausencia de registros al fallar la validación.
Las pruebas mantienen CSRF activo y restauran los registros originales al terminar.

Con python app.py activo, desde otra terminal:

```bat
python verificar.py
```

Comprueba rutas por HTTP y recursos locales, las condiciones Jinja2 de stock y los
enlaces de la evidencia estática. RESULTADO_PRUEBAS_SEMANA_11.txt contiene el
resultado obtenido durante la preparación de esta entrega.

Prueba manual para la revisión:
1. Entrar en Productos > Registrar producto y enviar vacío: aparecen errores.
2. Ingresar precio negativo o stock decimal: no se registra.
3. Completar con código nuevo, nombre Monitor, categoría Pantallas, precio 25.50
   y stock 0: se guarda y aparece Agotado en el listado.
4. Repetir el código: aparece el error de duplicado.
5. En Proveedores ingresar un correo sin @: aparece error; corregirlo y guardar.
6. Registrar un cliente y una factura con valores válidos y comprobar sus listados.
7. Reiniciar Flask: regresan los datos iniciales, según el alcance sin base de datos.

## GitHub y Pages

Subir el contenido de esta carpeta al mismo repositorio, conservando la raíz:
app.py, requirements.txt, forms/, templates/, static/, los scripts y la documentación.
No subir .venv, __pycache__ ni secretos del entorno; .gitignore ya los excluye.
En GitHub se puede usar Add file > Upload files y confirmar los cambios.
El mensaje sugerido es: Semana 11: formularios Flask-WTF, validación y CSRF.
Entregar en Moodle el enlace real del repositorio actualizado.

La publicación remota queda pendiente de acceso a la cuenta de GitHub.
El index.html raíz y avance10/ conservan la evidencia visual anterior.
GitHub Pages no ejecuta estos formularios: se revisan con Flask local.
exportar_pages.py puede regenerar los listados estáticos ocultando los botones de
registro, para evitar enlaces a funciones de backend en Pages.

## Relación con las indicaciones

| Grupo de requisitos | Evidencia |
| --- | --- |
| Continuar Semana 10 sin eliminar avances | Cinco rutas originales, templates, static, components, frontend original y avance10 |
| Carpeta forms e __init__.py | Cuatro clases separadas por módulo |
| Flask-WTF, WTForms y validadores | forms/*_form.py y requirements.txt |
| GET/POST y validate_on_submit | Cuatro rutas /nuevo en app.py |
| SECRET_KEY y CSRF | Configuración app.py, hidden_tag en components/formulario.html |
| Campos/etiquetas de WTForms | Bucle de campos en components/formulario.html |
| Errores debajo de campos y Bootstrap | formulario.html, clases is-invalid e invalid-feedback |
| Herencia y reutilización | Cuatro plantillas de formulario extienden base.html e incluyen el formulario común |
| Navegación y recursos | url_for en enlaces; CSS, JavaScript e imagen en static |
| Procesamiento solo válido | Append después de validate_on_submit y comprobación de duplicados |
| Sin base de datos | Listas de Python en app.py |
| Pruebas válidas, inválidas y CSRF | test_formularios.py y resultado de pruebas |
| Ejecución local y rutas | python app.py y verificar.py |
| Subida al repositorio | Pendiente publicar en la cuenta y comprobar el enlace |

## Documentación consultada

- https://flask-wtf.readthedocs.io/en/1.2.x/quickstart/
- https://wtforms.readthedocs.io/en/3.2.x/validators/
