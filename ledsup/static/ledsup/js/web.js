document.addEventListener('DOMContentLoaded', () => {
    // Menú móvil
    const btn = document.getElementById('menu-btn');
    const menu = document.getElementById('mobile-menu');
    if (btn && menu) {
        btn.addEventListener('click', () => {
            menu.classList.toggle('hidden');
        });
    }

    // Carrusel
    let currIndex = 0;

    function showSlide(index) {
        const items = document.querySelectorAll('.carousel-item');
        items.forEach((item, i) => {
            item.classList.toggle('hidden', i !== index);
            item.classList.toggle('block', i === index);
        });
    }

    function nextSlide() {
        const items = document.querySelectorAll('.carousel-item');
        currIndex = (currIndex + 1) % items.length;
        showSlide(currIndex);
    }

    function prevSlide() {
        const items = document.querySelectorAll('.carousel-item');
        currIndex = (currIndex - 1 + items.length) % items.length;
        showSlide(currIndex);
    }

    // Botones del carrusel
    const prevBtn = document.getElementById('prev-slide');
    const nextBtn = document.getElementById('next-slide');

    if (prevBtn) prevBtn.addEventListener('click', prevSlide);
    if (nextBtn) nextBtn.addEventListener('click', nextSlide);

    // Inicializar Fancybox y mostrar el primer slide
    showSlide(currIndex);
    if (typeof Fancybox !== 'undefined') {
        const elements = [...document.querySelectorAll("[data-fancybox='gallery']")]
            .filter(el => el.getAttribute("href") && el.getAttribute("href") !== "undefined");

        if (elements.length > 0) {
            Fancybox.bind(elements);
        }
    }
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

    socket.onopen = function () {
        console.log('WebSocket conectado');
    }
    socket.onmessage = function (event) {
        const data = JSON.parse(event.data);
        console.log('Mensaje recibido:', data);

        recibido = true;

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
        if (!recibido) {
            setEstadoDesconectado();
        }
    };

    socket.onerror = function (error) {
        console.error('Error WebSocket:', error);
        if (!recibido) {
            setEstadoDesconectado();
        }
    };
})();

