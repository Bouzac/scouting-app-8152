let previousSelectedTeam = null;

function show(shown, hidden) {
  document.getElementById(shown).style.display='block';
  document.getElementById(hidden).style.display='none';
  return false;
}

function matchInput(event) {
    const value = event.target.value;
    const checklistcontainer = document.getElementById('teams_checklist_container');
    const checklist = document.getElementById('teams_checklist');

    if (value.length > 0) {
        console.log("Typed value:", value);
        
        fetch(`/get_match_info/${value}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error("Erreur AJAX");
                }
                console.log("Fetch response ok");
                return response.json();
            })
            .then(data => {
                checklist.innerHTML = '<option value="" disabled selected>Choisir une équipe</option>';
                const all_team_ids = [...data.red, ...data.blue];
                const selected_teams = data.selected;

                all_team_ids.forEach(team_id => {
                    const selection = selected_teams.find(sel => sel.team_number == team_id);               
                    if (selection) {
                        checklist.innerHTML += `<option value="${team_id}" disabled>${team_id} — ${selection.user}</option>`;
                    } else {
                        checklist.innerHTML += `<option value="${team_id}">${team_id}</option>`;
                    }
                });
                checklistcontainer.style.display = "block";
            })
            .catch(err => {
                checklistcontainer.style.display = "none";
                console.error("Fetch error:", err);
                document.getElementById('match_number').value = '';
            });
    } else {
        document.getElementById('match_number').value = '';
        checklistcontainer.style.display = "none";
    }
}

function teamSelected(event) {
    const selectedTeam = event.target.value;
    const match_number = document.getElementById('match_number').value;
    const allianceColorDisplay = document.getElementById('alliance_color_display');
    const allianceColorContainer = document.getElementById('alliance_color_container');
    const user = document.getElementById('scout_name').value;

    if (!selectedTeam || selectedTeam === ""){
        console.log("désélection");
        allianceColorContainer.style.display = "none";
        allianceColorDisplay.value = "";

        fetch('/rem_selected', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({'team_number' : previousSelectedTeam})
        })
        .then(response => response.json())
        .then(data => {
            console.log("Sélection enlevée :", data)
        });
        
        previousSelectedTeam = null;
        return;
    }

    if (previousSelectedTeam && previousSelectedTeam !== selectedTeam){
        console.log('désélection')

        fetch('/rem_selected', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({'team_number' : previousSelectedTeam})
        })
        .then(response => response.json())
        .then(data => {
            console.log("Sélection enlevée :", data)
        });
    }

    previousSelectedTeam = selectedTeam;

    fetch('/select', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({'team_number': selectedTeam, 'user': user})
    })
    .then(response => response.json())
    .then(data => {
        console.log("Sélection enregistrée :", data)
    })

    fetch(`/get_team_color/${selectedTeam}$${match_number}`)
        .then(response => {
            if (!response.ok) {
                throw new Error("Erreur AJAX");
            }
            return response.json();
        })
        .then(data => {
            const teamColor = data.color;
            allianceColorContainer.style.display = 'block'
            console.log(teamColor)
            allianceColorDisplay.value = teamColor
        })
        .catch(err => {
            console.error("Fetch error:", err);
            allianceColorDisplay.textContent = 'Erreur lors de la récupération de la couleur de l\'alliance';
        });
}

function updateTeamsList() {
  const matchNumberInput = document.getElementById('match_number');
  const value = matchNumberInput.value;
  const checklistcontainer = document.getElementById('teams_checklist_container');
  const checklist = document.getElementById('teams_checklist');

  const selectedValue = checklist.value; // Sauvegarde sélection actuelle

  if (value.length > 0) {
    fetch(`/get_match_info/${value}`)
      .then(response => {
        if (!response.ok) throw new Error("Erreur AJAX");
        return response.json();
      })
      .then(data => {
        checklist.innerHTML = '<option value="" disabled>Choisir une équipe</option>';

        const all_team_ids = [...data.red, ...data.blue];
        const selected_teams = data.selected;

        all_team_ids.forEach(team_id => {
          const selection = selected_teams.find(sel => sel.team_number == team_id);
          const option = document.createElement('option');
          option.value = team_id;

          if (selection) {
            option.textContent = `${team_id} — ${selection.user}`;
            option.disabled = true;
          } else {
            option.textContent = `${team_id}`;
          }

          console.log(team_id)
          console.log(selectedValue)

          checklist.value = selectedValue

          console.log(checklist.value)

          checklist.appendChild(option);
        });

        checklistcontainer.style.display = "block";
      })
      .catch(err => {
        checklistcontainer.style.display = "none";
        console.error("Fetch error:", err);
        matchNumberInput.value = '';
      });
  } else {
    checklistcontainer.style.display = "none";
  }
}


window.addEventListener('beforeunload', () => {
    const team = document.getElementById('teams_checklist')?.value;
    const user = document.getElementById('scout_name')?.value;

    if (team && user) {
        const data = JSON.stringify({
            'team_number': team,
            'user': user
        });
        const blob = new Blob([data], { type: 'application/json' });
        navigator.sendBeacon('/deselect', blob);
    }
});