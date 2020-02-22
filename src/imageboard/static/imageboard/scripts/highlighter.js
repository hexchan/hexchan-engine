import LocalCollection from './localCollection';

class Highlighter {
    constructor() {
        let userThreadsCollection = new LocalCollection({
            key: 'userThreads',
        });
    
        let userPostsCollection = new LocalCollection({
            key: 'userThreads',
        });
    
        fetch('/session/')
            .then((response) => response.json())
            .then((sessionData) => {
                userThreadsCollection.concat(sessionData['user_threads']);
                this.markElements(userThreadsCollection, '.js-thread-hid');
    
                userPostsCollection.concat(sessionData['user_posts']);
                this.markElements(userPostsCollection, '.js-post-hid');
            })
            .catch((error) => {
                console.error('Failed to fetch user session data', error);
            });        
    }
    
    markElements(collection, selector) {
        Array.from(document.querySelectorAll(selector)).forEach((element) => {
            let elementId = parseInt(element.getAttribute('data-id'));
            
            if (collection.check(elementId)) {
                element.setAttribute('data-user', true);
            }            
        });
    }
}

export default Highlighter;
