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
                this.markElements(userThreadsCollection, '.js-user-thread-icon');
    
                userPostsCollection.concat(sessionData['user_posts']);
                this.markElements(userPostsCollection, '.js-user-post-icon');
            })
            .catch((error) => {
                console.error('Failed to fetch user session data', error);
            });        
    }
    
    markElements(collection, selector) {
        Array.from(document.querySelectorAll(selector)).forEach((element) => {
            let elementId = parseInt(element.getAttribute('data-id'));
            
            if (collection.check(elementId)) {
                element.classList.remove('is-hidden');
            }            
        });
    }
}

export default Highlighter;
