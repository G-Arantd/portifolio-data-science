document.getElementById('update-button').addEventListener('click', function() {
    const updateButton = document.getElementById('update-button');
    updateButton.disabled = true;

    fetch('/database/update', {
        method: 'POST',
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            location.reload();
        } else {
            console.log(data.error);
        }
    })
    .catch(error => {
        console.error('Erro:', error);
        alert('Erro ao atualizar o database.');
    })
    .finally(() => {
        updateButton.disabled = false;
    });
});