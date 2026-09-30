# Publicación de Jorge Tech en Render

El archivo `render.yaml` ya configura estos dos recursos:

- Servicio web Flask: `jorge-tech-flask`.
- Base de datos PostgreSQL: `jorge-tech-postgres`.

Render asigna `DATABASE_URL` desde la base de datos y genera una `SECRET_KEY`.
No se debe copiar ninguna contraseña al repositorio.

## 1. Subir el proyecto a GitHub

1. Cree un repositorio nuevo en GitHub, por ejemplo `jorge-tech-flask`.
2. Suba todo el contenido de esta carpeta, incluidos `render.yaml`, `app.py`,
   `models.py`, `conexion/`, `forms/`, `templates/`, `static/`, `sql/` y
   `requirements.txt`.
3. No suba `.env`, `.venv`, archivos `__pycache__` ni contraseñas.

## 2. Crear el deploy

1. Ingrese a Render y abra **New > Blueprint**.
2. Conecte el repositorio de GitHub que contiene `render.yaml`.
3. Revise que aparezcan el servicio web y PostgreSQL.
4. Pulse **Apply**. Render instalará las dependencias con
   `pip install -r requirements.txt` y arrancará la aplicación con
   `gunicorn app:app`.
5. Espere a que el estado sea **Live** y copie el enlace `onrender.com` del
   servicio web.

La aplicación ejecuta `sql/esquema.sql` al iniciar cuando `AUTO_INIT_DB=true`.
Por ello una base Render nueva crea automáticamente usuarios, proveedores,
clientes, productos y facturas de ejemplo.

## 3. Prueba para la entrega

En la URL pública de Render ejecute este orden:

1. Abra **Crear usuario** y registre una cuenta.
2. Inicie sesión.
3. Entre a Productos, Clientes, Proveedores y Facturación.
4. Registre, modifique y elimine un dato de prueba en cada módulo.
5. En Facturación confirme que aparece el nombre del cliente relacionado.
6. Cierre sesión e intente abrir `/productos`; debe regresar a `/login`.

Entregue en Moodle el enlace del repositorio GitHub y la URL pública generada
por Render.
