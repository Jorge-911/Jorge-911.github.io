# Jorge Tech — Proyecto Integrador U3, avance 10/16

Estudiante: Jorge Manobanda. Asignatura: Desarrollo Web.
Continuación del proyecto adjunto de la Semana 9. Se mantienen las cinco rutas,
las páginas anteriores, los estilos, scripts, imagen, video y el frontend original.
Los datos de clientes, proveedores y facturas son ejemplos académicos.

## 1. Ejecutar Flask en Windows

Descomprimir el ZIP. Abrir una terminal dentro de la carpeta que contiene app.py.
Usar Python 3.9 o superior:

```bat
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
python app.py
```

Abrir http://127.0.0.1:5000 y navegar por Inicio, Productos, Clientes,
Proveedores y Facturación. Mantener la terminal abierta. Detener con Ctrl+C.
En macOS/Linux, la activación es `source .venv/bin/activate`.
El archivo venv.rar se conserva del original, pero no se necesita: crear un entorno nuevo.
Bootstrap y el video de YouTube requieren conexión a Internet.

## 2. Evidencias de cada requisito

| Requisito | Implementación / ubicación |
| --- | --- |
| Continuidad de Semana 9 | Se conservan las rutas y archivos previos; index.html raíz mantiene el frontend anterior con un enlace adicional al avance |
| app.py, templates y static | Permanecen en su estructura original |
| Plantilla principal | templates/base.html |
| Herencia en las cinco páginas | Todas declaran extends "base.html" |
| Bloques title y content | base.html y las cinco plantillas internas |
| Variable simple | mensaje_bienvenida en inicio(), enviada con render_template y mostrada en templates/index.html |
| Diccionario del sistema | sistema en app.py; enviado a index.html y compartido con context_processor para las otras rutas |
| Listas y diccionarios | servicios, productos_lista, clientes_lista, proveedores_lista y facturas en app.py |
| Envío de datos | render_template en cada función de ruta |
| Variables {{ ... }} | Nombres, precios, stock, clientes, servicios, información del pie y cabecera |
| Bucle for | Genera tarjetas/filas en los cinco módulos |
| if / else / endif | Stock positivo: Disponible; stock cero: Agotado en productos.html |
| Ambas condiciones con ejemplos | Cable UTP: 12, mouse: 8, teclado: 2, adaptador HDMI: 0 |
| Condición adicional | Stock hasta 2: Bajo stock; estados de clientes y de facturas |
| Filtros | upper en código de producto, length en total de productos, format para precios con dos decimales |
| Componentes independientes | components/navbar.html, footer.html y mensaje.html |
| Reutilización include | Los tres componentes se incluyen en base.html |
| Navegación url_for | components/navbar.html y botones de inicio |
| Recursos static con url_for | CSS y JavaScript en base.html; imagen en index.html |
| Presentación | Bootstrap y estilos originales; tarjetas y tabla adaptable |
| Sin base de datos | Datos temporales en Python; no se requiere persistencia en esta entrega |
| Ejecución python app.py | Verificada con servidor local y peticiones HTTP |
| Rutas y recursos sin 404 | Cinco rutas y recursos locales comprobados por verificar.py |
| requirements.txt | Flask==3.1.2 |
| Frontend para Pages | avance10/ contiene las cinco páginas HTML renderizadas y enlaces relativos |
| Publicación remota | Pendiente subir cambios a la cuenta y comprobar las URL públicas |

## 3. Repetir las pruebas

Con `python app.py` activo, abrir otra terminal en esta carpeta y ejecutar:

```bat
python verificar.py
```

Comprueba las cinco rutas por HTTP, sus enlaces y recursos locales, las condiciones
con stock positivo/cero, la lista vacía y los enlaces de las cinco páginas exportadas.
El resultado de la ejecución realizada se incluye en RESULTADO_PRUEBAS.txt.
No se certifica la disponibilidad de recursos externos ni de una publicación remota.

## 4. Actualizar GitHub Pages sin ejecutar Python en Pages

```bat
python exportar_pages.py
```

El script renderiza las mismas plantillas Flask y escribe HTML final en avance10/.
Volver a ejecutarlo cuando cambien los datos, componentes o plantillas.
El index.html de la raíz conserva la web anterior y ofrece un enlace al avance.
También se puede abrir avance10/index.html directamente en el navegador.
Las plantillas de templates/ se ejecutan mediante Flask; no abrirlas directamente.
No copiar Jinja2 sin renderizar en GitHub Pages.

## 5. Subir al mismo repositorio de GitHub

1. Entrar en el repositorio utilizado en la Semana 9.
2. Usar Add file > Upload files. Arrastrar el contenido de esta carpeta, incluyendo
   app.py, requirements.txt, templates, static, avance10, scripts y documentación.
   Los archivos deben quedar en la raíz del repositorio, sin otra carpeta contenedora.
3. Mantener los archivos del proyecto anterior. Confirmar los cambios con el mensaje
   `Avance 10: contenido dinámico Jinja2 y componentes reutilizables`.
4. En Settings > Pages, comprobar la publicación desde la rama correspondiente
   (normalmente main), carpeta /(root). Conservar la configuración existente si ya
   publica correctamente desde esa raíz.
5. Esperar a que termine la publicación y abrir la dirección que indique GitHub Pages.
6. Abrir el enlace «Ver avance 10» y comprobar sus cinco páginas desde otra ventana.
7. Entregar en Moodle el enlace real del repositorio y el enlace real de Pages.

Alternativa con un clon Git existente: copiar encima los archivos actualizados,
revisar `git diff`, ejecutar `git add .`, `git commit -m "Avance 10: Jinja2"` y
`git push`. No se incluye un repositorio .git en este ZIP.

La publicación no se ha efectuado desde esta entrega: hace falta acceso a GitHub.
No entregar solo el ZIP cuando Moodle solicita los dos enlaces.

## 6. Explicación breve para la revisión

Flask define los registros temporales en app.py. Cada ruta envía su lista a una
plantilla mediante render_template. Jinja2 recorre los datos con for y determina
los estados con if/else. base.html reúne la estructura común e incluye los
componentes de navegación, aviso y pie. Los filtros dan formato a los datos.
GitHub Pages muestra una exportación HTML, mientras Flask se ejecuta localmente.

## Documentación técnica

- https://flask.palletsprojects.com/en/stable/quickstart/
- https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages
