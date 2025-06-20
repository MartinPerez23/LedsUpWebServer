$(document).ready(function () {
    function generarColorHex() {
        let letras = '0123456789ABCDEF';
        let color = '#';
        for (let i = 0; i < 6; i++) {
            color += letras[Math.floor(Math.random() * 16)];
        }
        return color;
    }

    setInterval(function () {
        const colorRandom = generarColorHex();
        // Aplicar el gradiente radial con el color random y transparencia al final
        const gradiente = `radial-gradient(closest-side, ${colorRandom}, transparent)`;

        $("#imagenLogo").css({
            "background": gradiente,
            "-webkit-background": gradiente
        });
    }, 1500);
});

$(document).ready(function(){
    $('.venobox').venobox();
});

