$(document).ready(function () {
    $.validator.addMethod("notZero", function (value, element) {
        return value != "0";
    }, "Este campo es obligatorio.");
    $('#formProducto').validate({
        rules: {
            nombreproducto: {
                required: true,
                minlength: 3,
                maxlength: 50
            },
            precio: {
                required: true,
                number: true,
                min: 1
            },
            consola: {
                required: true,
                notZero: true,
            },
        }
    });
    $("#formProducto").submit(function (event) {
        event.preventDefault();
        if ($("#formProducto").valid()) {
            $(".alert").remove();
            $("#formProducto").before("<div class='alert alert-success alert-dismissible fade show'>Producto registrado</div>");
            $(".alert").append("<button type='button' class='btn-close' data-bs-dismiss='alert'></button>");
        } else {
            $(".alert").remove();
            $("#formProducto").before("<div class='alert alert-danger alert-dismissible fade show'>Error al registrar producto</div>");
            $(".alert").append("<button type='button' class='btn-close' data-bs-dismiss='alert'></button>");
        }
    })
});
