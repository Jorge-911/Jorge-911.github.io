// ==========================================================
// JORGE TECH
// Datos, plantillas reutilizables y validaciones dinámicas
// ==========================================================

// ----------------------------------------------------------
// 1. DATOS DEL PROYECTO REPRESENTADOS CON ARREGLOS Y OBJETOS
// En Flask, estos datos podrían llegar desde una ruta de Python.
// ----------------------------------------------------------

const serviciosProyecto = [
    {
        id: 1,
        titulo: "Soporte técnico",
        descripcion:
            "Mantenimiento preventivo y correctivo de equipos de computación.",
        icono: "💻",
        elementos: [
            "Limpieza de equipos",
            "Instalación de programas",
            "Revisión de fallas"
        ]
    },
    {
        id: 2,
        titulo: "Redes y conectividad",
        descripcion:
            "Configuración de redes para mejorar la conexión de hogares y negocios.",
        icono: "📡",
        elementos: [
            "Configuración de routers",
            "Instalación de repetidores Wi-Fi",
            "Revisión de Internet"
        ]
    },
    {
        id: 3,
        titulo: "Productos tecnológicos",
        descripcion:
            "Venta y asesoría de accesorios tecnológicos para uso diario.",
        icono: "🔌",
        elementos: [
            "Cables de red",
            "Mouse y teclados",
            "Adaptadores y accesorios"
        ]
    }
];

let solicitudes = [
    {
        id: 1001,
        nombre: "Carlos Pérez",
        descripcion:
            "Necesita revisar una computadora que se apaga después de varios minutos.",
        categoria: "Soporte técnico",
        estado: "Pendiente"
    },
    {
        id: 1002,
        nombre: "María López",
        descripcion:
            "Solicita mejorar la cobertura de la red inalámbrica de su pequeño negocio.",
        categoria: "Redes y conectividad",
        estado: "En proceso"
    }
];

let idSolicitudParaEliminar = null;

// ----------------------------------------------------------
// 2. REFERENCIAS A ELEMENTOS DEL DOM
// ----------------------------------------------------------

const listaServicios = document.getElementById("listaServicios");

const formularioSolicitud = document.getElementById(
    "formularioSolicitud"
);
const nombreSolicitud = document.getElementById("nombreSolicitud");
const descripcionSolicitud = document.getElementById(
    "descripcionSolicitud"
);
const categoriaSolicitud = document.getElementById(
    "categoriaSolicitud"
);
const estadoSolicitud = document.getElementById("estadoSolicitud");

const errorNombre = document.getElementById("errorNombre");
const errorDescripcion = document.getElementById(
    "errorDescripcion"
);
const errorCategoria = document.getElementById("errorCategoria");
const errorEstado = document.getElementById("errorEstado");

const contadorDescripcion = document.getElementById(
    "contadorDescripcion"
);
const mensajeValidacion = document.getElementById(
    "mensajeValidacion"
);
const spinnerRegistro = document.getElementById("spinnerRegistro");
const botonRegistrar = document.getElementById("botonRegistrar");
const listaSolicitudes = document.getElementById(
    "listaSolicitudes"
);
const totalRegistros = document.getElementById("totalRegistros");
const estadoVacio = document.getElementById("estadoVacio");

const modalDetallesContenido = document.getElementById("modalDetallesContenido");
const modalDetalles = new bootstrap.Modal(document.getElementById("modalDetalles"));
const modalConfirmarEliminar = new bootstrap.Modal(
    document.getElementById("modalConfirmarEliminar")
);
const botonConfirmarEliminar = document.getElementById("botonConfirmarEliminar");

// Reglas de validación
const LONGITUD_MINIMA_NOMBRE = 3;
const LONGITUD_MINIMA_DESCRIPCION = 20;
const LONGITUD_MAXIMA_DESCRIPCION = 250;

// ----------------------------------------------------------
// 3. PLANTILLAS REUTILIZABLES GENERADAS DESDE JAVASCRIPT
// Estas funciones simulan bloques repetitivos de una plantilla.
// ----------------------------------------------------------

function crearListaElementos(elementos) {
    const lista = document.createElement("ul");
    lista.classList.add("text-start");

    elementos.forEach(function (elemento) {
        const item = document.createElement("li");
        item.textContent = elemento;
        lista.appendChild(item);
    });

    return lista;
}

function crearTarjetaServicio(servicio) {
    const columna = document.createElement("article");
    columna.classList.add(
        "col-md-6",
        "col-lg-4",
        "render-animation"
    );

    const tarjeta = document.createElement("div");
    tarjeta.classList.add(
        "card",
        "service-card",
        "p-3",
        "h-100"
    );

    const cuerpo = document.createElement("div");
    cuerpo.classList.add("card-body", "text-center");

    const icono = document.createElement("div");
    icono.classList.add("service-icon");
    icono.setAttribute("aria-hidden", "true");
    icono.textContent = servicio.icono;

    const titulo = document.createElement("h3");
    titulo.classList.add("card-title", "h5");
    titulo.textContent = servicio.titulo;

    const descripcion = document.createElement("p");
    descripcion.classList.add("card-text");
    descripcion.textContent = servicio.descripcion;

    const boton = document.createElement("a");
    boton.classList.add("btn", "btn-primary");
    boton.href = "#registro";
    boton.textContent = "Solicitar";

    cuerpo.appendChild(icono);
    cuerpo.appendChild(titulo);
    cuerpo.appendChild(descripcion);
    cuerpo.appendChild(
        crearListaElementos(servicio.elementos)
    );
    cuerpo.appendChild(boton);

    tarjeta.appendChild(cuerpo);
    columna.appendChild(tarjeta);

    return columna;
}

function renderizarServicios() {
    listaServicios.textContent = "";

    // Estructura repetitiva para mostrar varios servicios
    serviciosProyecto.forEach(function (servicio) {
        listaServicios.appendChild(
            crearTarjetaServicio(servicio)
        );
    });
}

// ----------------------------------------------------------
// 4. VALIDACIONES DINÁMICAS Y REUTILIZABLES
// ----------------------------------------------------------

function obtenerContenedorError(campo) {
    if (campo === nombreSolicitud) {
        return errorNombre;
    }

    if (campo === descripcionSolicitud) {
        return errorDescripcion;
    }

    if (campo === categoriaSolicitud) {
        return errorCategoria;
    }

    return errorEstado;
}

function aplicarEstadoCampo(
    campo,
    esValido,
    mensajeError = ""
) {
    const contenedorError = obtenerContenedorError(campo);

    campo.classList.remove("is-valid", "is-invalid");

    if (esValido) {
        campo.classList.add("is-valid");
        contenedorError.textContent = "";
    } else {
        campo.classList.add("is-invalid");
        contenedorError.textContent = mensajeError;
    }

    return esValido;
}

function validarNombre() {
    const nombre = nombreSolicitud.value.trim();

    if (nombre === "") {
        return aplicarEstadoCampo(
            nombreSolicitud,
            false,
            "El nombre es obligatorio."
        );
    }

    if (nombre.length < LONGITUD_MINIMA_NOMBRE) {
        return aplicarEstadoCampo(
            nombreSolicitud,
            false,
            `El nombre debe contener al menos ${LONGITUD_MINIMA_NOMBRE} caracteres.`
        );
    }

    return aplicarEstadoCampo(nombreSolicitud, true);
}

function validarDescripcion() {
    const descripcion = descripcionSolicitud.value.trim();

    actualizarContadorDescripcion();

    if (descripcion === "") {
        return aplicarEstadoCampo(
            descripcionSolicitud,
            false,
            "La descripción es obligatoria."
        );
    }

    if (descripcion.length < LONGITUD_MINIMA_DESCRIPCION) {
        return aplicarEstadoCampo(
            descripcionSolicitud,
            false,
            `La descripción debe contener al menos ${LONGITUD_MINIMA_DESCRIPCION} caracteres.`
        );
    }

    return aplicarEstadoCampo(
        descripcionSolicitud,
        true
    );
}

function validarCategoria() {
    if (categoriaSolicitud.value === "") {
        return aplicarEstadoCampo(
            categoriaSolicitud,
            false,
            "Debe seleccionar una categoría."
        );
    }

    return aplicarEstadoCampo(
        categoriaSolicitud,
        true
    );
}

function validarEstado() {
    if (estadoSolicitud.value === "") {
        return aplicarEstadoCampo(
            estadoSolicitud,
            false,
            "Debe seleccionar un estado."
        );
    }

    return aplicarEstadoCampo(estadoSolicitud, true);
}

function validarFormularioCompleto() {
    const nombreValido = validarNombre();
    const descripcionValida = validarDescripcion();
    const categoriaValida = validarCategoria();
    const estadoValido = validarEstado();

    return (
        nombreValido &&
        descripcionValida &&
        categoriaValida &&
        estadoValido
    );
}

function actualizarContadorDescripcion() {
    const cantidad = descripcionSolicitud.value.length;

    contadorDescripcion.textContent =
        `${cantidad}/${LONGITUD_MAXIMA_DESCRIPCION}`;

    contadorDescripcion.classList.remove(
        "text-warning",
        "text-success"
    );

    if (
        cantidad > 0 &&
        cantidad < LONGITUD_MINIMA_DESCRIPCION
    ) {
        contadorDescripcion.classList.add("text-warning");
    }

    if (cantidad >= LONGITUD_MINIMA_DESCRIPCION) {
        contadorDescripcion.classList.add("text-success");
    }
}

function limpiarEstadosValidacion() {
    [
        nombreSolicitud,
        descripcionSolicitud,
        categoriaSolicitud,
        estadoSolicitud
    ].forEach(function (campo) {
        campo.classList.remove("is-valid", "is-invalid");
    });

    errorNombre.textContent = "";
    errorDescripcion.textContent = "";
    errorCategoria.textContent = "";
    errorEstado.textContent = "";

    actualizarContadorDescripcion();
}

// ----------------------------------------------------------
// 5. CONDICIONES SEGÚN EL ESTADO DE LOS DATOS
// ----------------------------------------------------------

function obtenerClaseEstado(estado) {
    if (estado === "Completado") {
        return "text-bg-success";
    }

    if (estado === "En proceso") {
        return "text-bg-warning";
    }

    return "text-bg-secondary";
}

function obtenerMensajeEstado(estado) {
    if (estado === "Completado") {
        return "La solicitud ya fue atendida.";
    }

    if (estado === "En proceso") {
        return "El servicio se encuentra en revisión.";
    }

    return "La solicitud está pendiente de atención.";
}

// ----------------------------------------------------------
// 6. CREACIÓN Y RENDERIZADO DE SOLICITUDES
// ----------------------------------------------------------

function crearTarjetaSolicitud(solicitud) {
    const columna = document.createElement("div");
    columna.classList.add("col-md-6", "render-animation");
    columna.dataset.id = solicitud.id;

    const tarjeta = document.createElement("article");
    tarjeta.classList.add("card", "request-card", "h-100");

    const cuerpo = document.createElement("div");
    cuerpo.classList.add("card-body", "d-flex", "flex-column");

    const filaEtiquetas = document.createElement("div");
    filaEtiquetas.classList.add("d-flex", "flex-wrap", "gap-2", "mb-3");

    const categoria = document.createElement("span");
    categoria.classList.add("badge", "text-bg-primary");
    categoria.textContent = solicitud.categoria;

    const estado = document.createElement("span");
    estado.classList.add("badge", obtenerClaseEstado(solicitud.estado));
    estado.textContent = solicitud.estado;

    const titulo = document.createElement("h3");
    titulo.classList.add("card-title", "h5");
    titulo.textContent = solicitud.nombre;

    const descripcion = document.createElement("p");
    descripcion.classList.add("card-text", "request-description");
    descripcion.textContent = solicitud.descripcion;

    const mensajeEstado = document.createElement("p");
    mensajeEstado.classList.add("small", "text-secondary", "mt-auto");
    mensajeEstado.textContent = obtenerMensajeEstado(solicitud.estado);

    const botones = document.createElement("div");
    botones.classList.add("d-flex", "flex-wrap", "gap-2", "mt-2");

    const botonDetalles = document.createElement("button");
    botonDetalles.type = "button";
    botonDetalles.classList.add("btn", "btn-success", "btn-sm");
    botonDetalles.textContent = "Ver detalles";
    botonDetalles.addEventListener("click", function () {
        mostrarDetallesSolicitud(solicitud.id);
    });

    const botonEliminar = document.createElement("button");
    botonEliminar.type = "button";
    botonEliminar.classList.add("btn", "btn-danger", "btn-sm");
    botonEliminar.textContent = "Eliminar";
    botonEliminar.addEventListener("click", function () {
        abrirConfirmacionEliminar(solicitud.id);
    });

    filaEtiquetas.appendChild(categoria);
    filaEtiquetas.appendChild(estado);

    botones.appendChild(botonDetalles);
    botones.appendChild(botonEliminar);

    cuerpo.appendChild(filaEtiquetas);
    cuerpo.appendChild(titulo);
    cuerpo.appendChild(descripcion);
    cuerpo.appendChild(mensajeEstado);
    cuerpo.appendChild(botones);

    tarjeta.appendChild(cuerpo);
    columna.appendChild(tarjeta);

    return columna;
}

function renderizarSolicitudes() {
    listaSolicitudes.textContent = "";

    // Condición: muestra un mensaje si no hay datos
    if (solicitudes.length === 0) {
        estadoVacio.classList.remove("d-none");
    } else {
        estadoVacio.classList.add("d-none");

        // Estructura repetitiva para varios registros
        solicitudes.forEach(function (solicitud) {
            listaSolicitudes.appendChild(
                crearTarjetaSolicitud(solicitud)
            );
        });
    }

    totalRegistros.textContent = solicitudes.length;
}

function mostrarDetallesSolicitud(id) {
    const solicitud = solicitudes.find(function (item) {
        return item.id === id;
    });

    if (!solicitud) {
        return;
    }

    modalDetallesContenido.textContent = "";

    const contenido = document.createElement("div");

    const nombre = document.createElement("p");
    nombre.innerHTML = `<strong>Cliente:</strong> ${solicitud.nombre}`;

    const categoria = document.createElement("p");
    categoria.innerHTML = `<strong>Categoría:</strong> ${solicitud.categoria}`;

    const estado = document.createElement("p");
    estado.innerHTML = `<strong>Estado:</strong> ${solicitud.estado}`;

    const descripcion = document.createElement("p");
    descripcion.innerHTML = `<strong>Descripción:</strong> ${solicitud.descripcion}`;

    const alerta = document.createElement("div");
    alerta.classList.add("alert", "alert-info", "mb-0");
    alerta.textContent = obtenerMensajeEstado(solicitud.estado);

    contenido.appendChild(nombre);
    contenido.appendChild(categoria);
    contenido.appendChild(estado);
    contenido.appendChild(descripcion);
    contenido.appendChild(alerta);

    modalDetallesContenido.appendChild(contenido);
    modalDetalles.show();
}

function abrirConfirmacionEliminar(id) {
    idSolicitudParaEliminar = id;
    modalConfirmarEliminar.show();
}

botonConfirmarEliminar.addEventListener("click", function () {
    if (idSolicitudParaEliminar === null) {
        return;
    }

    solicitudes = solicitudes.filter(function (solicitud) {
        return solicitud.id !== idSolicitudParaEliminar;
    });

    idSolicitudParaEliminar = null;
    modalConfirmarEliminar.hide();
    renderizarSolicitudes();

    mostrarAlerta(
        mensajeValidacion,
        "El registro fue eliminado correctamente.",
        "success"
    );
});


// ----------------------------------------------------------
// 7. EVENTOS// ----------------------------------------------------------
// 7. EVENTOS DEL FORMULARIO
// ----------------------------------------------------------

nombreSolicitud.addEventListener(
    "input",
    validarNombre
);
nombreSolicitud.addEventListener(
    "blur",
    validarNombre
);

descripcionSolicitud.addEventListener(
    "input",
    validarDescripcion
);
descripcionSolicitud.addEventListener(
    "blur",
    validarDescripcion
);

categoriaSolicitud.addEventListener(
    "change",
    validarCategoria
);
categoriaSolicitud.addEventListener(
    "blur",
    validarCategoria
);

estadoSolicitud.addEventListener(
    "change",
    validarEstado
);
estadoSolicitud.addEventListener(
    "blur",
    validarEstado
);

formularioSolicitud.addEventListener(
    "submit",
    function (evento) {
        evento.preventDefault();

        if (!validarFormularioCompleto()) {
            mostrarAlerta(
                mensajeValidacion,
                "Revise los campos marcados en rojo antes de registrar.",
                "danger"
            );

            const primerCampoInvalido =
                formularioSolicitud.querySelector(".is-invalid");

            if (primerCampoInvalido) {
                primerCampoInvalido.focus();
            }

            return;
        }

        spinnerRegistro.classList.remove("d-none");
        spinnerRegistro.classList.add("d-flex");
        botonRegistrar.disabled = true;

        window.setTimeout(function () {
            const nuevaSolicitud = {
                id: Date.now(),
                nombre: nombreSolicitud.value.trim(),
                descripcion: descripcionSolicitud.value.trim(),
                categoria: categoriaSolicitud.value,
                estado: estadoSolicitud.value
            };

            solicitudes.push(nuevaSolicitud);
            renderizarSolicitudes();

            mostrarAlerta(
                mensajeValidacion,
                "La solicitud fue registrada correctamente.",
                "success"
            );

            formularioSolicitud.reset();
            limpiarEstadosValidacion();

            spinnerRegistro.classList.add("d-none");
            spinnerRegistro.classList.remove("d-flex");
            botonRegistrar.disabled = false;
            nombreSolicitud.focus();
        }, 800);
    }
);


// ----------------------------------------------------------
// 8. ALERTAS// ----------------------------------------------------------
// 8. ALERTAS DINÁMICAS CON BOOTSTRAP
// ----------------------------------------------------------

function mostrarAlerta(
    contenedor,
    texto,
    tipo
) {
    contenedor.textContent = "";

    const alerta = document.createElement("div");
    alerta.classList.add(
        "alert",
        `alert-${tipo}`,
        "mb-0"
    );
    alerta.setAttribute("role", "alert");
    alerta.textContent = texto;

    contenedor.appendChild(alerta);

    window.setTimeout(function () {
        alerta.remove();
    }, 4500);
}

// ----------------------------------------------------------
// 9. FORMULARIO DE CONTACTO
// ----------------------------------------------------------

const formularioContacto = document.getElementById(
    "formularioContacto"
);
const mensajeContacto = document.getElementById(
    "mensajeContacto"
);

formularioContacto.addEventListener(
    "submit",
    function (evento) {
        evento.preventDefault();

        const nombre = document
            .getElementById("nombreContacto")
            .value.trim();
        const correo = document
            .getElementById("correoContacto")
            .value.trim();
        const asunto = document
            .getElementById("asuntoContacto")
            .value.trim();
        const mensaje = document
            .getElementById("mensajeContactoTexto")
            .value.trim();

        if (
            nombre === "" ||
            correo === "" ||
            asunto === "" ||
            mensaje === ""
        ) {
            mostrarAlerta(
                mensajeContacto,
                "Complete todos los campos del formulario de contacto.",
                "danger"
            );
            return;
        }

        mostrarAlerta(
            mensajeContacto,
            "Mensaje validado correctamente. Esta demostración no lo envía a un servidor.",
            "success"
        );

        formularioContacto.reset();
    }
);

// ----------------------------------------------------------
// 10. INICIALIZACIÓN DE LA APLICACIÓN
// ----------------------------------------------------------

function iniciarAplicacion() {
    renderizarServicios();
    renderizarSolicitudes();
    actualizarContadorDescripcion();
}

document.addEventListener(
    "DOMContentLoaded",
    iniciarAplicacion
);
