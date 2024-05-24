$(document).ready(function () {
    $.validator.addMethod("notZero", function (value, element) {
        return value != "0";
    }, "Este campo es obligatorio.");
    $("#formPerfil").validate({
        debug: false,
        rules: {
            email: {
                required: true,
                email: true
            },
            telefono: {
                required: true,
                digits: true,
                minlength: 9,
                maxlength: 9
            },
            region: {
                required: true,
                notZero: true
            },
            comuna: {
                required: true,
                notZero: true
            },
            direccion: {
                required: true
            }
        },
        messages: {
            region: {
                notZero: "Por favor seleccione su region."
            },
            comuna: {
                notZero: "Por favor seleccione su comuna."
            },
        }
    })
    $("#formCambioPass").validate({
        debug: false,
        rules: {
            passA: {
                required: true
            },
            pass1: {
                required: true,
                minlength: 8,
                maxlength: 16
            },
            pass2: {
                required: true,
                equalTo: "#pass1"
            }
        },
    })
});
