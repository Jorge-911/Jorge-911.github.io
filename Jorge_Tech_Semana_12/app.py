from flask import Flask, render_template, redirect, url_for, flash
import os
import secrets
import sqlite3
from pathlib import Path
from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.proveedor_form import ProveedorForm
from forms.facturacion_form import FacturacionForm

app = Flask(__name__)
# Local classroom use: generated once per process; set SECRET_KEY in the environment for a stable key.
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY") or secrets.token_hex(32)
app.config["WTF_CSRF_ENABLED"] = True

# Información compartida del sistema: diccionario temporal, sin base de datos.
sistema = {"nombre": "Jorge Tech", "estudiante": "Jorge Manobanda",
           "asignatura": "Desarrollo Web", "anio": 2026, "avance": "12/16"}

@app.context_processor
def contexto_comun():
    return {"sistema": sistema}



# Ruta absoluta: funciona aunque Flask se inicie desde otro directorio.
app.config["DATABASE"] = os.environ.get("JORGE_TECH_DB") or str(
    Path(__file__).resolve().parent / "data" / "ferreteria.db"
)


def conectar_db():
    conn = sqlite3.connect(app.config["DATABASE"])
    conn.row_factory = sqlite3.Row
    return conn


def inicializar_db():
    Path(app.config["DATABASE"]).parent.mkdir(parents=True, exist_ok=True)
    conn = conectar_db()
    try:
        conn.execute("""CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo TEXT NOT NULL COLLATE NOCASE UNIQUE,
            nombre TEXT NOT NULL,
            categoria TEXT NOT NULL,
            precio_centavos INTEGER NOT NULL CHECK(precio_centavos > 0),
            stock INTEGER NOT NULL CHECK(stock >= 0)
        )""")
        conn.commit()
    finally:
        conn.close()


def consultar_productos():
    conn = conectar_db()
    try:
        return conn.execute("""SELECT id, codigo, nombre, categoria,
            precio_centavos / 100.0 AS precio, stock
            FROM productos ORDER BY id""").fetchall()
    finally:
        conn.close()


inicializar_db()

clientes_lista = [
    {"nombre": "Carlos Pérez", "servicio": "Soporte técnico", "telefono": "0987654321", "estado": "Pendiente"},
    {"nombre": "María López", "servicio": "Redes y conectividad", "telefono": "0991112233", "estado": "En proceso"},
    {"nombre": "Luis Andrade", "servicio": "Productos tecnológicos", "telefono": "0972223344", "estado": "Atendido"}
]

proveedores_lista = [
    {"empresa": "Tech Import", "producto": "Accesorios de computación", "contacto": "ventas@techimport.com", "ciudad": "Quito"},
    {"empresa": "Redes Ecuador", "producto": "Equipos de conectividad", "contacto": "info@redesecuador.com", "ciudad": "Guayaquil"},
    {"empresa": "Soluciones PC", "producto": "Repuestos y periféricos", "contacto": "contacto@solucionespc.com", "ciudad": "Cuenca"}
]

facturas = [
    {"numero": "F-001", "cliente": "Carlos Pérez", "detalle": "Mantenimiento de computadora", "total": 25.00, "estado": "Pagada"},
    {"numero": "F-002", "cliente": "María López", "detalle": "Configuración de router", "total": 18.00, "estado": "Pendiente"},
    {"numero": "F-003", "cliente": "Luis Andrade", "detalle": "Venta de accesorios", "total": 20.00, "estado": "Pagada"}
]

@app.route("/")
def inicio():
    servicios = [
        {"nombre": "Soporte técnico", "descripcion": "Mantenimiento preventivo y correctivo de computadoras, instalación de programas y revisión de fallas.", "icono": "💻"},
        {"nombre": "Redes y conectividad", "descripcion": "Configuración de routers, repetidores Wi-Fi, revisión de Internet y puntos de red.", "icono": "📡"},
        {"nombre": "Productos tecnológicos", "descripcion": "Venta y asesoría de accesorios tecnológicos como cables, adaptadores, mouse y teclados.", "icono": "🔌"}
    ]
    mensaje_bienvenida = "Soluciones tecnológicas a tu alcance"
    return render_template("index.html", servicios=servicios,
                           mensaje_bienvenida=mensaje_bienvenida, sistema=sistema)


@app.route("/productos")
def productos():
    return render_template("productos.html", productos=consultar_productos())


@app.route("/clientes")
def clientes():
    return render_template("clientes.html", clientes=clientes_lista)


@app.route("/proveedores")
def proveedores():
    return render_template("proveedores.html", proveedores=proveedores_lista)


@app.route("/facturacion")
def facturacion():
    return render_template("facturacion.html", facturas=facturas)



@app.route("/productos/nuevo", methods=["GET", "POST"])
def nuevo_producto():
    form = ProductoForm()
    if form.validate_on_submit():
        conn = conectar_db()
        try:
            # Solo se llega al INSERT tras superar WTForms y CSRF.
            conn.execute("""INSERT INTO productos
                (codigo, nombre, categoria, precio_centavos, stock)
                VALUES (?, ?, ?, ?, ?)""",
                (form.codigo.data, form.nombre.data, form.categoria.data,
                 int(form.precio.data * 100), form.stock.data))
            conn.commit()
        except sqlite3.IntegrityError:
            conn.rollback()
            form.codigo.errors.append("Este identificador ya está registrado.")
        except sqlite3.Error:
            conn.rollback()
            app.logger.exception("No se pudo guardar el producto")
            flash("No se pudo guardar el producto. Intente nuevamente.", "danger")
        else:
            flash("Producto guardado correctamente en SQLite.", "success")
            return redirect(url_for("productos"))
        finally:
            conn.close()
    return render_template("formulario_producto.html", form=form)


@app.route("/clientes/nuevo", methods=["GET", "POST"])
def nuevo_cliente():
    form = ClienteForm()
    if form.validate_on_submit():
        registro = {"nombre": form.nombre.data, "servicio": form.servicio.data, "telefono": form.telefono.data, "estado": form.estado.data}
        clientes_lista.append(registro)
        flash("Registro guardado correctamente. Los datos son temporales.", "success")
        return redirect(url_for("clientes"))
    return render_template("formulario_cliente.html", form=form)


@app.route("/proveedores/nuevo", methods=["GET", "POST"])
def nuevo_proveedor():
    form = ProveedorForm()
    if form.validate_on_submit():
        registro = {"empresa": form.empresa.data, "producto": form.producto.data, "contacto": form.contacto.data, "ciudad": form.ciudad.data}
        proveedores_lista.append(registro)
        flash("Registro guardado correctamente. Los datos son temporales.", "success")
        return redirect(url_for("proveedores"))
    return render_template("formulario_proveedor.html", form=form)


@app.route("/facturacion/nuevo", methods=["GET", "POST"])
def nuevo_facturacion():
    form = FacturacionForm()
    if form.validate_on_submit():
        if any(item["numero"].casefold() == form.numero.data.casefold() for item in facturas):
            form.numero.errors.append("Este identificador ya está registrado.")
        else:
            registro = {"numero": form.numero.data, "cliente": form.cliente.data, "detalle": form.detalle.data, "total": form.total.data, "estado": form.estado.data}
            facturas.append(registro)
            flash("Registro guardado correctamente. Los datos son temporales.", "success")
            return redirect(url_for("facturacion"))
    return render_template("formulario_facturacion.html", form=form)


if __name__ == "__main__":
    app.run()
