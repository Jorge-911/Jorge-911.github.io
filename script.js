// ==========================================================
// JORGE TECH - VALIDACIONES DINÁMICAS Y MANIPULACIÓN DEL DOM
// ==========================================================

// Elementos del formulario de solicitudes
const formularioSolicitud = document.getElementById("formularioSolicitud");
const nombreSolicitud = document.getElementById("nombreSolicitud");
const descripcionSolicitud = document.getElementById("descripcionSolicitud");
const categoriaSolicitud = document.getElementById("categoriaSolicitud");

const errorNombre = document.getElementById("errorNombre");
const errorDescripcion = document.getElementById("errorDescripcion");
const errorCategoria = document.getElementById("errorCategoria");
const contadorDescripcion = document.getElementById("contadorDescripcion");

const mensajeValidacion = document.getElementById("mensajeValidacion");
const listaSolicitudes = document.getElementById("listaSolicitudes");
const totalRegistros = document.getElementById("totalRegistros");
const estadoVacio = document.getElementById("estadoVacio");

// Arreglo de registros creados durante la sesión
let solicitudes = [];

// Reglas de validación
const LONGITUD_MINIMA_NOMBRE = 3;
const LONGITUD_MINIMA_DESCRIPCION = 20;
const LONGITUD_MAXIMA_DESCRIPCION = 250;

// ----------------------------------------------------------
// Funciones reutilizables de validación
// ----------------------------------------------------------

function aplicarEstadoCampo(campo, esValido, mensajeError = "") {
    campo.classList.remove("is-valid", "is-invalid");

    if (esValido) {
        campo.classList.add("is-valid");
    } else {
        campo.classList.add("is-invalid");
    }

    if (campo === nombreSolicitud) {
        errorNombre.textContent = mensajeError;
    }

    if (campo === descripcionSolicitud) {
        errorDescripcion.textContent = mensajeError;
    }

    if (campo === categoriaSolicitud) {
        errorCategoria.textContent = mensajeError;
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

    return aplicarEstadoCampo(descripcionSolicitud, true);
}

function validarCategoria() {
    const categoria = categoriaSolicitud.value.trim();

    if (categoria === "") {
        return aplicarEstadoCampo(
            categoriaSolicitud,
            false,
            "Debe seleccionar una categoría."
        );
    }

    return aplicarEstadoCampo(categoriaSolicitud, true);
}

function validarFormularioCompleto() {
    const nombreValido = validarNombre();
    const descripcionValida = validarDescripcion();
    const categoriaValida = validarCategoria();

    return nombreValido && descripcionValida && categoriaValida;
}

function actualizarContadorDescripcion() {
    const cantidad = descripcionSolicitud.value.length;
    contadorDescripcion.textContent = `${cantidad}/${LONGITUD_MAXIMA_DESCRIPCION}`;

    contadorDescripcion.classList.remove(
        "text-danger",
        "text-warning",
        "text-success"
    );

    if (cantidad === 0) {
        return;
    }

    if (cantidad < LONGITUD_MINIMA_DESCRIPCION) {
        contadorDescripcion.classList.add("text-warning");
    } else {
        contadorDescripcion.classList.add("text-success");
    }
}

function limpiarEstadosValidacion() {
    [nombreSolicitud, descripcionSolicitud, categoriaSolicitud].forEach(
        function (campo) {
            campo.classList.remove("is-valid", "is-invalid");
        }
    );

    errorNombre.textContent = "";
    errorDescripcion.textContent = "";
    errorCategoria.textContent = "";
    actualizarContadorDescripcion();
}

// ----------------------------------------------------------
// Eventos en tiempo real: input, blur, change y submit
// ----------------------------------------------------------

// Valida mientras el usuario escribe
nombreSolicitud.addEventListener("input", validarNombre);
descripcionSolicitud.addEventListener("input", validarDescripcion);

// Valida cuando el usuario sale del campo
nombreSolicitud.addEventListener("blur", validarNombre);
descripcionSolicitud.addEventListener("blur", validarDescripcion);
categoriaSolicitud.addEventListener("blur", validarCategoria);

// El select se valida inmediatamente al cambiar
categoriaSolicitud.addEventListener("change", validarCategoria);

// Captura el envío y evita que la página se recargue
formularioSolicitud.addEventListener("submit", function (evento) {
    evento.preventDefault();

    const formularioValido = validarFormularioCompleto();

    if (!formularioValido) {
        mostrarAlerta(
            mensajeValidacion,
            "Revise los campos marcados en rojo antes de registrar la solicitud.",
            "danger"
        );

        const primerCampoInvalido =
            formularioSolicitud.querySelector(".is-invalid");

        if (primerCampoInvalido) {
            primerCampoInvalido.focus();
        }

        return;
    }

    const nuevaSolicitud = {
        id: Date.now(),
        nombre: nombreSolicitud.value.trim(),
        descripcion: descripcionSolicitud.value.trim(),
        categoria: categoriaSolicitud.value
    };

    solicitudes.push(nuevaSolicitud);
    crearTarjetaSolicitud(nuevaSolicitud);
    actualizarTotal();

    mostrarAlerta(
        mensajeValidacion,
        "La solicitud fue registrada correctamente.",
        "success"
    );

    formularioSolicitud.reset();
    limpiarEstadosValidacion();
    nombreSolicitud.focus();
});

// ----------------------------------------------------------
// Creación, visualización, conteo y eliminación de registros
// ----------------------------------------------------------

function crearTarjetaSolicitud(solicitud) {
    const columna = document.createElement("div");
    columna.classList.add("col-md-6", "record-animation");
    columna.dataset.id = solicitud.id;

    const tarjeta = document.createElement("article");
    tarjeta.classList.add("card", "request-card", "h-100");

    const cuerpo = document.createElement("div");
    cuerpo.classList.add("card-body", "d-flex", "flex-column");

    const categoria = document.createElement("span");
    categoria.classList.add(
        "badge",
        "text-bg-primary",
        "align-self-start",
        "mb-3"
    );
    categoria.textContent = solicitud.categoria;

    const titulo = document.createElement("h3");
    titulo.classList.add("card-title", "h5");
    titulo.textContent = solicitud.nombre;

    const descripcion = document.createElement("p");
    descripcion.classList.add(
        "card-text",
        "request-description",
        "flex-grow-1"
    );
    descripcion.textContent = solicitud.descripcion;

    const botonEliminar = document.createElement("button");
    botonEliminar.type = "button";
    botonEliminar.classList.add("btn", "btn-danger", "mt-2");
    botonEliminar.textContent = "Eliminar registro";
    botonEliminar.setAttribute(
        "aria-label",
        `Eliminar solicitud de ${solicitud.nombre}`
    );

    botonEliminar.addEventListener("click", function () {
        eliminarSolicitud(solicitud.id, columna);
    });

    // appendChild() agrega cada elemento creado al DOM
    cuerpo.appendChild(categoria);
    cuerpo.appendChild(titulo);
    cuerpo.appendChild(descripcion);
    cuerpo.appendChild(botonEliminar);

    tarjeta.appendChild(cuerpo);
    columna.appendChild(tarjeta);
    listaSolicitudes.appendChild(columna);
}

function eliminarSolicitud(id, elementoHTML) {
    solicitudes = solicitudes.filter(function (solicitud) {
        return solicitud.id !== id;
    });

    elementoHTML.remove();
    actualizarTotal();

    mostrarAlerta(
        mensajeValidacion,
        "El registro fue eliminado correctamente.",
        "success"
    );
}

function actualizarTotal() {
    totalRegistros.textContent = solicitudes.length;

    if (solicitudes.length === 0) {
        estadoVacio.classList.remove("d-none");
    } else {
        estadoVacio.classList.add("d-none");
    }
}

// ----------------------------------------------------------
// Alertas dinámicas con clases de Bootstrap
// ----------------------------------------------------------

function mostrarAlerta(contenedor, texto, tipo) {
    contenedor.textContent = "";

    const alerta = document.createElement("div");
    alerta.classList.add("alert", `alert-${tipo}`, "mb-0");
    alerta.setAttribute("role", "alert");
    alerta.textContent = texto;

    contenedor.appendChild(alerta);

    window.setTimeout(function () {
        alerta.remove();
    }, 4500);
}

// ----------------------------------------------------------
// Formulario de contacto de demostración
// ----------------------------------------------------------

const formularioContacto = document.getElementById("formularioContacto");
const mensajeContacto = document.getElementById("mensajeContacto");

formularioContacto.addEventListener("submit", function (evento) {
    evento.preventDefault();

    const nombre = document.getElementById("nombreContacto").value.trim();
    const correo = document.getElementById("correoContacto").value.trim();
    const asunto = document.getElementById("asuntoContacto").value.trim();
    const mensaje = document
        .getElementById("mensajeContactoTexto")
        .value.trim();

    if (nombre === "" || correo === "" || asunto === "" || mensaje === "") {
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
});

// Estado inicial de la aplicación
actualizarContadorDescripcion();
actualizarTotal();
