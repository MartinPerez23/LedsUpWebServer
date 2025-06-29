document.addEventListener('DOMContentLoaded', function () {
    const estadoBadge = document.getElementById('estado-badge');
    const estadoBadgeMobile = document.getElementById('estado-badge-mobile');
    const mensajeError = document.getElementById('mensaje-error');

    const botones = document.querySelectorAll('.btn-probar');

    botones.forEach(function (btn) {
        btn.addEventListener('click', function (e) {
            const textoEstado = [
                estadoBadge?.textContent || '',
                estadoBadgeMobile?.textContent || ''
            ].join(' ');

            if (textoEstado.includes("Desconectada")) {
                e.preventDefault();
                mostrarError("No hay conexión con la PC. Conéctela para enviar comandos.");
                return;
            }

            if (textoEstado.includes("Cargando")) {
                e.preventDefault();
                mostrarError("Esperando conexión con la PC...");
            }
        });
    });

    function mostrarError(mensaje) {
        mensajeError.textContent = mensaje;
        mensajeError.classList.remove('hidden');
        setTimeout(() => {
            mensajeError.classList.add('hidden');
        }, 5000);
    }
});
