$(document).ready(function () {
    $.validator.addMethod("notZero", function (value, element) {
        return value != "0";
    }, "Este campo es obligatorio.");
    $.validator.addMethod("validaRUT", function (value, element) {
        var rut = value.replace(/\./g, '').split('-');
        var num = rut[0];
        var checkDigit = rut[1];
        var s = 0;
        var m = 2;
        for (var i = num.length - 1; i >= 0; i--) {
            s += num[i] * m;
            if (m == 7) {
                m = 2;
            } else {
                m++;
            }
        }
        var res = s % 11;
        var d = 11 - res;
        if (d == 11) {
            d = 0;
        } else if (d == 10) {
            d = 'K';
        }
        return d == checkDigit.toUpperCase();
    }, "RUT inválido.");
    $.validator.addMethod("soloLetras", function (value, element) {
        return this.optional(element) || /^[a-záéíóúñüàè\s]+$/i.test(value);
    }, "Este campo solo acepta letras.");
    $("#formRegistro").validate({
        debug: false,
        rules: {
            rut: {
                required: true,
                validaRUT: true
            },
            nombre: {
                required: true,
                soloLetras: true
            },
            apellido: {
                required: true,
                soloLetras: true
            },
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
        messages: {
            region: {
                notZero: "Por favor seleccione su region."
            },
            comuna: {
                notZero: "Por favor seleccione su comuna."
            },
        }
    })
});
