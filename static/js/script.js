console.log("Jorge Tech Flask cargado correctamente.");
document.addEventListener("DOMContentLoaded", function () {
    const enlaces = document.querySelectorAll(".navbar .nav-link");
    const rutaActual = window.location.pathname;
    enlaces.forEach(function (enlace) {
        const rutaEnlace = new URL(enlace.href).pathname;
        enlace.classList.remove("active");
        if (rutaEnlace === rutaActual) {
            enlace.classList.add("active");
        }
    });
});
