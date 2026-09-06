# Jorge Tech — Semana 12 / Avance 12 de 16

Estudiante: Jorge Manobanda. Desarrollo de Aplicaciones Web.
Este proyecto continúa directamente la Semana 11: conserva formularios Flask-WTF,
CSRF, las cinco rutas de listado, componentes, estilos y frontend anterior.
Productos incorpora persistencia SQLite. Los otros tres módulos siguen temporales.

## 1. Preparar el proyecto

Descomprimir este ZIP. Abrir la terminal dentro de la carpeta que contiene app.py.
No sustituir una base propia con registros por la base de ejemplo de este ZIP.

```bat
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
python app.py
```

En Linux/macOS activar con `source .venv/bin/activate`.
Se requiere Python 3.9 o superior con sqlite3. SQLite forma parte de la distribución
habitual de Python: no instalar un paquete sqlite3 con pip. Se conservan las
versiones de requirements.txt de Semana 11 porque no se agrega dependencia externa.
El archivo venv.rar heredado no hace falta para ejecutar el proyecto.

## 2. Usar el módulo persistente

1. Abrir http://127.0.0.1:5000.
2. Entrar en Productos y pulsar Registrar producto.
3. Completar un código nuevo, nombre, categoría, precio positivo con hasta dos
   decimales y stock entero mayor o igual a cero.
4. Guardar. Si hay errores, se muestran debajo del campo y no se realiza INSERT.
5. Un registro válido se guarda y redirige a /productos.
6. La tabla Bootstrap muestra los resultados de SELECT con un for de Jinja2.
7. Un stock cero muestra Agotado; stock positivo muestra Disponible; hasta dos
   unidades también muestra Bajo stock.

## 3. Comprobar que los datos permanecen

1. Registrar código PRUEBA12, nombre Monitor de prueba, categoría Pantallas,
   precio 25.50 y stock 0.
2. Confirmar que aparece en la tabla.
3. Detener Flask con Ctrl+C.
4. Ejecutar nuevamente `python app.py`.
5. Abrir /productos: PRUEBA12 permanece disponible.

No borrar data/ferreteria.db: es el archivo que conserva los registros.
La base incluida contiene los cuatro productos de ejemplo de semanas anteriores,
insertados a través del formulario validado durante la preparación de la entrega.
Al iniciar no se reemplazan registros ni se repiten datos iniciales. Si no existe
la base, la aplicación crea una base vacía y su tabla automáticamente.

## 4. Implementación en app.py

| Requisito | Evidencia |
| --- | --- |
| Carpeta data y ferreteria.db | data/ferreteria.db, incluida en el ZIP |
| sqlite3 y connect | conectar_db() utiliza sqlite3.connect() |
| Creación idempotente | inicializar_db(): CREATE TABLE IF NOT EXISTS productos |
| Clave primaria | id INTEGER PRIMARY KEY AUTOINCREMENT |
| Campos del formulario | codigo, nombre, categoria, precio_centavos, stock |
| Validación previa | nuevo_producto(): form.validate_on_submit() |
| INSERT parametrizado | VALUES (?, ?, ?, ?, ?) y tupla de valores |
| Confirmación | conn.commit() tras CREATE/INSERT |
| Cierre correcto | conn.close() en finally |
| Manejo de fallos | rollback; aviso de duplicado o error de guardado |
| Recuperación | consultar_productos(): SELECT y fetchall() |
| Flask a Jinja2 | productos(): render_template con registros recuperados |
| Tabla HTML | templates/productos.html, table y for |
| Persistencia real | test_persistencia.py detiene y reinicia dos procesos |
| Sin lista como almacenamiento | Productos se lee y escribe únicamente en SQLite |
| Formularios y CSRF | forms/, SECRET_KEY, hidden_tag y validaciones conservadas |
| Reutilización | base.html y components; formulario común |
| Navegación/recursos | url_for y static conservados |
| Continuidad de módulos | Clientes, proveedores y facturación siguen operativos |
| Subida a GitHub | Pendiente acceso a la cuenta y publicación |

El precio se almacena en centavos enteros (25.50 → 2550) para evitar errores de
representación monetaria; SELECT lo convierte a precio para mostrarlo. Se rechazan
precios con más de dos decimales. El código es UNIQUE sin distinguir mayúsculas ASCII.
El estado se calcula desde stock y no se almacena duplicado.

La base usa una ruta absoluta relativa al directorio de app.py. La variable de
entorno JORGE_TECH_DB permite aislar pruebas sin tocar la base entregada.
SECRET_KEY se conserva configurable por entorno, con clave aleatoria por proceso
para ejecución local. Después de reiniciar, recargar un formulario abierto para
obtener un token nuevo; esto no elimina los productos guardados en SQLite.

## 5. Pruebas automatizadas

Con Flask detenido y el puerto 5000 libre:

```bat
python test_persistencia.py
python test_formularios.py
```

La primera prueba utiliza una base temporal y dos procesos reales de `python app.py`.
Comprueba campos inválidos, CSRF, INSERT, SELECT, duplicados, stock cero, comillas,
valores SQL como texto, rutas y persistencia después de reiniciar.
La segunda conserva las pruebas de formularios de clientes, proveedores y facturas.
No se modifica la base entregada con los casos de prueba.

Con Flask activo, abrir otra terminal y ejecutar `python verificar.py` para verificar
rutas HTTP, recursos estáticos y evidencia Pages. El informe de las pruebas está en
RESULTADO_PRUEBAS_SEMANA_12.txt. Bootstrap y YouTube requieren conexión a Internet.

## 6. Publicar y entregar

Actualizar el mismo repositorio de GitHub con el contenido de esta carpeta:
app.py, requirements.txt, data/ferreteria.db, forms/, templates/, static/ y scripts.
No subir el entorno virtual, cachés ni secretos. .gitignore excluye los temporales.
En GitHub: Add file > Upload files, arrastrar el contenido y confirmar los cambios.
No crear una carpeta adicional que deje app.py fuera de la raíz esperada.
Mensaje sugerido: Semana 12: persistencia SQLite en productos.
Abrir el repositorio publicado y comprobar que data/ferreteria.db esté disponible.
Entregar en Moodle el enlace real del repositorio actualizado.

La publicación no se ha realizado desde esta entrega: falta acceso a GitHub.
GitHub Pages conserva la evidencia frontend; no ejecuta SQLite, Flask ni los POST.
Las funciones de esta semana se revisan ejecutando Flask localmente.

## Alcance y continuidad

Productos permanece guardado al reiniciar. Clientes, proveedores y facturas siguen
usando datos temporales como en Semana 11; su persistencia se añadirá progresivamente.
Las clases de formulario siguen separadas para facilitar esa integración.
No se incorporan edición ni eliminación, porque no se piden en este avance.
Las guías de semanas 10 y 11 se conservan como referencia histórica; esta guía
reemplaza sus indicaciones sobre el almacenamiento de productos.

## Referencia técnica

https://docs.python.org/3/library/sqlite3.html
