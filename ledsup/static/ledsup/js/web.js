const btn = document.getElementById('menu-btn');
const menu = document.getElementById('mobile-menu');

btn.addEventListener('click', () => {
    menu.classList.toggle('hidden');
});

const estadoBadge = document.getElementById('estado-badge');
const estadoBadgeMobile = document.getElementById('estado-badge-mobile');

function setEstadoConectado() {
    [estadoBadge, estadoBadgeMobile].forEach(el => {
        if (el) {
            el.textContent = 'PC: Conectada';
            el.style.backgroundColor = '#00FFA3';
            el.style.color = '#0D1117';
        }
    });
}

function setEstadoDesconectado() {
    [estadoBadge, estadoBadgeMobile].forEach(el => {
        if (el) {
            el.textContent = 'PC: Desconectada';
            el.style.backgroundColor = '#9E00FF';
            el.style.color = '#FFFFFF';
        }
    });
}

function setEstadoCargando() {
    [estadoBadge, estadoBadgeMobile].forEach(el => {
        if (el) {
            el.textContent = 'PC: Cargando...';
            el.style.backgroundColor = '#FFA500'; // naranja
            el.style.color = '#0D1117';
        }
    });
}

(function () {
    setEstadoCargando();

    let recibido = false;
    const socketProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const socket = new WebSocket(socketProtocol + '//' + window.location.host + '/ws/estado/');

    const timeout = setTimeout(() => {
        if (!recibido) {
            setEstadoDesconectado();
        }
    }, 3000);

    socket.onopen = function () {
        console.log('WebSocket conectado');
    };

    socket.onmessage = function (event) {
        const data = JSON.parse(event.data);
        console.log('Mensaje recibido:', data);

        recibido = true;
        clearTimeout(timeout);

        if (data.estado === 'conectado') {
            setEstadoConectado();
        } else if (data.estado === 'desconectado') {
            setEstadoDesconectado();
        } else {
            setEstadoDesconectado();
        }
    };

    socket.onclose = function () {
        console.log('WebSocket cerrado');
        setEstadoDesconectado();
    };

    socket.onerror = function (error) {
        console.error('Error WebSocket:', error);
        setEstadoDesconectado();
    };
})();
