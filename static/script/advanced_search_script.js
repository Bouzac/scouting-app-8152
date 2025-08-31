

document.addEventListener("DOMContentLoaded", function () {
    const rows = document.querySelectorAll('.result-row');
    const panel = document.getElementById('details-panel');
    const content = document.getElementById('details-content');
    const wrapper = document.querySelector('.tables-and-details');
    
    rows.forEach(row => {
        row.addEventListener('click', function () {
            const unParsedId = this.id;
            const parsedId = unParsedId.split("-")[1];
            
            rows.forEach(r => {
                if (r !== row) {
                    r.style.backgroundColor = "";
                }
            });
            
            row.style.backgroundColor = "#FFFF00";

            fetch(`/get_scouting_details/${parsedId}`)
                .then(response => {
                    if (!response.ok) throw new Error("Erreur AJAX");
                    return response.json();
                })
                .then(data => {
                    content.innerHTML = `
                        <p><strong>Match:</strong> ${data.match_number}</p>
                        <p><strong>Team:</strong> ${data.team_number}</p>
                        <p><strong>Scout:</strong> ${data.initials}</p>
                        <p><strong>Auto:</strong> ${data.auto_points}</p>
                        <p><strong>Teleop:</strong> ${data.teleop_points}</p>
                        <p><strong>Endgame:</strong> ${data.endgame_points}</p>
                        <p><strong>Penalties:</strong> ${data.penalties}</p>
                        <p><strong>Status:</strong> ${data.robot_status}</p>
                        <p><strong>Notes:</strong> ${data.notes}</p>
                        <p><strong>Timestamp:</strong> ${data.timestamp}</p>
                    `;

                    // Obtenir la position de la ligne et du wrapper
                    const rowRect = row.getBoundingClientRect();
                    const wrapperRect = wrapper.getBoundingClientRect();

                    // Calculer l'offset top relatif au wrapper
                    const offsetTop = rowRect.top - wrapperRect.top + wrapper.scrollTop;

                    // Positionner le panneau et l'afficher
                    panel.style.top = `${offsetTop}px`;
                    panel.style.display = "block";
                })
                .catch(err => {
                    content.innerHTML = "Erreur lors du chargement.";
                    console.error(err);
                });
        });
    });
});

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