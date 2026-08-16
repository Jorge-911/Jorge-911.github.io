from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def inicio():
    servicios = [
        {"nombre": "Soporte técnico", "descripcion": "Mantenimiento preventivo y correctivo de computadoras, instalación de programas y revisión de fallas.", "icono": "💻"},
        {"nombre": "Redes y conectividad", "descripcion": "Configuración de routers, repetidores Wi-Fi, revisión de Internet y puntos de red.", "icono": "📡"},
        {"nombre": "Productos tecnológicos", "descripcion": "Venta y asesoría de accesorios tecnológicos como cables, adaptadores, mouse y teclados.", "icono": "🔌"}
    ]
    return render_template("index.html", servicios=servicios)


@app.route("/productos")
def productos():
    productos_lista = [
        {"codigo": "P001", "nombre": "Cable de red UTP", "categoria": "Redes", "precio": 5.00, "estado": "Disponible"},
        {"codigo": "P002", "nombre": "Mouse óptico", "categoria": "Accesorios", "precio": 8.00, "estado": "Disponible"},
        {"codigo": "P003", "nombre": "Teclado USB", "categoria": "Accesorios", "precio": 12.00, "estado": "Bajo stock"},
        {"codigo": "P004", "nombre": "Adaptador HDMI", "categoria": "Conectividad", "precio": 10.00, "estado": "Disponible"}
    ]
    return render_template("productos.html", productos=productos_lista)


@app.route("/clientes")
def clientes():
    clientes_lista = [
        {"nombre": "Carlos Pérez", "servicio": "Soporte técnico", "telefono": "0987654321", "estado": "Pendiente"},
        {"nombre": "María López", "servicio": "Redes y conectividad", "telefono": "0991112233", "estado": "En proceso"},
        {"nombre": "Luis Andrade", "servicio": "Productos tecnológicos", "telefono": "0972223344", "estado": "Atendido"}
    ]
    return render_template("clientes.html", clientes=clientes_lista)


@app.route("/proveedores")
def proveedores():
    proveedores_lista = [
        {"empresa": "Tech Import", "producto": "Accesorios de computación", "contacto": "ventas@techimport.com", "ciudad": "Quito"},
        {"empresa": "Redes Ecuador", "producto": "Equipos de conectividad", "contacto": "info@redesecuador.com", "ciudad": "Guayaquil"},
        {"empresa": "Soluciones PC", "producto": "Repuestos y periféricos", "contacto": "contacto@solucionespc.com", "ciudad": "Cuenca"}
    ]
    return render_template("proveedores.html", proveedores=proveedores_lista)


@app.route("/facturacion")
def facturacion():
    facturas = [
        {"numero": "F-001", "cliente": "Carlos Pérez", "detalle": "Mantenimiento de computadora", "total": 25.00, "estado": "Pagada"},
        {"numero": "F-002", "cliente": "María López", "detalle": "Configuración de router", "total": 18.00, "estado": "Pendiente"},
        {"numero": "F-003", "cliente": "Luis Andrade", "detalle": "Venta de accesorios", "total": 20.00, "estado": "Pagada"}
    ]
    return render_template("facturacion.html", facturas=facturas)


if __name__ == "__main__":
    app.run(debug=True)
