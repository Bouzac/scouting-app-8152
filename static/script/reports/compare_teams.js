document.addEventListener("DOMContentLoaded", function () {
    const rawTeam1Data = document.getElementById("chart-team1-data").textContent;
    const rawTeam2Data = document.getElementById("chart-team2-data").textContent;
    const parsedTeam1Data = JSON.parse(rawTeam1Data);
    const parsedTeam2Data = JSON.parse(rawTeam2Data);

    const ctx = document.getElementById('teamChart').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: parsedData.labels,
            datasets: [
            {
                label: 'Points Moyens',
                data: parsedTeam1Data.data,
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
                label: 'Points moyens',
                data: parsedTeam2Data.data,
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
                    text: 'Performance Moyenne'
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
