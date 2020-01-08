function globalErrorHandler(msg, url, line, column, error) {
    function getCookie(name) {
        let matches = document.cookie.match(new RegExp(
        "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
        ));
        return matches ? decodeURIComponent(matches[1]) : undefined;
    }

    // Get CSRF token
    var csrfToken = getCookie('csrftoken');
    if (!csrfToken) {
        console.error('Couldn\'t get CSRF token. Aborted.');
        return;
    }

    // Create new request
    var xhr = new XMLHttpRequest();

    xhr.open('POST', '/clientErrors/', true);

    xhr.responseType = 'json';

    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.setRequestHeader("X-CSRFToken", csrfToken);

    xhr.onload = function() {
        if (xhr.status !== 200) {
            console.error('Error occured when sending client error to the server');
        }
    };

    xhr.onerror = function() {
        console.error('Error occured when sending client error to the server');
    };


    // Make request body
    var requestBodyArray = [
        'msg=' + encodeURIComponent(msg.toString()),
        'url=' + encodeURIComponent(url.toString()),
        'line=' + encodeURIComponent(line.toString())
    ];
    var requestBody = requestBodyArray.join('&');

    // Send request
    xhr.send(requestBody);

    // 'False' result here means 'propagate error to other handlers'
    return false;
}


export default globalErrorHandler;
