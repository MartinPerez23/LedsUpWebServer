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


document.addEventListener('DOMContentLoaded', function() {
    var spinner = document.getElementById('globalSpinner');
    if (spinner) spinner.style.display = 'none';

    // Detectar si el link es Fancybox
    function esFancyboxLink(link) {
        return (
            link.hasAttribute('data-fancybox') ||
            link.hasAttribute('data-src') ||
            link.hasAttribute('data-type') ||
            link.hasAttribute('data-caption')
        );
    }

    document.querySelectorAll('a[href]').forEach(function (link) {
        link.addEventListener('click', function (e) {
            const href = link.getAttribute('href');

            if (
                esFancyboxLink(link) ||
                link.hasAttribute('download') ||
                href?.startsWith('#') ||
                link.getAttribute('target') === '_blank'   
            ) {
                return;
            }

            setTimeout(function () {
                if (!e.defaultPrevented) {
                    spinner.style.display = 'flex';
                }
            }, 0);
        });
    });


    document.querySelectorAll('button[type="submit"], input[type="submit"]').forEach(function(btn) {
        btn.addEventListener('click', function(e) {
            setTimeout(function() {
                if (!e.defaultPrevented) spinner.style.display = 'flex';
            }, 0);
        });
    });

    window.addEventListener('pageshow', function() {
        if (spinner) spinner.style.display = 'none';
    });

    // ✅ PREVENIR spinner si Fancybox está abierto
    function fancyboxActivo() {
        return window.Fancybox?.getInstance?.() !== null;
    }

    window.addEventListener('beforeunload', function () {
        if (spinner && !fancyboxActivo()) {
            spinner.style.display = 'flex';
        }
    });

    window.addEventListener('popstate', function () {
        if (spinner && !fancyboxActivo()) {
            spinner.style.display = 'flex';
        }
    });

    // Oculta el spinner al abrir/cerrar cualquier Fancybox (v6)
    if (window.Fancybox && typeof window.Fancybox.bind === 'function') {
        window.Fancybox.bind('[data-fancybox]', {
            on: {
                close: () => {
                    if (spinner) spinner.style.display = 'none';
                },
                reveal: () => {
                    if (spinner) spinner.style.display = 'none';
                },
                destroy: () => {
                    if (spinner) spinner.style.display = 'none';
                },
                done: () => {
                    if (spinner) spinner.style.display = 'none';
                }
            }
        });
    }
});

