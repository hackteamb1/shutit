var positionText = document.querySelector('#position');

function fetchUpdatePosition() {
    fetch('/api/state/by_id/' + id).then((response) => {
        response.json().then((json) => {
            positionText.innerText = json.number_in_queue;
            return json.number_in_queue;
        });
    });
};


fetchUpdatePosition();
setInterval(fetchUpdatePosition, 5000);
