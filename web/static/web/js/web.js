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

    document.querySelectorAll('a[href]').forEach(function(link) {
        link.addEventListener('click', function(e) {
            setTimeout(function() {
                if (!e.defaultPrevented && link.getAttribute('href') !== '#' && !link.hasAttribute('target')) {
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

    // Oculta el spinner al cargar la página (incluye navegación adelante/atrás)
    window.addEventListener('pageshow', function() {
        if (spinner) spinner.style.display = 'none';
    });

    // Muestra el spinner antes de recargar o navegar fuera de la página (F5, cerrar, cambiar de url, etc)
    window.addEventListener('beforeunload', function () {
        if (spinner) spinner.style.display = 'flex';
    });

    // Muestra el spinner al navegar con los botones del navegador (adelante/atrás)
    window.addEventListener('popstate', function () {
        if (spinner) spinner.style.display = 'flex';
    });
});

