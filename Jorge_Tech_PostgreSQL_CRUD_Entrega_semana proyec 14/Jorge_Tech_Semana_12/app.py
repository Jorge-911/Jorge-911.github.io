"""Aplicación principal de Jorge Tech.

El módulo Productos trabaja con PostgreSQL y conserva los formularios, plantillas,
componentes y rutas elaborados en las semanas anteriores.
"""
import os
import secrets

from flask import Flask, abort, flash, redirect, render_template, request, url_for
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from psycopg import Error, IntegrityError
from werkzeug.security import check_password_hash, generate_password_hash

from conexion.conexion import obtener_conexion, probar_conexion
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
    "nombre": "Jorge Tech",
    "estudiante": "Jorge Manobanda",
    "asignatura": "Desarrollo de Aplicaciones Web",
    "anio": 2026,
    "avance": "Base de datos PostgreSQL",
}


@app.context_processor
def contexto_comun():
    return {"sistema": sistema}


@login_manager.user_loader
def cargar_usuario(usuario_id):
    """Flask-Login recupera la sesión mediante el identificador almacenado."""
    try:
        return Usuario.buscar_por_id(usuario_id)
    except Error:
        app.logger.exception("No se pudo recuperar el usuario de la sesión")
        return None


def consultar_productos():
    """SELECT con JOIN: cada producto muestra su proveedor relacionado."""
    consulta = """
        SELECT p.id, p.codigo, p.nombre, p.categoria, p.precio, p.stock,
               pr.empresa AS proveedor
        FROM productos AS p
        INNER JOIN proveedores AS pr ON pr.id = p.proveedor_id
        ORDER BY p.id
    """
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        cursor.execute(consulta)
        return cursor.fetchall()  # Recupera varios registros para Jinja2.
    finally:
        cursor.close()
        conexion.close()


def consultar_proveedores_opciones():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        cursor.execute("SELECT id, empresa FROM proveedores ORDER BY empresa")
        return [(fila["id"], fila["empresa"]) for fila in cursor.fetchall()]
    finally:
        cursor.close()
        conexion.close()


def buscar_producto(producto_id):
    """Recupera únicamente el producto elegido mediante WHERE y parámetro."""
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        cursor.execute(
            """SELECT id, proveedor_id, codigo, nombre, categoria, precio, stock
               FROM productos WHERE id = %s""",
            (producto_id,),
        )
        return cursor.fetchone()
    finally:
        cursor.close()
        conexion.close()


def insertar_producto(formulario):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        cursor.execute(
            """INSERT INTO productos
               (proveedor_id, codigo, nombre, categoria, precio, stock)
               VALUES (%s, %s, %s, %s, %s, %s)""",
            (formulario.proveedor_id.data, formulario.codigo.data,
             formulario.nombre.data, formulario.categoria.data,
             formulario.precio.data, formulario.stock.data),
        )
        conexion.commit()
    except Exception:
        conexion.rollback()
        raise
    finally:
        cursor.close()
        conexion.close()


def actualizar_producto(producto_id, formulario):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        cursor.execute(
            """UPDATE productos
               SET proveedor_id = %s, codigo = %s, nombre = %s,
                   categoria = %s, precio = %s, stock = %s
               WHERE id = %s""",
            (formulario.proveedor_id.data, formulario.codigo.data,
             formulario.nombre.data, formulario.categoria.data,
             formulario.precio.data, formulario.stock.data, producto_id),
        )
        conexion.commit()
        return cursor.rowcount
    except Exception:
        conexion.rollback()
        raise
    finally:
        cursor.close()
        conexion.close()


def eliminar_producto_db(producto_id):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        cursor.execute("DELETE FROM productos WHERE id = %s", (producto_id,))
        conexion.commit()
        return cursor.rowcount
    except Exception:
        conexion.rollback()
        raise
    finally:
        cursor.close()
        conexion.close()


def registrar_usuario_db(nombre_usuario, password_hash):
    """INSERT parametrizado: la contraseña ya llega transformada en hash."""
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        cursor.execute(
            "INSERT INTO usuarios (usuario, password) VALUES (%s, %s)",
            (nombre_usuario, password_hash),
        )
        conexion.commit()
    except Exception:
        conexion.rollback()
        raise
    finally:
        cursor.close()
        conexion.close()


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
            # Werkzug genera un hash seguro; no se conserva el texto ingresado.
            password_hash = generate_password_hash(form.password.data)
            registrar_usuario_db(form.usuario.data, password_hash)
        except IntegrityError:
            form.usuario.errors.append("Este nombre de usuario ya está registrado.")
        except Error:
            app.logger.exception("No se pudo registrar el usuario")
            flash("No se pudo crear el usuario. Revise PostgreSQL.", "danger")
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
        except Error:
            app.logger.exception("No se pudo consultar el usuario")
            flash("No fue posible conectar con PostgreSQL.", "danger")
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
    except Error:
        app.logger.exception("No se pudo consultar PostgreSQL")
        flash("No fue posible conectar con PostgreSQL. Revise DATABASE_URL y ejecute sql/esquema.sql.", "danger")
        registros = []
    return render_template("productos.html", productos=registros,
                           form_eliminar=EliminarForm())


@app.route("/productos/nuevo", methods=["GET", "POST"])
@login_required
def nuevo_producto():
    form = ProductoForm()
    try:
        form.proveedor_id.choices = consultar_proveedores_opciones()
    except Error:
        app.logger.exception("No se pudo cargar proveedores")
        flash("Primero configure PostgreSQL y ejecute sql/esquema.sql.", "danger")
        form.proveedor_id.choices = []

    if form.validate_on_submit():
        try:
            insertar_producto(form)
        except IntegrityError:
            form.codigo.errors.append("Este código ya está registrado.")
        except Error:
            app.logger.exception("No se pudo guardar el producto")
            flash("No se pudo guardar el producto. Revise la conexión a PostgreSQL.", "danger")
        else:
            flash("Producto registrado correctamente en PostgreSQL.", "success")
            return redirect(url_for("productos"))
    return render_template("formulario_producto.html", form=form,
                           titulo_formulario="Registrar producto", volver="productos")


@app.route("/productos/<int:producto_id>/editar", methods=["GET", "POST"])
@login_required
def editar_producto(producto_id):
    try:
        producto = buscar_producto(producto_id)
        if producto is None:
            abort(404)
        form = ProductoForm(data=producto) if request.method == "GET" else ProductoForm()
        form.proveedor_id.choices = consultar_proveedores_opciones()
    except Error:
        app.logger.exception("No se pudo preparar la edición")
        flash("No fue posible consultar PostgreSQL.", "danger")
        return redirect(url_for("productos"))

    if form.validate_on_submit():
        try:
            if actualizar_producto(producto_id, form) == 0:
                abort(404)
        except IntegrityError:
            form.codigo.errors.append("Este código ya está registrado.")
        except Error:
            app.logger.exception("No se pudo actualizar el producto")
            flash("No se pudo actualizar el producto.", "danger")
        else:
            flash("Producto modificado correctamente.", "success")
            return redirect(url_for("productos"))
    return render_template("formulario_producto.html", form=form,
                           titulo_formulario="Modificar producto", volver="productos")


@app.post("/productos/<int:producto_id>/eliminar")
@login_required
def eliminar_producto(producto_id):
    form = EliminarForm()
    if not form.validate_on_submit():
        flash("No se pudo validar la eliminación. Intente nuevamente.", "danger")
        return redirect(url_for("productos"))
    try:
        if eliminar_producto_db(producto_id) == 0:
            abort(404)
    except Error:
        app.logger.exception("No se pudo eliminar el producto")
        flash("No se pudo eliminar el producto.", "danger")
    else:
        flash("Producto eliminado correctamente de PostgreSQL.", "success")
    return redirect(url_for("productos"))


# Los módulos anteriores se conservan para mantener la continuidad del proyecto.
clientes_lista = [
    {"nombre": "Carlos Pérez", "servicio": "Soporte técnico", "telefono": "0987654321", "estado": "Pendiente"},
    {"nombre": "María López", "servicio": "Redes y conectividad", "telefono": "0991112233", "estado": "En proceso"},
    {"nombre": "Luis Andrade", "servicio": "Productos tecnológicos", "telefono": "0972223344", "estado": "Atendido"},
]
proveedores_lista = [
    {"empresa": "Tech Import", "producto": "Accesorios de computación", "contacto": "ventas@techimport.com", "ciudad": "Quito"},
    {"empresa": "Redes Ecuador", "producto": "Equipos de conectividad", "contacto": "info@redesecuador.com", "ciudad": "Guayaquil"},
    {"empresa": "Soluciones PC", "producto": "Repuestos y periféricos", "contacto": "contacto@solucionespc.com", "ciudad": "Cuenca"},
]
facturas = [
    {"numero": "F-001", "cliente": "Carlos Pérez", "detalle": "Mantenimiento de computadora", "total": 25.00, "estado": "Pagada"},
    {"numero": "F-002", "cliente": "María López", "detalle": "Configuración de router", "total": 18.00, "estado": "Pendiente"},
    {"numero": "F-003", "cliente": "Luis Andrade", "detalle": "Venta de accesorios", "total": 20.00, "estado": "Pagada"},
]


@app.route("/clientes")
@login_required
def clientes():
    return render_template("clientes.html", clientes=clientes_lista)


@app.route("/proveedores")
@login_required
def proveedores():
    return render_template("proveedores.html", proveedores=proveedores_lista)


@app.route("/facturacion")
@login_required
def facturacion():
    return render_template("facturacion.html", facturas=facturas)


@app.route("/clientes/nuevo", methods=["GET", "POST"])
@login_required
def nuevo_cliente():
    form = ClienteForm()
    if form.validate_on_submit():
        clientes_lista.append({campo: getattr(form, campo).data for campo in ("nombre", "servicio", "telefono", "estado")})
        flash("Registro guardado correctamente. Los datos son temporales.", "success")
        return redirect(url_for("clientes"))
    return render_template("formulario_cliente.html", form=form)


@app.route("/proveedores/nuevo", methods=["GET", "POST"])
@login_required
def nuevo_proveedor():
    form = ProveedorForm()
    if form.validate_on_submit():
        proveedores_lista.append({"empresa": form.empresa.data, "producto": form.producto.data,
                                  "contacto": form.contacto.data, "ciudad": form.ciudad.data})
        flash("Registro guardado correctamente. Los datos son temporales.", "success")
        return redirect(url_for("proveedores"))
    return render_template("formulario_proveedor.html", form=form)


@app.route("/facturacion/nuevo", methods=["GET", "POST"])
@login_required
def nuevo_facturacion():
    form = FacturacionForm()
    if form.validate_on_submit():
        if any(item["numero"].casefold() == form.numero.data.casefold() for item in facturas):
            form.numero.errors.append("Este identificador ya está registrado.")
        else:
            facturas.append({"numero": form.numero.data, "cliente": form.cliente.data,
                             "detalle": form.detalle.data, "total": form.total.data,
                             "estado": form.estado.data})
            flash("Registro guardado correctamente. Los datos son temporales.", "success")
            return redirect(url_for("facturacion"))
    return render_template("formulario_facturacion.html", form=form)


if __name__ == "__main__":
    estado, mensaje = probar_conexion()
    if not estado:
        app.logger.warning("PostgreSQL aún no está disponible: %s", mensaje)
    app.run(debug=True)
