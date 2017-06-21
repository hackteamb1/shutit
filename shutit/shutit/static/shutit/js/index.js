'use strict';

var positionText = document.querySelector('#position');

function fetchUpdatePosition() {
    fetch('/api/state/by_id/' + id).then(function (response) {
        response.json().then(function (json) {
            positionText.innerText = json.number_in_queue;
            return json.number_in_queue;
        });
    });
};

fetchUpdatePosition();
setInterval(fetchUpdatePosition, 1000);
