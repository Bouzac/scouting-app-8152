$(document).ready(function() {
    var table = $('#reportTable').DataTable({
        orderCellsTop: true,
        fixedHeader: true
    });

    $.fn.dataTable.ext.search.push(
        function(settings, data, dataIndex) {
            var valid = true;

            // Pour chaque colonne numérique filtrée
            $('.num-value').each(function() {
                var colIndex = $(this).data('col-index');
                var operator = $('.num-operator[data-col-index="'+colIndex+'"]').val();
                var filterVal = $(this).val();

                if(filterVal) {
                    var cellVal = parseFloat(data[colIndex]) || 0;
                    var filterNum = parseFloat(filterVal);

                    switch(operator) {
                        case '=': valid = valid && (cellVal === filterNum); break;
                        case '>': valid = valid && (cellVal > filterNum); break;
                        case '<': valid = valid && (cellVal < filterNum); break;
                        case '>=': valid = valid && (cellVal >= filterNum); break;
                        case '<=': valid = valid && (cellVal <= filterNum); break;
                    }
                }
            });

            // Recherche texte simple sur autres colonnes
            $('.column-filter').each(function() {
                var colIndex = $(this).data('col-index');
                var val = $(this).val().toLowerCase();
                if(val) {
                    var cellText = data[colIndex].toString().toLowerCase();
                    if(!cellText.includes(val)) {
                        valid = false;
                    }
                }
            });

            return valid;
        }
    );

    // Déclencher redraw au changement sur inputs/selects
    $('input, select').on('keyup change', function() {
        table.draw();
    });
});
