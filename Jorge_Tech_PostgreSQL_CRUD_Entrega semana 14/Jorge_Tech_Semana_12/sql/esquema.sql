-- Jorge Tech: estructura relacional PostgreSQL.
-- Ejecutar una vez en pgAdmin o psql después de crear la base jorge_tech.

CREATE TABLE IF NOT EXISTS proveedores (
    id SERIAL PRIMARY KEY,
    empresa VARCHAR(100) NOT NULL UNIQUE,
    producto_servicio VARCHAR(150) NOT NULL,
    contacto VARCHAR(120) NOT NULL,
    ciudad VARCHAR(60) NOT NULL
);

CREATE TABLE IF NOT EXISTS clientes (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    servicio VARCHAR(100) NOT NULL,
    telefono VARCHAR(10) NOT NULL,
    estado VARCHAR(20) NOT NULL
);

CREATE TABLE IF NOT EXISTS productos (
    id SERIAL PRIMARY KEY,
    proveedor_id INTEGER NOT NULL,
    codigo VARCHAR(20) NOT NULL UNIQUE,
    nombre VARCHAR(100) NOT NULL,
    categoria VARCHAR(60) NOT NULL,
    precio NUMERIC(10, 2) NOT NULL CHECK (precio > 0),
    stock INTEGER NOT NULL CHECK (stock >= 0),
    CONSTRAINT fk_productos_proveedores
        FOREIGN KEY (proveedor_id) REFERENCES proveedores(id)
        ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS facturas (
    id SERIAL PRIMARY KEY,
    cliente_id INTEGER NOT NULL,
    numero VARCHAR(20) NOT NULL UNIQUE,
    detalle VARCHAR(200) NOT NULL,
    total NUMERIC(10, 2) NOT NULL CHECK (total > 0),
    estado VARCHAR(20) NOT NULL,
    CONSTRAINT fk_facturas_clientes
        FOREIGN KEY (cliente_id) REFERENCES clientes(id)
        ON UPDATE CASCADE ON DELETE RESTRICT
);

-- Datos iniciales para que el formulario de Productos tenga proveedores disponibles.
INSERT INTO proveedores (empresa, producto_servicio, contacto, ciudad) VALUES
    ('Tech Import', 'Accesorios de computación', 'ventas@techimport.com', 'Quito'),
    ('Redes Ecuador', 'Equipos de conectividad', 'info@redesecuador.com', 'Guayaquil'),
    ('Soluciones PC', 'Repuestos y periféricos', 'contacto@solucionespc.com', 'Cuenca')
ON CONFLICT (empresa) DO NOTHING;

INSERT INTO clientes (nombre, servicio, telefono, estado) VALUES
    ('Carlos Pérez', 'Soporte técnico', '0987654321', 'Pendiente'),
    ('María López', 'Redes y conectividad', '0991112233', 'En proceso'),
    ('Luis Andrade', 'Productos tecnológicos', '0972223344', 'Atendido')
ON CONFLICT (nombre) DO NOTHING;

INSERT INTO productos (proveedor_id, codigo, nombre, categoria, precio, stock)
SELECT id, 'JT-001', 'Mouse inalámbrico', 'Accesorios', 18.50, 12
FROM proveedores WHERE empresa = 'Tech Import'
ON CONFLICT (codigo) DO NOTHING;

INSERT INTO productos (proveedor_id, codigo, nombre, categoria, precio, stock)
SELECT id, 'JT-002', 'Router Wi-Fi', 'Redes', 42.00, 5
FROM proveedores WHERE empresa = 'Redes Ecuador'
ON CONFLICT (codigo) DO NOTHING;

INSERT INTO facturas (cliente_id, numero, detalle, total, estado)
SELECT id, 'F-001', 'Mantenimiento de computadora', 25.00, 'Pagada'
FROM clientes WHERE nombre = 'Carlos Pérez'
ON CONFLICT (numero) DO NOTHING;
