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

document.addEventListener("DOMContentLoaded", function () {
    const rawData = document.getElementById("chart-data").textContent;
    const parsedData = JSON.parse(rawData);
    
    const rawEventData = document.getElementById("chart-event-data").textContent;
    const parsedEventData = JSON.parse(rawEventData);

    const ctx = document.getElementById('teamChart').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: parsedData.labels,
            datasets: [
            {
                label: 'Points Moyens',
                data: parsedData.data,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.5)',
                    'rgba(54, 162, 235, 0.5)',
                    'rgba(255, 206, 86, 0.5)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)'
                ],
                borderWidth: 1
            },
            {
                label: 'Moyenne de l\'événement',
                data: parsedEventData.data,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.5)',
                    'rgba(54, 162, 235, 0.5)',
                    'rgba(255, 206, 86, 0.5)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)'
                ],
                borderWidth: 1
            }
        ]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Performance Moyenne par Phase'
                },
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
});
