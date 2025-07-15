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
        Fancybox.bind("[data-fancybox='gallery']");
    }
});

// Funciones para hCaptcha
window.onContactSubmit = function (token) {
    document.getElementById('ContactForm').submit();
};
window.onUserSubmit = function (token) {
    document.getElementById('UserForm').submit();
};
window.onLoginSubmit = function (token) {
    document.getElementById('LoginForm').submit();
};


function updateCharCount(input, counterId, maxLength) {
    const currentLength = input.value.length;
    const remaining = Math.max(0, maxLength - currentLength);
    const counter = document.getElementById(counterId);
    if (counter) {
        counter.textContent = `${remaining} caracteres restantes`;
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const fields = [
        {inputId: 'id_nombre', counterId: 'nombreCount', max: 30},
        {inputId: 'id_apellido', counterId: 'apellidoCount', max: 30},
        {inputId: 'id_mensaje', counterId: 'mensajeCount', max: 500}
    ];

    fields.forEach(({inputId, counterId, max}) => {
        const input = document.getElementById(inputId);
        if (input) {
            updateCharCount(input, counterId, max);
            input.addEventListener('input', () => {
                if (input.value.length > max) {
                    input.value = input.value.substring(0, max);
                }
                updateCharCount(input, counterId, max);
            });
        }
    });
});


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
