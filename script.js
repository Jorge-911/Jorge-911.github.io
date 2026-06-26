// Elementos principales del registro dinámico
const formularioSolicitud = document.getElementById("formularioSolicitud");
const nombreSolicitud = document.getElementById("nombreSolicitud");
const descripcionSolicitud = document.getElementById("descripcionSolicitud");
const categoriaSolicitud = document.getElementById("categoriaSolicitud");
const mensajeValidacion = document.getElementById("mensajeValidacion");
const listaSolicitudes = document.getElementById("listaSolicitudes");
const totalRegistros = document.getElementById("totalRegistros");
const estadoVacio = document.getElementById("estadoVacio");

// Arreglo que almacena los registros durante la sesión
let solicitudes = [];

// Captura del evento submit mediante addEventListener
formularioSolicitud.addEventListener("submit", function (evento) {
    // Evita que la página se recargue
    evento.preventDefault();

    const nombre = nombreSolicitud.value.trim();
    const descripcion = descripcionSolicitud.value.trim();
    const categoria = categoriaSolicitud.value.trim();

    // Validación de campos vacíos
    if (nombre === "" || descripcion === "" || categoria === "") {
        mostrarMensaje(
            mensajeValidacion,
            "Todos los campos son obligatorios. Complete la información antes de continuar.",
            "danger"
        );
        return;
    }

    const nuevaSolicitud = {
        id: Date.now(),
        nombre: nombre,
        descripcion: descripcion,
        categoria: categoria
    };

    solicitudes.push(nuevaSolicitud);
    crearTarjetaSolicitud(nuevaSolicitud);
    actualizarTotal();

    mostrarMensaje(
        mensajeValidacion,
        "La solicitud fue registrada correctamente.",
        "success"
    );

    formularioSolicitud.reset();
    nombreSolicitud.focus();
});

// Crea elementos HTML dinámicamente con createElement()
function crearTarjetaSolicitud(solicitud) {
    const columna = document.createElement("div");
    columna.classList.add("col-md-6");
    columna.dataset.id = solicitud.id;

    const tarjeta = document.createElement("article");
    tarjeta.classList.add("card", "request-card", "h-100");

    const cuerpo = document.createElement("div");
    cuerpo.classList.add("card-body", "d-flex", "flex-column");

    const categoria = document.createElement("span");
    categoria.classList.add("badge", "text-bg-primary", "align-self-start", "mb-3");
    categoria.textContent = solicitud.categoria;

    const titulo = document.createElement("h3");
    titulo.classList.add("card-title", "h5");
    titulo.textContent = solicitud.nombre;

    const descripcion = document.createElement("p");
    descripcion.classList.add("card-text", "request-description", "flex-grow-1");
    descripcion.textContent = solicitud.descripcion;

    const botonEliminar = document.createElement("button");
    botonEliminar.type = "button";
    botonEliminar.classList.add("btn", "btn-danger", "mt-2");
    botonEliminar.textContent = "Eliminar registro";

    // Evento click para eliminar el registro
    botonEliminar.addEventListener("click", function () {
        eliminarSolicitud(solicitud.id, columna);
    });

    // Se agregan los elementos usando appendChild()
    cuerpo.appendChild(categoria);
    cuerpo.appendChild(titulo);
    cuerpo.appendChild(descripcion);
    cuerpo.appendChild(botonEliminar);
    tarjeta.appendChild(cuerpo);
    columna.appendChild(tarjeta);
    listaSolicitudes.appendChild(columna);
}

// Elimina el registro seleccionado
function eliminarSolicitud(id, elementoHTML) {
    solicitudes = solicitudes.filter(function (solicitud) {
        return solicitud.id !== id;
    });

    elementoHTML.remove();
    actualizarTotal();

    mostrarMensaje(
        mensajeValidacion,
        "El registro fue eliminado correctamente.",
        "warning"
    );
}

// Actualiza el contador total
function actualizarTotal() {
    totalRegistros.textContent = solicitudes.length;

    if (solicitudes.length === 0) {
        estadoVacio.classList.remove("d-none");
    } else {
        estadoVacio.classList.add("d-none");
    }
}

// Muestra mensajes dinámicos de validación
function mostrarMensaje(contenedor, texto, tipo) {
    contenedor.textContent = "";

    const alerta = document.createElement("div");
    alerta.classList.add("alert", `alert-${tipo}`, "mb-0");
    alerta.setAttribute("role", "alert");
    alerta.textContent = texto;

    contenedor.appendChild(alerta);

    window.setTimeout(function () {
        alerta.remove();
    }, 4000);
}

// Formulario de contacto: demostración adicional sin recargar la página
const formularioContacto = document.getElementById("formularioContacto");
const mensajeContacto = document.getElementById("mensajeContacto");

formularioContacto.addEventListener("submit", function (evento) {
    evento.preventDefault();

    const nombre = document.getElementById("nombreContacto").value.trim();
    const correo = document.getElementById("correoContacto").value.trim();
    const asunto = document.getElementById("asuntoContacto").value.trim();
    const mensaje = document.getElementById("mensajeContactoTexto").value.trim();

    if (nombre === "" || correo === "" || asunto === "" || mensaje === "") {
        mostrarMensaje(
            mensajeContacto,
            "Complete todos los campos del formulario de contacto.",
            "danger"
        );
        return;
    }

    mostrarMensaje(
        mensajeContacto,
        "Mensaje registrado correctamente. Esta demostración no envía datos a un servidor.",
        "success"
    );

    formularioContacto.reset();
});

// Estado inicial del contador
actualizarTotal();