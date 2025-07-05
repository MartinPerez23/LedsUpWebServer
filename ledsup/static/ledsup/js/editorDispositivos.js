//DISPOSITIVO CREATE/UPDATE
const matrizX = document.getElementById('id_matriz_x');
const matrizY = document.getElementById('id_matriz_y');

const divErrores = document.getElementById('id_errores');

const botonEditar = document.getElementById('botonEditar');
const botonGuardar = document.getElementById('botonGuardar');
const botonAceptar = document.getElementById('botonAceptar');

const patch = document.getElementById('id_patch');
const divEditor = document.getElementById('editor');
const selectPacheoRapido = document.getElementById('pacheoRapido');
// Referencias
const popupOverlay = document.getElementById('popupOverlay');
const botonCerrar = document.getElementById('cerrarPopup');
const botonCancelar = document.getElementById('cancelarPopup');

botonEditar.addEventListener('click', () => {
    let contador = 0;
    let matrizDeInputs = '';

    // Intentar cargar valores guardados si existen (de la base o lo que haya guardado antes)
    let valoresGuardados = null;
    if (patch.value) {
        valoresGuardados = patch.value.split(',').map(v => v.trim());
    }

    for (let y = 0; y < matrizY.value; y++) {
        matrizDeInputs += "<div class='row'>";
        for (let x = 0; x < matrizX.value; x++) {
            // Si hay valores guardados, los uso; sino uso el índice por defecto
            let valor = contador;
            if (valoresGuardados && valoresGuardados.length === matrizX.value * matrizY.value) {
                valor = valoresGuardados[contador];
            }
            matrizDeInputs += `<input type='number' class='form-control col w-12 h-12 text-center font-bold rounded-md bg-gray-800 text-white border border-gray-700' id='led${contador}' value='${valor}'>`;
            contador++;
        }
        matrizDeInputs += "</div>";
    }
    divEditor.innerHTML = matrizDeInputs;

    popupOverlay.classList.remove('hidden');
});

// Cerrar popup al hacer click en cerrar o cancelar
botonCerrar.addEventListener('click', () => {
    popupOverlay.classList.add('hidden');
});

botonCancelar.addEventListener('click', () => {
    popupOverlay.classList.add('hidden');
});

// Cerrar popup si clickeas fuera del contenido (overlay)
popupOverlay.addEventListener('click', (event) => {
    // Si el click fue directamente en el overlay (no en el contenido)
    if (event.target === popupOverlay) {
        popupOverlay.classList.add('hidden');
    }
});


function chequeoDeMatriz() {
    if (matrizX.value * matrizY.value <= 170) {
        divErrores.innerHTML = ''
        botonAceptar.removeAttribute('disabled');
    } else {
        divErrores.innerHTML = "<div class='alert alert-danger'>" +
            "<h5 class='text-danger'>¡Error!</h5>" +
            "<p>El numero máximo de LEDs que puede controlar nuestra aplicación es de 170 " +
            "(la multiplicación de MatrizX y MatrizY debe ser menor o igual a 170)</p>" +
            "<p>Valor actual de la multiplicación: " + matrizX.value * matrizY.value + "</p></div>";
        botonAceptar.setAttribute("disabled", true);
    }
}

matrizX.addEventListener('change', chequeoDeMatriz, false);
matrizY.addEventListener('change', chequeoDeMatriz, false);

// Guardar los valores y cerrar popup
botonGuardar.addEventListener('click', () => {
    let contador = 0;
    let posiciones = [];
    for (let y = 0; y < matrizY.value; y++) {
        for (let x = 0; x < matrizX.value; x++) {
            const valor = document.getElementById('led' + contador);
            posiciones.push(valor.value);
            contador++;
        }
    }
    patch.value = posiciones.join(',');
    popupOverlay.classList.add('hidden');
});


selectPacheoRapido.addEventListener('change', function (MouseEvent) {
    let num;
    let matrizDeInputs = '';
    if (selectPacheoRapido.value === '0') {
        for (let y = 0; y < matrizY.value; y++) {
            matrizDeInputs += "<div class='row'>";
            for (let x = 0; x < matrizX.value; x++) {
                num = x + matrizX.value * y
                matrizDeInputs = matrizDeInputs + "<input type='number' class='form-control col w-12 h-12 text-center font-bold rounded-md bg-gray-800 text-white border border-gray-700' id='led" + (x + matrizX.value * y) + "' value='" + num + "'>";
            }
            matrizDeInputs += "</div>";
        }
    } else if (selectPacheoRapido.value === '1') {
        for (let y = 0; y < matrizY.value; y++) {
            matrizDeInputs += "<div class='row'>";
            for (let x = 0; x < matrizX.value; x++) {
                num = matrizX.value * (y + 1) - (x + 1)
                matrizDeInputs = matrizDeInputs + "<input type='number' class='form-control col w-12 h-12 text-center font-bold rounded-md bg-gray-800 text-white border border-gray-700' id='led" + (x + matrizX.value * y) + "' value='" + num + "'>";
            }
            matrizDeInputs += "</div>";
        }
    } else if (selectPacheoRapido.value === '2') {
        for (let y = 0; y < matrizY.value; y++) {
            matrizDeInputs += "<div class='row'>";
            for (let x = 0; x < matrizX.value; x++) {
                num = matrizX.value * matrizY.value - matrizX.value + x - matrizX.value * y
                matrizDeInputs = matrizDeInputs + "<input type='number' class='form-control col w-12 h-12 text-center font-bold rounded-md bg-gray-800 text-white border border-gray-700' id='led" + (x + matrizX.value * y) + "' value='" + num + "'>";
            }
            matrizDeInputs += "</div>";
        }
    } else if (selectPacheoRapido.value === '3') {
        for (let y = 0; y < matrizY.value; y++) {
            matrizDeInputs += "<div class='row'>";
            for (let x = 0; x < matrizX.value; x++) {
                num = matrizX.value * matrizY.value - (x + 1) - matrizX.value * y
                matrizDeInputs = matrizDeInputs + "<input type='number' class='form-control col w-12 h-12 text-center font-bold rounded-md bg-gray-800 text-white border border-gray-700' id='led" + (x + matrizX.value * y) + "' value='" + num + "'>";
            }
            matrizDeInputs += "</div>";
        }
    } else if (selectPacheoRapido.value === '4') {
        for (let y = 0; y < matrizY.value; y++) {
            matrizDeInputs += "<div class='row'>";
            for (let x = 0; x < matrizX.value; x++) {
                if (y % 2 === 0) {
                    num = x + matrizX.value * y
                } else {
                    num = matrizX.value * (y + 1) - (x + 1)
                }

                matrizDeInputs = matrizDeInputs + "<input type='number' class='form-control col w-12 h-12 text-center font-bold rounded-md bg-gray-800 text-white border border-gray-700' id='led" + (x + matrizX.value * y) + "' value='" + num + "'>";
            }
            matrizDeInputs += "</div>";
        }
    } else if (selectPacheoRapido.value === '5') {
        for (let y = 0; y < matrizY.value; y++) {
            matrizDeInputs += "<div class='row'>";
            for (let x = 0; x < matrizX.value; x++) {
                if (y % 2 === 0) {
                    num = matrizX.value * (y + 1) - (x + 1)
                } else {
                    num = x + matrizX.value * y
                }

                matrizDeInputs = matrizDeInputs + "<input type='number' class='form-control col w-12 h-12 text-center font-bold rounded-md bg-gray-800 text-white border border-gray-700' id='led" + (x + matrizX.value * y) + "' value='" + num + "'>";
            }
            matrizDeInputs += "</div>";
        }
    } else if (selectPacheoRapido.value === '6') {
        for (let y = 0; y < matrizY.value; y++) {
            matrizDeInputs += "<div class='row'>";
            for (let x = 0; x < matrizX.value; x++) {
                if (y % 2 === 0) {
                    num = matrizX.value * matrizY.value - (x + 1) - matrizX.value * y
                } else {
                    num = matrizX.value * matrizY.value - matrizX.value + x - matrizX.value * y
                }

                matrizDeInputs = matrizDeInputs + "<input type='number' class='form-control col w-12 h-12 text-center font-bold rounded-md bg-gray-800 text-white border border-gray-700' id='led" + (x + matrizX.value * y) + "' value='" + num + "'>";
            }
            matrizDeInputs += "</div>";
        }
    } else if (selectPacheoRapido.value === '7') {
        for (let y = 0; y < matrizY.value; y++) {
            matrizDeInputs += "<div class='row'>";
            for (let x = 0; x < matrizX.value; x++) {
                if (y % 2 === 0) {
                    num = matrizX.value * matrizY.value - matrizX.value + x - matrizX.value * y
                } else {
                    num = matrizX.value * matrizY.value - (x + 1) - matrizX.value * y
                }

                matrizDeInputs = matrizDeInputs + "<input type='number' class='form-control col w-12 h-12 text-center font-bold rounded-md bg-gray-800 text-white border border-gray-700' id='led" + (x + matrizX.value * y) + "' value='" + num + "'>";
            }
            matrizDeInputs += "</div>";
        }
    } else if (selectPacheoRapido.value === '8') {
        for (let y = 0; y < matrizY.value; y++) {
            matrizDeInputs += "<div class='row'>";
            for (let x = 0; x < matrizX.value; x++) {
                num = matrizY.value * x + y
                matrizDeInputs = matrizDeInputs + "<input type='number' class='form-control col w-12 h-12 text-center font-bold rounded-md bg-gray-800 text-white border border-gray-700' id='led" + (x + matrizX.value * y) + "' value='" + num + "'>";
            }
            matrizDeInputs += "</div>";
        }
    } else if (selectPacheoRapido.value === '9') {
        for (let y = 0; y < matrizY.value; y++) {
            matrizDeInputs += "<div class='row'>";
            for (let x = 0; x < matrizX.value; x++) {
                num = matrizX.value * matrizY.value - matrizY.value + y - matrizY.value * x
                matrizDeInputs = matrizDeInputs + "<input type='number' class='form-control col w-12 h-12 text-center font-bold rounded-md bg-gray-800 text-white border border-gray-700' id='led" + (x + matrizX.value * y) + "' value='" + num + "'>";
            }
            matrizDeInputs += "</div>";
        }
    } else if (selectPacheoRapido.value === '10') {
        for (let y = 0; y < matrizY.value; y++) {
            matrizDeInputs += "<div class='row'>";
            for (let x = 0; x < matrizX.value; x++) {
                num = matrizY.value * (x + 1) - (y + 1)
                matrizDeInputs = matrizDeInputs + "<input type='number' class='form-control col w-12 h-12 text-center font-bold rounded-md bg-gray-800 text-white border border-gray-700' id='led" + (x + matrizX.value * y) + "' value='" + num + "'>";
            }
            matrizDeInputs += "</div>";
        }
    } else if (selectPacheoRapido.value === '11') {
        for (let y = 0; y < matrizY.value; y++) {
            matrizDeInputs += "<div class='row'>";
            for (let x = 0; x < matrizX.value; x++) {
                num = matrizY.value * matrizX.value - (y + 1) - matrizY.value * x
                matrizDeInputs = matrizDeInputs + "<input type='number' class='form-control col w-12 h-12 text-center font-bold rounded-md bg-gray-800 text-white border border-gray-700' id='led" + (x + matrizX.value * y) + "' value='" + num + "'>";
            }
            matrizDeInputs += "</div>";
        }
    } else if (selectPacheoRapido.value === '12') {
        for (let y = 0; y < matrizY.value; y++) {
            matrizDeInputs += "<div class='row'>";
            for (let x = 0; x < matrizX.value; x++) {
                if (x % 2 === 0) {
                    num = y + matrizY.value * x
                } else {
                    num = matrizY.value * (x + 1) - (y + 1)
                }

                matrizDeInputs = matrizDeInputs + "<input type='number' class='form-control col w-12 h-12 text-center font-bold rounded-md bg-gray-800 text-white border border-gray-700' id='led" + (x + matrizX.value * y) + "' value='" + num + "'>";
            }
            matrizDeInputs += "</div>";
        }
    } else if (selectPacheoRapido.value === '14') {
        for (let y = 0; y < matrizY.value; y++) {
            matrizDeInputs += "<div class='row'>";
            for (let x = 0; x < matrizX.value; x++) {
                if (x % 2 === 0) {
                    num = matrizY.value * (x + 1) - (y + 1)
                } else {
                    num = y + matrizY.value * x
                }

                matrizDeInputs = matrizDeInputs + "<input type='number' class='form-control col w-12 h-12 text-center font-bold rounded-md bg-gray-800 text-white border border-gray-700' id='led" + (x + matrizX.value * y) + "' value='" + num + "'>";
            }
            matrizDeInputs += "</div>";
        }
    } else if (selectPacheoRapido.value === '15') {
        for (let y = 0; y < matrizY.value; y++) {
            matrizDeInputs += "<div class='row'>";
            for (let x = 0; x < matrizX.value; x++) {
                if (x % 2 === 0) {
                    num = matrizX.value * matrizY.value - (y + 1) - matrizY.value * x
                } else {
                    num = matrizX.value * matrizY.value - matrizY.value + y - matrizY.value * x
                }

                matrizDeInputs = matrizDeInputs + "<input type='number' class='form-control col w-12 h-12 text-center font-bold rounded-md bg-gray-800 text-white border border-gray-700' id='led" + (x + matrizX.value * y) + "' value='" + num + "'>";
            }
            matrizDeInputs += "</div>";
        }
    } else if (selectPacheoRapido.value === '13') {
        for (let y = 0; y < matrizY.value; y++) {
            matrizDeInputs += "<div class='row'>";
            for (let x = 0; x < matrizX.value; x++) {
                if (x % 2 === 0) {
                    num = matrizX.value * matrizY.value - matrizY.value + y - matrizY.value * x
                } else {
                    num = matrizY.value * matrizX.value - (y + 1) - matrizY.value * x
                }

                matrizDeInputs = matrizDeInputs + "<input type='number' class='form-control col w-12 h-12 text-center font-bold rounded-md bg-gray-800 text-white border border-gray-700' id='led" + (x + matrizX.value * y) + "' value='" + num + "'>";
            }
            matrizDeInputs += "</div>";
        }
    }

    divEditor.innerHTML = matrizDeInputs;
});
