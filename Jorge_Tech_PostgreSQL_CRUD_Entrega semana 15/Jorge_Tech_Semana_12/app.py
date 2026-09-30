"""Aplicación Flask de Jorge Tech: PostgreSQL, CRUD y autenticación."""
import os
import secrets

from flask import Flask, abort, flash, redirect, render_template, request, url_for
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from psycopg import Error, IntegrityError
from werkzeug.security import check_password_hash, generate_password_hash

from conexion.conexion import inicializar_esquema, obtener_conexion, probar_conexion
from forms.cliente_form import ClienteForm
from forms.eliminar_form import EliminarForm
from forms.facturacion_form import FacturacionForm
from forms.login_form import LoginForm
from forms.producto_form import ProductoForm
from forms.proveedor_form import ProveedorForm
from forms.usuario_form import UsuarioForm
from models import Usuario


app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY") or secrets.token_hex(32)
app.config["WTF_CSRF_ENABLED"] = True

login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message = "Inicie sesión para acceder a esta página."
login_manager.login_message_category = "warning"

sistema = {
    "nombre": "Jorge Tech", "estudiante": "Jorge Manobanda",
    "asignatura": "Desarrollo de Aplicaciones Web", "anio": 2026,
    "avance": "Semana 15 · CRUD PostgreSQL y Login",
}

# En Render se crea automáticamente la estructura usando DATABASE_URL. En local
# también evita errores si la base está vacía; se puede desactivar con AUTO_INIT_DB=false.
if os.environ.get("AUTO_INIT_DB", "true").lower() == "true":
    try:
        inicializar_esquema()
    except Error:
        app.logger.warning("La base de datos aún no está disponible para inicializar el esquema.")


@app.context_processor
def contexto_comun():
    return {"sistema": sistema}


@login_manager.user_loader
def cargar_usuario(usuario_id):
    try:
        return Usuario.buscar_por_id(usuario_id)
    except Error:
        app.logger.exception("No se pudo recuperar la sesión del usuario")
        return None


def consultar_varios(consulta, parametros=()):
    """Ejecuta SELECT y fetchall(); siempre cierra cursor y conexión."""
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        cursor.execute(consulta, parametros)
        return cursor.fetchall()
    finally:
        cursor.close()
        conexion.close()


def consultar_uno(consulta, parametros=()):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        cursor.execute(consulta, parametros)
        return cursor.fetchone()
    finally:
        cursor.close()
        conexion.close()


def ejecutar_cambio(consulta, parametros=()):
    """Ejecuta INSERT, UPDATE o DELETE parametrizado y confirma con commit."""
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        cursor.execute(consulta, parametros)
        conexion.commit()
        return cursor.rowcount
    except Exception:
        conexion.rollback()
        raise
    finally:
        cursor.close()
        conexion.close()


def opciones_proveedores():
    return [(fila["id"], fila["empresa"]) for fila in consultar_varios(
        "SELECT id, empresa FROM proveedores ORDER BY empresa"
    )]


def opciones_clientes():
    return [(fila["id"], fila["nombre"]) for fila in consultar_varios(
        "SELECT id, nombre FROM clientes ORDER BY nombre"
    )]


def consultar_productos():
    return consultar_varios("""
        SELECT p.id, p.codigo, p.nombre, p.categoria, p.precio, p.stock,
               p.proveedor_id, pr.empresa AS proveedor
        FROM productos p INNER JOIN proveedores pr ON pr.id = p.proveedor_id
        ORDER BY p.id
    """)


def consultar_clientes():
    return consultar_varios("SELECT id, nombre, servicio, telefono, estado FROM clientes ORDER BY id")


def consultar_proveedores():
    return consultar_varios("""
        SELECT id, empresa, producto_servicio AS producto, contacto, ciudad
        FROM proveedores ORDER BY empresa
    """)


def consultar_facturas():
    """JOIN obligatorio: muestra el cliente que corresponde a cada factura."""
    return consultar_varios("""
        SELECT f.id, f.numero, f.detalle, f.total, f.estado, f.cliente_id,
               c.nombre AS cliente
        FROM facturas f INNER JOIN clientes c ON c.id = f.cliente_id
        ORDER BY f.id
    """)


def buscar_producto(producto_id):
    return consultar_uno("""
        SELECT id, proveedor_id, codigo, nombre, categoria, precio, stock
        FROM productos WHERE id = %s
    """, (producto_id,))


def buscar_cliente(cliente_id):
    return consultar_uno("SELECT id, nombre, servicio, telefono, estado FROM clientes WHERE id = %s", (cliente_id,))


def buscar_proveedor(proveedor_id):
    return consultar_uno("""
        SELECT id, empresa, producto_servicio AS producto, contacto, ciudad
        FROM proveedores WHERE id = %s
    """, (proveedor_id,))


def buscar_factura(factura_id):
    return consultar_uno("""
        SELECT id, cliente_id, numero, detalle, total, estado
        FROM facturas WHERE id = %s
    """, (factura_id,))


def configurar_proveedores(form):
    form.proveedor_id.choices = opciones_proveedores()


def configurar_clientes(form):
    form.cliente_id.choices = opciones_clientes()


def guardar_producto(form, producto_id=None):
    valores = (form.proveedor_id.data, form.codigo.data, form.nombre.data,
               form.categoria.data, form.precio.data, form.stock.data)
    if producto_id is None:
        return ejecutar_cambio("""
            INSERT INTO productos (proveedor_id, codigo, nombre, categoria, precio, stock)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, valores)
    return ejecutar_cambio("""
        UPDATE productos SET proveedor_id = %s, codigo = %s, nombre = %s,
        categoria = %s, precio = %s, stock = %s WHERE id = %s
    """, valores + (producto_id,))


def guardar_cliente(form, cliente_id=None):
    valores = (form.nombre.data, form.servicio.data, form.telefono.data, form.estado.data)
    if cliente_id is None:
        return ejecutar_cambio("""
            INSERT INTO clientes (nombre, servicio, telefono, estado) VALUES (%s, %s, %s, %s)
        """, valores)
    return ejecutar_cambio("""
        UPDATE clientes SET nombre = %s, servicio = %s, telefono = %s, estado = %s WHERE id = %s
    """, valores + (cliente_id,))


def guardar_proveedor(form, proveedor_id=None):
    valores = (form.empresa.data, form.producto.data, form.contacto.data, form.ciudad.data)
    if proveedor_id is None:
        return ejecutar_cambio("""
            INSERT INTO proveedores (empresa, producto_servicio, contacto, ciudad)
            VALUES (%s, %s, %s, %s)
        """, valores)
    return ejecutar_cambio("""
        UPDATE proveedores SET empresa = %s, producto_servicio = %s,
        contacto = %s, ciudad = %s WHERE id = %s
    """, valores + (proveedor_id,))


def guardar_factura(form, factura_id=None):
    valores = (form.cliente_id.data, form.numero.data, form.detalle.data, form.total.data, form.estado.data)
    if factura_id is None:
        return ejecutar_cambio("""
            INSERT INTO facturas (cliente_id, numero, detalle, total, estado)
            VALUES (%s, %s, %s, %s, %s)
        """, valores)
    return ejecutar_cambio("""
        UPDATE facturas SET cliente_id = %s, numero = %s, detalle = %s,
        total = %s, estado = %s WHERE id = %s
    """, valores + (factura_id,))


def eliminar_registro(tabla, registro_id):
    consultas = {
        "productos": "DELETE FROM productos WHERE id = %s",
        "clientes": "DELETE FROM clientes WHERE id = %s",
        "proveedores": "DELETE FROM proveedores WHERE id = %s",
        "facturas": "DELETE FROM facturas WHERE id = %s",
    }
    return ejecutar_cambio(consultas[tabla], (registro_id,))


def registrar_usuario_db(nombre_usuario, password_hash):
    return ejecutar_cambio(
        "INSERT INTO usuarios (usuario, password) VALUES (%s, %s)",
        (nombre_usuario, password_hash),
    )


def formulario_eliminar_valido():
    form = EliminarForm()
    if not form.validate_on_submit():
        flash("No se pudo validar la eliminación. Intente nuevamente.", "danger")
        return False
    return True


def procesar_error_bd(error, campo=None):
    app.logger.exception("Error de PostgreSQL: %s", error)
    if campo is not None and isinstance(error, IntegrityError):
        campo.errors.append("Este valor ya está registrado o está relacionado con otro registro.")
    elif isinstance(error, IntegrityError):
        flash("No se puede eliminar este registro porque está relacionado con otra información.", "danger")
    else:
        flash("No fue posible completar la operación. Revise la conexión a PostgreSQL.", "danger")


@app.route("/")
def inicio():
    servicios = [
        {"nombre": "Soporte técnico", "descripcion": "Mantenimiento preventivo y correctivo de computadoras, instalación de programas y revisión de fallas.", "icono": "💻"},
        {"nombre": "Redes y conectividad", "descripcion": "Configuración de routers, repetidores Wi-Fi, revisión de Internet y puntos de red.", "icono": "📡"},
        {"nombre": "Productos tecnológicos", "descripcion": "Venta y asesoría de accesorios tecnológicos como cables, adaptadores, mouse y teclados.", "icono": "🔌"},
    ]
    return render_template("index.html", servicios=servicios,
                           mensaje_bienvenida="Soluciones tecnológicas a tu alcance")


@app.route("/registro", methods=["GET", "POST"])
def registro():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))
    form = UsuarioForm()
    if form.validate_on_submit():
        try:
            registrar_usuario_db(form.usuario.data, generate_password_hash(form.password.data))
        except Error as error:
            procesar_error_bd(error, form.usuario)
        else:
            flash("Usuario creado correctamente. Ahora puede iniciar sesión.", "success")
            return redirect(url_for("login"))
    return render_template("registro.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))
    form = LoginForm()
    if form.validate_on_submit():
        try:
            usuario = Usuario.buscar_por_nombre(form.usuario.data)
        except Error as error:
            procesar_error_bd(error)
        else:
            if usuario and check_password_hash(usuario.password_hash, form.password.data):
                login_user(usuario, remember=form.recordar.data)
                flash(f"Bienvenido/a, {usuario.usuario}.", "success")
                return redirect(url_for("dashboard"))
            flash("Usuario o contraseña incorrectos.", "danger")
    return render_template("login.html", form=form)


@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("La sesión se cerró correctamente.", "info")
    return redirect(url_for("login"))


@app.route("/productos")
@login_required
def productos():
    try:
        registros = consultar_productos()
    except Error as error:
        procesar_error_bd(error)
        registros = []
    return render_template("productos.html", productos=registros, form_eliminar=EliminarForm())


@app.route("/productos/nuevo", methods=["GET", "POST"])
@login_required
def nuevo_producto():
    form = ProductoForm()
    try:
        configurar_proveedores(form)
    except Error as error:
        procesar_error_bd(error)
    if form.validate_on_submit():
        try:
            guardar_producto(form)
        except Error as error:
            procesar_error_bd(error, form.codigo)
        else:
            flash("Producto registrado correctamente.", "success")
            return redirect(url_for("productos"))
    return render_template("formulario_producto.html", form=form, titulo_formulario="Registrar producto", volver="productos")


@app.route("/productos/<int:producto_id>/editar", methods=["GET", "POST"])
@login_required
def editar_producto(producto_id):
    try:
        producto = buscar_producto(producto_id)
        if producto is None:
            abort(404)
        form = ProductoForm(data=producto) if request.method == "GET" else ProductoForm()
        configurar_proveedores(form)
    except Error as error:
        procesar_error_bd(error)
        return redirect(url_for("productos"))
    if form.validate_on_submit():
        try:
            if guardar_producto(form, producto_id) == 0:
                abort(404)
        except Error as error:
            procesar_error_bd(error, form.codigo)
        else:
            flash("Producto modificado correctamente.", "success")
            return redirect(url_for("productos"))
    return render_template("formulario_producto.html", form=form, titulo_formulario="Modificar producto", volver="productos")


@app.post("/productos/<int:producto_id>/eliminar")
@login_required
def eliminar_producto(producto_id):
    if formulario_eliminar_valido():
        try:
            if eliminar_registro("productos", producto_id) == 0:
                abort(404)
        except Error as error:
            procesar_error_bd(error)
        else:
            flash("Producto eliminado correctamente.", "success")
    return redirect(url_for("productos"))


@app.route("/clientes")
@login_required
def clientes():
    try:
        registros = consultar_clientes()
    except Error as error:
        procesar_error_bd(error)
        registros = []
    return render_template("clientes.html", clientes=registros, form_eliminar=EliminarForm())


@app.route("/clientes/nuevo", methods=["GET", "POST"])
@login_required
def nuevo_cliente():
    form = ClienteForm()
    if form.validate_on_submit():
        try:
            guardar_cliente(form)
        except Error as error:
            procesar_error_bd(error, form.nombre)
        else:
            flash("Cliente registrado correctamente.", "success")
            return redirect(url_for("clientes"))
    return render_template("formulario_cliente.html", form=form, titulo_formulario="Registrar cliente", volver="clientes")


@app.route("/clientes/<int:cliente_id>/editar", methods=["GET", "POST"])
@login_required
def editar_cliente(cliente_id):
    try:
        cliente = buscar_cliente(cliente_id)
        if cliente is None:
            abort(404)
    except Error as error:
        procesar_error_bd(error)
        return redirect(url_for("clientes"))
    form = ClienteForm(data=cliente) if request.method == "GET" else ClienteForm()
    if form.validate_on_submit():
        try:
            if guardar_cliente(form, cliente_id) == 0:
                abort(404)
        except Error as error:
            procesar_error_bd(error, form.nombre)
        else:
            flash("Cliente modificado correctamente.", "success")
            return redirect(url_for("clientes"))
    return render_template("formulario_cliente.html", form=form, titulo_formulario="Modificar cliente", volver="clientes")


@app.post("/clientes/<int:cliente_id>/eliminar")
@login_required
def eliminar_cliente(cliente_id):
    if formulario_eliminar_valido():
        try:
            if eliminar_registro("clientes", cliente_id) == 0:
                abort(404)
        except Error as error:
            procesar_error_bd(error)
        else:
            flash("Cliente eliminado correctamente.", "success")
    return redirect(url_for("clientes"))


@app.route("/proveedores")
@login_required
def proveedores():
    try:
        registros = consultar_proveedores()
    except Error as error:
        procesar_error_bd(error)
        registros = []
    return render_template("proveedores.html", proveedores=registros, form_eliminar=EliminarForm())


@app.route("/proveedores/nuevo", methods=["GET", "POST"])
@login_required
def nuevo_proveedor():
    form = ProveedorForm()
    if form.validate_on_submit():
        try:
            guardar_proveedor(form)
        except Error as error:
            procesar_error_bd(error, form.empresa)
        else:
            flash("Proveedor registrado correctamente.", "success")
            return redirect(url_for("proveedores"))
    return render_template("formulario_proveedor.html", form=form, titulo_formulario="Registrar proveedor", volver="proveedores")


@app.route("/proveedores/<int:proveedor_id>/editar", methods=["GET", "POST"])
@login_required
def editar_proveedor(proveedor_id):
    try:
        proveedor = buscar_proveedor(proveedor_id)
        if proveedor is None:
            abort(404)
    except Error as error:
        procesar_error_bd(error)
        return redirect(url_for("proveedores"))
    form = ProveedorForm(data=proveedor) if request.method == "GET" else ProveedorForm()
    if form.validate_on_submit():
        try:
            if guardar_proveedor(form, proveedor_id) == 0:
                abort(404)
        except Error as error:
            procesar_error_bd(error, form.empresa)
        else:
            flash("Proveedor modificado correctamente.", "success")
            return redirect(url_for("proveedores"))
    return render_template("formulario_proveedor.html", form=form, titulo_formulario="Modificar proveedor", volver="proveedores")


@app.post("/proveedores/<int:proveedor_id>/eliminar")
@login_required
def eliminar_proveedor(proveedor_id):
    if formulario_eliminar_valido():
        try:
            if eliminar_registro("proveedores", proveedor_id) == 0:
                abort(404)
        except Error as error:
            procesar_error_bd(error)
        else:
            flash("Proveedor eliminado correctamente.", "success")
    return redirect(url_for("proveedores"))


@app.route("/facturacion")
@login_required
def facturacion():
    try:
        registros = consultar_facturas()
    except Error as error:
        procesar_error_bd(error)
        registros = []
    return render_template("facturacion.html", facturas=registros, form_eliminar=EliminarForm())


@app.route("/facturacion/nuevo", methods=["GET", "POST"])
@login_required
def nuevo_facturacion():
    form = FacturacionForm()
    try:
        configurar_clientes(form)
    except Error as error:
        procesar_error_bd(error)
    if form.validate_on_submit():
        try:
            guardar_factura(form)
        except Error as error:
            procesar_error_bd(error, form.numero)
        else:
            flash("Factura registrada correctamente.", "success")
            return redirect(url_for("facturacion"))
    return render_template("formulario_facturacion.html", form=form, titulo_formulario="Registrar factura", volver="facturacion")


@app.route("/facturacion/<int:factura_id>/editar", methods=["GET", "POST"])
@login_required
def editar_facturacion(factura_id):
    try:
        factura = buscar_factura(factura_id)
        if factura is None:
            abort(404)
        form = FacturacionForm(data=factura) if request.method == "GET" else FacturacionForm()
        configurar_clientes(form)
    except Error as error:
        procesar_error_bd(error)
        return redirect(url_for("facturacion"))
    if form.validate_on_submit():
        try:
            if guardar_factura(form, factura_id) == 0:
                abort(404)
        except Error as error:
            procesar_error_bd(error, form.numero)
        else:
            flash("Factura modificada correctamente.", "success")
            return redirect(url_for("facturacion"))
    return render_template("formulario_facturacion.html", form=form, titulo_formulario="Modificar factura", volver="facturacion")


@app.post("/facturacion/<int:factura_id>/eliminar")
@login_required
def eliminar_facturacion(factura_id):
    if formulario_eliminar_valido():
        try:
            if eliminar_registro("facturas", factura_id) == 0:
                abort(404)
        except Error as error:
            procesar_error_bd(error)
        else:
            flash("Factura eliminada correctamente.", "success")
    return redirect(url_for("facturacion"))


if __name__ == "__main__":
    estado, mensaje = probar_conexion()
    if not estado:
        app.logger.warning("PostgreSQL aún no está disponible: %s", mensaje)
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)
