document.getElementById("searchType").addEventListener("change", function() {
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

document.addEventListener("DOMContentLoaded", function() {
    const rows = document.querySelectorAll('.result-row');
    rows.forEach(row => {
        row.addEventListener('click', function() {
            rowHiddenData = row.querySelectorAll('td[hidden]');
            alert(Array.from(rowHiddenData).map(td => td.textContent).join(', '));
        });
    });
});