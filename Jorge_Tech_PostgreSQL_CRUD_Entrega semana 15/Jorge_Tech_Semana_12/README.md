# Jorge Tech — PostgreSQL, CRUD, autenticación y Render (Semana 15)

**Estudiante:** Jorge Manobanda  
**Asignatura:** Desarrollo de Aplicaciones Web

Este proyecto conserva los formularios Flask-WTF, CSRF, plantillas Jinja2,
componentes reutilizables, Bootstrap, CSS, JavaScript y rutas creadas previamente.
El módulo **Productos** se actualizó para trabajar con PostgreSQL y ejecutar las
operaciones SQL `SELECT`, `INSERT`, `UPDATE` y `DELETE` de forma persistente.

## Estructura principal

```text
Jorge_Tech_Semana_12/
├── app.py
├── requirements.txt
├── .env.example
├── conexion/
│   └── conexion.py
├── sql/
│   └── esquema.sql
├── forms/
│   ├── producto_form.py
│   ├── cliente_form.py
│   ├── proveedor_form.py
│   ├── facturacion_form.py
│   └── eliminar_form.py
├── templates/
│   ├── base.html
│   ├── productos.html
│   ├── formulario_producto.html
│   └── components/
└── static/
    ├── css/style.css
    ├── js/script.js
    └── img/
```

## 1. Preparar PostgreSQL

1. Instale PostgreSQL y abra **pgAdmin**.
2. Cree una base de datos llamada `jorge_tech`.
3. Seleccione esa base y abra **Query Tool**.
4. Abra el archivo `sql/esquema.sql`, copie su contenido y ejecútelo.
   El script crea las tablas `proveedores`, `productos`, `clientes` y `facturas`,
   sus claves primarias, dos claves foráneas y datos iniciales.
5. Copie `.env.example` como `.env` y escriba su contraseña real:

```env
DATABASE_URL=postgresql://postgres:TU_CONTRASENA@localhost:5432/jorge_tech
SECRET_KEY=una-clave-larga-y-secreta
```

El archivo `.env` está en `.gitignore`; por eso la contraseña no se sube a GitHub.

## 2. Ejecutar Flask

En la carpeta donde está `app.py`:

```bat
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
python app.py
```

En Linux/macOS, active el entorno con `source .venv/bin/activate`.
Después abra <http://127.0.0.1:5000> y entre a **Productos**.

## 3. Flujo obligatorio para la evidencia

1. Abra `/productos`. El listado usa `SELECT` y `fetchall()`.
2. Pulse **Registrar producto**. Elija un proveedor y guarde un código nuevo,
   por ejemplo `PRUEBA-CRUD`.
3. Confirme en Productos que aparece el registro y, en pgAdmin, ejecute:

```sql
SELECT p.codigo, p.nombre, pr.empresa AS proveedor
FROM productos p
INNER JOIN proveedores pr ON pr.id = p.proveedor_id
WHERE p.codigo = 'PRUEBA-CRUD';
```

4. Pulse **Modificar**, cambie por ejemplo el precio o stock y guarde.
5. Vuelva a ejecutar el `SELECT` para confirmar el cambio en PostgreSQL.
6. Pulse **Eliminar**, acepte la confirmación visual y compruebe que el registro
   desapareció tanto de la página como de la consulta en pgAdmin.
7. Detenga Flask, inícielo de nuevo y confirme que los demás datos siguen allí.

## 4. Evidencia técnica

| Requisito | Ubicación en el proyecto |
| --- | --- |
| Conexión centralizada | `conexion/conexion.py` |
| Variables sin contraseña pública | `.env.example` y `.gitignore` |
| Tablas, PK y FK | `sql/esquema.sql` |
| SELECT y `fetchall()` | `consultar_productos()` en `app.py` |
| Consulta relacionada | `INNER JOIN productos - proveedores` |
| INSERT parametrizado | `insertar_producto()` |
| UPDATE con WHERE | `actualizar_producto()` |
| DELETE con WHERE | `eliminar_producto_db()` |
| Confirmación de cambios | `conexion.commit()` en INSERT, UPDATE y DELETE |
| Cierre de recursos | `finally` con `cursor.close()` y `conexion.close()` |
| Validación y CSRF | `ProductoForm`, `validate_on_submit()` y `hidden_tag()` |
| Confirmación visual antes de borrar | `templates/productos.html` |

Todas las consultas que reciben valores del usuario usan parámetros `%s`; no se
concatenan campos de formularios dentro de SQL.

## 5. Prueba automatizada opcional

Con PostgreSQL configurado y Flask detenido, ejecute:

```bat
python test_persistencia.py
```

La prueba registra, actualiza, consulta y elimina un producto de prueba. Al final
verifica que no queda ese registro en la base de datos.

## 6. Autenticación — Semana 14

El sistema incorpora registro, login, sesión y cierre de sesión mediante
**Flask-Login**. La tabla `usuarios` se crea desde `sql/esquema.sql`; su campo
`usuario` es único y el campo `password` almacena solamente hashes generados con
`generate_password_hash()` de Werkzeug.

### Comprobar el flujo de acceso

1. Ejecute nuevamente `sql/esquema.sql` en la base `jorge_tech` para crear la
   tabla `usuarios`.
2. Abra `http://127.0.0.1:5000/registro`, cree un usuario y contraseña de al
   menos ocho caracteres.
3. En pgAdmin compruebe que el valor de `password` no coincide con la contraseña
   escrita; se mostrará como un hash.
4. Pruebe iniciar sesión con una contraseña incorrecta: el acceso se rechaza.
5. Inicie sesión correctamente. El panel muestra el usuario activo y permite
   acceder a Productos, Clientes, Proveedores y Facturación.
6. Pulse **Cerrar sesión** e intente entrar directamente a `/productos`:
   Flask-Login lo redirige automáticamente hacia `/login`.

Para validar el proceso de forma automatizada:

```bat
python test_autenticacion.py
```

La prueba crea un usuario temporal, confirma el hash, prueba acceso incorrecto,
login correcto, ruta protegida y logout; al final elimina ese usuario de prueba.

## 7. GitHub y GitHub Pages

Suba al mismo repositorio todos los archivos, excepto `.env`, `.venv` y cachés.
GitHub Pages muestra solamente el frontend estático que ya se conserva en
`avance10/`; GitHub Pages no ejecuta Flask ni PostgreSQL. El CRUD se demuestra
localmente con Flask y pgAdmin.

## 8. Semana 15: módulos completos y Render

Clientes, Proveedores, Productos y Facturación ahora trabajan directamente con
PostgreSQL. Cada módulo tiene listado, registro, edición y eliminación; los
módulos Facturación y Productos muestran información relacionada mediante JOIN.
Las rutas administrativas requieren sesión activa.

El archivo `render.yaml` prepara un servicio Flask con Gunicorn y una base de
datos Render PostgreSQL. Consulte [GUIA_RENDER.md](GUIA_RENDER.md) para subir
el repositorio y crear el deploy público.
