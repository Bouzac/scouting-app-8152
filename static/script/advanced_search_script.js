document.getElementById("advanced_searchType").addEventListener("change", function() {
    const searchType = this.value;
    const comparator = document.getElementById("comparator");
    const search_types = {};
    for (const s of document.querySelectorAll("input[type='hidden']")) {
        s.style.display = "none";
        search_types[s.id] = s.value;
    }
    

    if(search_types[searchType] === 'number') {
        comparator.style.display = "block";
    } else {
        comparator.style.display = "none";
    }
});

document.addEventListener("DOMContentLoaded", function () {
    const rows = document.querySelectorAll('.result-row');
    const panel = document.getElementById('details-panel');
    const content = document.getElementById('details-content');

    rows.forEach(row => {
        row.addEventListener('click', function () {
            unParsedId = this.id;
            parsedId = unParsedId.split("-")[1];
            alert(parsedId);
            
            fetch(`/get_scouting_details/${parsedId}`)
                .then(response => {
                    if (!response.ok) throw new Error("Erreur AJAX");
                    return response.json();
                })
                .then(data => {
                    content.innerHTML = `
                        <p><strong>Match:</strong> ${data.match_id}</p>
                        <p><strong>Team:</strong> ${data.team_id}</p>
                        <p><strong>Scout:</strong> ${data.scout_id}</p>
                        <p><strong>Auto:</strong> ${data.auto_points}</p>
                        <p><strong>Teleop:</strong> ${data.teleop_points}</p>
                        <p><strong>Endgame:</strong> ${data.endgame_points}</p>
                        <p><strong>Penalties:</strong> ${data.penalties}</p>
                        <p><strong>Status:</strong> ${data.robot_status}</p>
                        <p><strong>Notes:</strong> ${data.notes}</p>
                        <p><strong>Timestamp:</strong> ${data.timestamp}</p>
                    `;
                    panel.style.display = "block";
                })
                .catch(err => {
                    content.innerHTML = "Erreur lors du chargement.";
                    console.error(err);
                });
        });
    });
});