$(document).ready(function () {
    var dataJSON;

    $.getJSON("https://gist.githubusercontent.com/juanbrujo/0fd2f4d126b3ce5a95a7dd1f28b3d8dd/raw/b8575eb82dce974fd2647f46819a7568278396bd/comunas-regiones.json", function (data) {
        dataJSON = data;
        var select = $("#region");
        $.each(data.regiones, function (index, obj) {
            select.append($("<option></option>")
                .attr("value", obj.region)
                .text(obj.region));
        });
    });

    $('#region').change(function () {
        var regionSeleccionada = $(this).val();
        var selectComunas = $("#comuna");
        selectComunas.empty();
        if (regionSeleccionada != "0") {
            var comunas = dataJSON.regiones.find(r => r.region === regionSeleccionada).comunas;
            comunas.sort();
            $.each(comunas, function (index, comuna) {
                selectComunas.append($("<option></option>")
                    .attr("value", comuna)
                    .text(comuna));
            });
        }
    });
});