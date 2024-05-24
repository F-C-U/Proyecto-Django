$(document).ready(function () {
    $("#formSesion").validate({
        debug: true,
        rules: {
            email: {
                required: true,
                email: true
            }
        },
    });
});