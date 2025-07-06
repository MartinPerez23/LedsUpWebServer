// Funciones auxiliares y variables globales
function limpiarDisplay() {
    clearInterval(scroll);
    clearInterval(scan);
    clearInterval(estrellas);
    clearInterval(colorCambioConstante);

    numeroColorCambioConstante = 0;
    numeroScroll = 0;
    numeroScan = 0;

    for (let f = 0; f < matriz[0].length; f++) {
        for (let c = 0; c < matriz[0].length; c++) {
            contextoDisplay.fillStyle = colores[13];
            contextoDisplay.fill(matriz[f][c]);
        }
    }
}

function getRandomInt(min, max) {
    return Math.floor(Math.random() * (max - min)) + min;
}

// Canvas y contextos
const canvas = document.getElementById('circulo');
const ctx = canvas.getContext('2d');
const centerCircleX = canvas.width / 2;
const centerCircleY = canvas.height / 2;
const $display = document.querySelector("#display");
const contextoDisplay = $display.getContext("2d");

// Elementos DOM
const dirScroll = document.getElementById('dirScroll');
const dirScan = document.getElementById('dirScan');
const color1Scan = document.getElementById('color1Scan');
const color2Scan = document.getElementById('color2Scan');
const color1Estrellas = document.getElementById('color1Estrellas');
const color2Estrellas = document.getElementById('color2Estrellas');
const velScroll = document.getElementById('velocidadScroll');
const velScan = document.getElementById('velocidadScan');
const velEstrellas = document.getElementById('velocidadEstrellas');
const velColorCambioConstante = document.getElementById('velocidadColorCambioConstante');
const botonColor = document.getElementById('tab-color');
const botonScroll = document.getElementById('tab-scroll');
const botonScan = document.getElementById('tab-scan');
const botonEstrellas = document.getElementById('tab-estrellas');
const checkBoxConstanteColor = document.getElementById('cambioConstanteColor');
const labelVelocidadColorCambioConstante = document.getElementById('labelVelocidadColorCambioConstante');
const inputColor = document.getElementById('color');
const inputColorPersonalizado = document.getElementById('colorPersonalizado');

// Estado
let colorCambioConstante;
let numeroColorCambioConstante = 0;
let scroll;
let numeroScroll = 0;
let scan;
let numeroScan = 0;
let estrellas;
let matriz = [];
let circles = [];

let coloresScroll = [
    "#FF0000", "#FF8000", "#FFFF00", "#80FF00", "#00FF00", "#00FF80",
    "#00FFFF", "#0080FF", "#0000FF", "#8000FF", "#FF00FF", "#FF0080",
    "#FF0000", "#FF8000", "#FFFF00", "#80FF00", "#00FF00", "#00FF80",
    "#00FFFF", "#0080FF", "#0000FF", "#8000FF", "#FF00FF", "#FF0080"
];

let colores = [
    "#FF0000", "#FF8000", "#FFFF00", "#80FF00", "#00FF00", "#00FF80",
    "#00FFFF", "#0080FF", "#0000FF", "#8000FF", "#FF00FF", "#FF0080",
    "#FFFFFF", "#000000"
];

// Inicializar matriz y display

const canvasWidth = $display.clientWidth;
const cellSize = canvasWidth / 10;
const spacing = canvasWidth / 6;
const offset = (canvasWidth - (5 * spacing - (spacing - cellSize))) / 2;

for (let i = 0; i < 5; i++) matriz[i] = new Array(5);
for (let x = 0; x < 5; x++) {
    for (let y = 0; y < 5; y++) {
        let col = x * spacing + offset;
        let row = y * spacing + offset;

        matriz[x][y] = new Path2D();
        matriz[x][y].rect(col, row, cellSize, cellSize);

        contextoDisplay.fillStyle = inputColor.value;
        contextoDisplay.fill(matriz[x][y]);
    }
}

// Inicializar rueda de colores
for (let i = 0; i < 14; i++) {
    let anguloInicio = -(Math.PI / 180) * (i * 30);
    let anguloFin = -(Math.PI / 180) * (i + 1) * 30;

    circles[i] = new Path2D();

    if (i < 12) {
        circles[i].moveTo(centerCircleX, centerCircleY);
        circles[i].arc(centerCircleX, centerCircleY, 100, anguloInicio, anguloFin, true);
    } else if (i === 12) {
        circles[i].moveTo(centerCircleX, centerCircleY);
        circles[i].arc(centerCircleX, centerCircleY, 40, 0, Math.PI * 2, true);
    } else {
        circles[i].moveTo(centerCircleX, centerCircleY);
        circles[i].arc(centerCircleX, centerCircleY, 20, 0, Math.PI * 2, true);
    }

    ctx.fillStyle = colores[i];
    ctx.fill(circles[i]);
}

// Selección en rueda
canvas.addEventListener('click', function (event) {
    limpiarDisplay();
    for (let i = 0; i < 14; i++) {
        if (ctx.isPointInPath(circles[i], event.offsetX, event.offsetY)) {
            const nuevoColor = colores[i];
            inputColor.value = nuevoColor;
            if (inputColorPersonalizado) inputColorPersonalizado.value = nuevoColor;
            contextoDisplay.fillStyle = nuevoColor;
            for (const fila of matriz) {
                for (const cuadrado of fila) contextoDisplay.fill(cuadrado);
            }
        }
    }
});

// Cambio manual en input color personalizado
inputColorPersonalizado?.addEventListener('input', function (event) {
    const nuevoColor = event.target.value;
    inputColor.value = nuevoColor;
    limpiarDisplay();
    contextoDisplay.fillStyle = nuevoColor;
    for (const fila of matriz) {
        for (const cuadrado of fila) contextoDisplay.fill(cuadrado);
    }
});

// BOTON Color (SOLO Limpia display)
botonColor.addEventListener('click', function (event) {
    let numeroActual = velColorCambioConstante.value;

    if (checkBoxConstanteColor.checked) {
        labelVelocidadColorCambioConstante.classList.remove('hidden')
        limpiarDisplay();
        colorCambioConstante = setInterval(function () {

            if (numeroActual !== velColorCambioConstante.value) {
                botonColor.click();
            }

            if (numeroColorCambioConstante === 12) {
                numeroColorCambioConstante = 0;
            }

            for (let f = 0; f < matriz[0].length; f++) {
                for (let c = 0; c < matriz[0].length; c++) {
                    contextoDisplay.fillStyle = colores[numeroColorCambioConstante];
                    contextoDisplay.fill(matriz[f][c]);
                }
            }
            numeroColorCambioConstante++;

        }, 1000 / velColorCambioConstante.value);
    } else {
        labelVelocidadColorCambioConstante.classList.add('hidden')
        limpiarDisplay();
        inputColorPersonalizado.value = '#000000';
        inputColor.value = '#000000';
    }
})

checkBoxConstanteColor.addEventListener('change', function (event) {

    botonColor.click();
    if (checkBoxConstanteColor.checked) {
        canvas.style.pointerEvents = 'none';
        canvas.style.opacity = '0.5';  // opcional: visualmente muestra que está deshabilitado
        inputColorPersonalizado.disabled = checkBoxConstanteColor.checked;
    } else {
        canvas.style.pointerEvents = 'auto';
        canvas.style.opacity = '1';
    }
});

// BOTON SCROLL (SOLO EFECTO VISUAL)
botonScroll.addEventListener('click', function (event) {
    let numeroActual = velScroll.value;

    limpiarDisplay();

    scroll = setInterval(function () {

        if (numeroActual !== velScroll.value) {
            botonScroll.click();
        }
        if (numeroScroll === 12) {
            numeroScroll = 0;
        }
        switch (dirScroll.value) {
            case "Izquierda":
                for (let f = 0; f < matriz[0].length; f++) {
                    contextoDisplay.fillStyle = coloresScroll[f + numeroScroll];
                    for (let c = 0; c < matriz[0].length; c++) {
                        contextoDisplay.fill(matriz[f][c]);
                    }
                }
                break;
            case 'Derecha':
                for (let f = 0; f < matriz[0].length; f++) {
                    contextoDisplay.fillStyle = coloresScroll[f + numeroScroll];
                    for (let c = 0; c < matriz[0].length; c++) {
                        let fila = matriz[0].length - 1 - f
                        contextoDisplay.fill(matriz[fila][c]);
                    }
                }
                break;
            case 'Abajo':
                for (let f = 0; f < matriz[0].length; f++) {
                    contextoDisplay.fillStyle = coloresScroll[f + numeroScroll];
                    for (let c = 0; c < matriz[0].length; c++) {
                        let fila = matriz[0].length - 1 - f
                        contextoDisplay.fill(matriz[c][fila]);
                    }
                }
                break;
            case 'Arriba':
                for (let f = 0; f < matriz[0].length; f++) {
                    contextoDisplay.fillStyle = coloresScroll[f + numeroScroll];
                    for (let c = 0; c < matriz[0].length; c++) {
                        contextoDisplay.fill(matriz[c][f]);
                    }
                }
                break;
        }
        numeroScroll++;
    }, 1000 / velScroll.value);
});

// BOTON SCAN (SOLO EFECTO VISUAL)

botonScan.addEventListener('click', function (event) {

    let numeroActual = velScan.value;
    limpiarDisplay();

    scan = setInterval(function () {
        if (numeroActual !== velScan.value) {
            botonScan.click();
        }
        if (numeroScan === 5) {
            numeroScan = 0;
        }
        switch (dirScan.value) {
            case 'Derecha':
                for (let f = 0; f < matriz[0].length; f++) {
                    for (let c = 0; c < matriz[0].length; c++) {
                        contextoDisplay.fillStyle = color2Scan.value;
                        contextoDisplay.fill(matriz[f][c]);
                        contextoDisplay.fillStyle = color1Scan.value;
                        contextoDisplay.fill(matriz[numeroScan][c]);
                    }
                }
                break;
            case 'Izquierda':
                for (let f = 0; f < matriz[0].length; f++) {
                    for (let c = 0; c < matriz[0].length; c++) {
                        contextoDisplay.fillStyle = color2Scan.value;
                        contextoDisplay.fill(matriz[f][c]);
                        contextoDisplay.fillStyle = color1Scan.value;
                        let fila = matriz[0].length - 1 - numeroScan
                        contextoDisplay.fill(matriz[fila][c]);
                    }
                }
                break;
            case 'Arriba':
                for (let f = 0; f < matriz[0].length; f++) {
                    for (let c = 0; c < matriz[0].length; c++) {
                        contextoDisplay.fillStyle = color2Scan.value;
                        contextoDisplay.fill(matriz[f][c]);
                        contextoDisplay.fillStyle = color1Scan.value;
                        let col = matriz[0].length - 1 - numeroScan
                        contextoDisplay.fill(matriz[f][col]);
                    }
                }
                break;
            case 'Abajo':
                for (let f = 0; f < matriz[0].length; f++) {
                    for (let c = 0; c < matriz[0].length; c++) {
                        contextoDisplay.fillStyle = color2Scan.value;
                        contextoDisplay.fill(matriz[f][c]);
                        contextoDisplay.fillStyle = color1Scan.value;
                        contextoDisplay.fill(matriz[f][numeroScan]);
                    }
                }
                break;
        }

        numeroScan++;
    }, 1000 / velScan.value);
});

// BOTON ESTRELLAS (SOLO EFECTO VISUAL)

botonEstrellas.addEventListener('click', function (event) {

    let numeroActual = velEstrellas.value;
    limpiarDisplay();

    estrellas = setInterval(function () {

        if (numeroActual !== velEstrellas.value) {
            botonEstrellas.click();
        }

        for (let f = 0; f < matriz[0].length; f++) {
            for (let c = 0; c < matriz[0].length; c++) {

                contextoDisplay.fillStyle = color2Estrellas.value;
                contextoDisplay.fill(matriz[f][c]);
                contextoDisplay.fillStyle = color1Estrellas.value;
                contextoDisplay.fill(matriz[getRandomInt(0, 5)][getRandomInt(0, 5)]);
            }
        }
    }, 1000 / velEstrellas.value);
});

let active = document.getElementById('active').value;

if (active === 'color') {
    botonColor.click();
}

if (active === 'scroll') {
    botonScroll.click();
}

if (active === 'scan') {
    botonScan.click();
}

if (active === 'estrellas') {
    botonEstrellas.click();
}

// Script simple para controlar tabs sin Bootstrap
document.addEventListener('DOMContentLoaded', function () {
    const tabs = document.querySelectorAll('[data-tab-target]');
    const panels = document.querySelectorAll('section[role="tabpanel"]');

    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            tabs.forEach(t => {
                t.classList.remove('bg-cyan-500', 'text-white');
                t.classList.add('bg-[#2c2c2c]', 'text-cyan-300');
                t.setAttribute('aria-selected', 'false');
            });
            tab.classList.add('bg-cyan-500', 'text-white');
            tab.classList.remove('bg-[#2c2c2c]', 'text-cyan-300');
            tab.setAttribute('aria-selected', 'true');

            const target = document.querySelector(tab.dataset.tabTarget);
            panels.forEach(panel => panel.classList.add('hidden'));
            target.classList.remove('hidden');
        });
    });
});


document.addEventListener('DOMContentLoaded', function () {

    const botones = document.querySelectorAll('.btn-enviar');
    const mensajes = document.querySelectorAll('.div-error');
    const inputsShowroom = document.querySelectorAll(".select-showroom");

    const estadoBadge = document.getElementById('estado-badge');
    const estadoBadgeMobile = document.getElementById('estado-badge-mobile');

    for (let i = 0; i < botones.length; i++) {
        const btn = botones[i];
        const mensajeError = mensajes[i];

        btn?.addEventListener('click', function (e) {
            const textoEstado = [
                estadoBadge?.textContent || '',
                estadoBadgeMobile?.textContent || ''
            ].join(' ');

            if (textoEstado.includes("Desconectada")) {
                e.preventDefault();
                mostrarError("No hay conexión con la PC. Conéctela para enviar comandos.", mensajeError);
                return;
            }

            if (textoEstado.includes("Cargando")) {
                e.preventDefault();
                mostrarError("Esperando conexión con la PC...", mensajeError);
            }
        });
    }

    function mostrarError(mensaje, mensajeError) {
        mensajeError.textContent = mensaje;
        mensajeError.classList.remove('hidden');
        setTimeout(() => {
            mensajeError.classList.add('hidden');
        }, 5000);
    }

    if (checkBoxConstanteColor.checked) {
        canvas.style.pointerEvents = 'none';
        canvas.style.opacity = '0.5';
        inputColorPersonalizado.disabled = true;
        labelVelocidadColorCambioConstante.classList.remove('hidden');
    } else {
        canvas.style.pointerEvents = 'auto';
        canvas.style.opacity = '1';
        inputColorPersonalizado.disabled = false;
        labelVelocidadColorCambioConstante.classList.add('hidden');
    }


    inputsShowroom.forEach((inputShowroom, i) => {
        const btnRelacionado = botones[i];

        function actualizarBoton() {
            const valorSeleccionado = parseInt(inputShowroom.value);
            if (valorSeleccionado === 0) {
                btnRelacionado.disabled = true;
                btnRelacionado.style.opacity = "0.5";
                btnRelacionado.style.pointerEvents = "none";
                btnRelacionado.style.backgroundColor = "#6b7280"; // Tailwind bg-gray-500
                btnRelacionado.style.cursor = "not-allowed";
            } else {
                btnRelacionado.disabled = false;
                btnRelacionado.style.opacity = "1";
                btnRelacionado.style.pointerEvents = "auto";
                btnRelacionado.style.backgroundColor = "#06b6d4"; // Tailwind bg-cyan-500
                btnRelacionado.style.cursor = "pointer";
            }
        }

        actualizarBoton();
        inputShowroom.addEventListener('change', actualizarBoton);
        btnRelacionado.closest('form').addEventListener('submit', (e) => {
            if (btnRelacionado.disabled) {
                e.preventDefault();
            }
        });
    });

});