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

const canvas = document.getElementById('circulo');
const ctx = canvas.getContext('2d');

const $display = document.querySelector("#display");
const contextoDisplay = $display.getContext("2d");

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

const botonColor = document.getElementById('nav-color-tab');
const botonScroll = document.getElementById('nav-scroll-tab');
const botonScan = document.getElementById('nav-scan-tab');
const botonEstrellas = document.getElementById('nav-estrellas-tab');

const checkBoxConstanteColor = document.getElementById('cambioConstanteColor');

const labelVelocidadColorCambioConstante = document.getElementById('labelVelocidadColorCambioConstante');

let colorCambioConstante;
let numeroColorCambioConstante = 0;

let scroll;
let numeroScroll = 0;

let scan;
let numeroScan = 0;

let estrellas;

let colorete = document.getElementById('color').value;
let matriz = [];
let circles = [];

let coloresScroll = [
    "#FF0000",
    "#FF8000",
    "#FFFF00",
    "#80FF00",
    "#00FF00",
    "#00FF80",
    "#00FFFF",
    "#0080FF",
    "#0000FF",
    "#8000FF",
    "#FF00FF",
    "#FF0080",
    "#FF0000",
    "#FF8000",
    "#FFFF00",
    "#80FF00",
    "#00FF00",
    "#00FF80",
    "#00FFFF",
    "#0080FF",
    "#0000FF",
    "#8000FF",
    "#FF00FF",
    "#FF0080",
];

let colores = [
    "#FF0000",
    "#FF8000",
    "#FFFF00",
    "#80FF00",
    "#00FF00",
    "#00FF80",
    "#00FFFF",
    "#0080FF",
    "#0000FF",
    "#8000FF",
    "#FF00FF",
    "#FF0080",
    "#FFFFFF",
    "#000000",
];

//creo MATRIZ
for(let i=0; i < 5; i++) {
    matriz[i] = new Array(5);
}
//lleno MATRIZ CON PATH2D
for(let x = 0; x < 5; x++) {
    for(let y = 0; y < 5; y++) {

        let col = x * 70 + 10,
            row = y * 70 + 10;

        matriz[x][y] = new Path2D();

        matriz[x][y].moveTo(col, row);
        matriz[x][y].rect(col,row,50,50)


        console.log(colorete)
        contextoDisplay.fillStyle = colorete
        contextoDisplay.fill(matriz[x][y]);
    }
}

for (let i =0;i < 14;i++) {
    let anguloInicio = -(Math.PI / 180) * (i * 30);
    let anguloFin = -(Math.PI / 180) * (i + 1) * 30;

    if (i < 12){

        circles[i] = new Path2D();
        circles[i].moveTo(120, 120);
        circles[i].arc(120, 120, 100, anguloInicio, anguloFin, true);

    }else if(i === 12){

        circles[i] = new Path2D();
        circles[i].moveTo(120, 120);
        circles[i].arc(120, 120, 40, 0, Math.PI * 2, true);

    }else{

        circles[i] = new Path2D();
        circles[i].moveTo(120, 120);
        circles[i].arc(120, 120, 20, 0, Math.PI * 2, true);

    }

    ctx.fillStyle = colores[i];
    ctx.fill(circles[i]);

}

// CLICKS DENTRO DEL CIRCULO DE COLORES
canvas.addEventListener('click', function(event) {
  // Check whether point is inside circle

    limpiarDisplay();

    for (let i=0;i<14;i++){
        if (ctx.isPointInPath(circles[i], event.offsetX, event.offsetY)) {
            contextoDisplay.fillStyle = colores[i];
            document.getElementById('color').value = colores[i];

            for (const fila of matriz) {
                for (const columna of fila) {
                    contextoDisplay.fill(columna);
                }
            }


        }
    }
});

// BOTON Color (SOLO Limpia display)
botonColor.addEventListener('click', function(event) {
    limpiarDisplay();

    let numeroActual = velColorCambioConstante.value;

    if(checkBoxConstanteColor.checked){
        labelVelocidadColorCambioConstante.classList.remove('visually-hidden')
        colorCambioConstante = setInterval(function () {

            if (numeroActual !== velColorCambioConstante.value){
            botonColor.click();
            }

            if (numeroColorCambioConstante === 12){
            numeroColorCambioConstante=0;
            }

            for (let f = 0; f < matriz[0].length; f++) {
                for (let c = 0; c < matriz[0].length; c++) {
                    contextoDisplay.fillStyle = colores[numeroColorCambioConstante];
                    contextoDisplay.fill(matriz[f][c]);
                }
            }
            numeroColorCambioConstante++;

        },1000 / velColorCambioConstante.value);
    }else{
        labelVelocidadColorCambioConstante.classList.add('visually-hidden')
        limpiarDisplay();
    }
});

checkBoxConstanteColor.addEventListener('change',function (event){

        botonColor.click();

});

// BOTON SCROLL (SOLO EFECTO VISUAL)
botonScroll.addEventListener('click', function(event) {
    let numeroActual = velScroll.value;

    limpiarDisplay();

    scroll = setInterval(function () {

        if (numeroActual !== velScroll.value){
            botonScroll.click();
        }
        if (numeroScroll === 12){
            numeroScroll=0;
        }
        switch (dirScroll.value) {
        case "Izquierda":
            for (let f = 0; f < matriz[0].length; f++) {
                contextoDisplay.fillStyle = coloresScroll[f+numeroScroll];
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
                contextoDisplay.fillStyle = coloresScroll[f+numeroScroll];
                for (let c = 0; c < matriz[0].length; c++) {
                    let fila = matriz[0].length -1 - f
                    contextoDisplay.fill(matriz[c][fila]);
                }
            }
            break;
        case 'Arriba':
            for (let f = 0; f < matriz[0].length; f++) {
                contextoDisplay.fillStyle = coloresScroll[f+numeroScroll];
                for (let c = 0; c < matriz[0].length; c++) {
                    contextoDisplay.fill(matriz[c][f]);
                }
            }
            break;
        }
        numeroScroll++;
    },1000 / velScroll.value);
});

// BOTON SCAN (SOLO EFECTO VISUAL)

botonScan.addEventListener('click', function(event) {

    let numeroActual = velScan.value;
    limpiarDisplay();

    scan = setInterval(function () {
        if (numeroActual !== velScan.value){
            botonScan.click();
        }
        if (numeroScan === 5){
            numeroScan=0;
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
    },1000 / velScan.value);
});

// BOTON ESTRELLAS (SOLO EFECTO VISUAL)

botonEstrellas.addEventListener('click', function(event) {

    let numeroActual = velEstrellas.value;
    limpiarDisplay();

    estrellas = setInterval(function () {

        if (numeroActual !== velEstrellas.value){
            botonEstrellas.click();
        }

        for (let f = 0; f < matriz[0].length; f++) {
            for (let c = 0; c < matriz[0].length; c++) {

                contextoDisplay.fillStyle = color2Estrellas.value;
                contextoDisplay.fill(matriz[f][c]);
                contextoDisplay.fillStyle = color1Estrellas.value;
                contextoDisplay.fill(matriz[getRandomInt(0,5)][getRandomInt(0,5)]);
            }
        }
    },1000 / velEstrellas.value);
});

let active = document.getElementById('active').value;

if (active === 'color'){
    botonColor.click();
}

if (active === 'scroll'){
    botonScroll.click();
}

if (active === 'scan'){
    botonScan.click();
}

if (active === 'estrellas'){
    botonEstrellas.click();
}
