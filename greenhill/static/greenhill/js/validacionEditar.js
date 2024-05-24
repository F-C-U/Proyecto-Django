$(document).ready(function () {
    $.validator.addMethod("notZero", function (value, element) {
        return value != "0";
    }, "Este campo es obligatorio.");
    $("#formEditar").validate({
        debug: false,
        rules: {
            nombreproducto: {
                required: true
            },
            precio: {
                required: true,
                number: true,
                min: 1
            },
            consola: {
                required: true,
                notZero: true
            }
        },
    })
});