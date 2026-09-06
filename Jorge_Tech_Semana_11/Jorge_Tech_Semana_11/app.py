from flask import Flask, render_template, redirect, url_for, flash
import os
import secrets
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
           "asignatura": "Desarrollo Web", "anio": 2026, "avance": "11/16"}

@app.context_processor
def contexto_comun():
    return {"sistema": sistema}



productos_lista = [
    {"codigo": "P001", "nombre": "Cable de red UTP", "categoria": "Redes", "precio": 5.00, "stock": 12, "estado": "Disponible"},
    {"codigo": "P002", "nombre": "Mouse óptico", "categoria": "Accesorios", "precio": 8.00, "stock": 8, "estado": "Disponible"},
    {"codigo": "P003", "nombre": "Teclado USB", "categoria": "Accesorios", "precio": 12.00, "stock": 2, "estado": "Bajo stock"},
    {"codigo": "P004", "nombre": "Adaptador HDMI", "categoria": "Conectividad", "precio": 10.00, "stock": 0, "estado": "Agotado"}
]

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
    return render_template("productos.html", productos=productos_lista)


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
        if any(item["codigo"].casefold() == form.codigo.data.casefold() for item in productos_lista):
            form.codigo.errors.append("Este identificador ya está registrado.")
        else:
            registro = {"codigo": form.codigo.data, "nombre": form.nombre.data, "categoria": form.categoria.data, "precio": form.precio.data, "stock": form.stock.data}
            registro["estado"] = "Disponible" if registro["stock"] > 0 else "Agotado"
            productos_lista.append(registro)
            flash("Registro guardado correctamente. Los datos son temporales.", "success")
            return redirect(url_for("productos"))
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
