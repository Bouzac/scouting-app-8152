function getInputValue() {
    const inputElement = document.getElementById('team_number');
    const inputValue = inputElement.value;

    window.location.href = `/reports/${inputValue}`;
}