import LocalCollection from './localCollection';


var Highlighter = function(props) {
    function markElements(key, data, selector) {
        // Create localstorage interface
        var localCollection = new LocalCollection({key: key});

        // Concat new data with collection
        localCollection.concat(data);

        // Add attributes for styling marked elements
        var elements = document.querySelectorAll(selector);
        var element, elementId;
        for (var i = 0; i < elements.length; i++) {
            element = elements[i];
            elementId = parseInt(element.getAttribute('data-id'), 10);
            if (localCollection.check(elementId)) {
                element.setAttribute('data-user', true);
            }
        }
    }

    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/session');
    xhr.responseType = 'json';
    xhr.send();
    xhr.onload = function() {
        if (xhr.status === 200) {
            markElements('userThreads', xhr.response['user_threads'], '.js-thread-hid');
            markElements('userPosts', xhr.response['user_posts'], '.js-post-hid');
        }

    }
};


export default Highlighter;
