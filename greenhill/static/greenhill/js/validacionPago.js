$(document).ready(function () {
    $("#formPago").validate({
        debug: true,
        rules: {
            nombre: {
                required: true,
            },
            direccion: {
                required: true
            },
            tarjeta: {
                required: true,
                number: true,
                min: 0
            },
            vencimiento: {
                required: true
            },
            cvv: {
                required: true,
                number: true,
                min: 0,
                max: 999
            }
        }
    })
});