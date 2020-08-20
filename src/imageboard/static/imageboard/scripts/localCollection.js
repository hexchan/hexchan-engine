class LocalCollection {
    constructor(props) {
        this.key = props.key;
        this.callback = props.callback;
        this.collection = new Set();

        this.readFromStorage();
        window.addEventListener('storage', this.onStorageUpdate.bind(this));
    }

    onStorageUpdate(ev){
        if (ev.key === this.key) {
            this.readFromStorage();
            if (typeof this.callback === 'function') {
                this.callback(this.collection);
            }
        }
    }

    readFromStorage() {
        let collectionString = window.localStorage.getItem(this.key);

        try {
            this.collection = new Set(JSON.parse(collectionString));
        } catch (e) {
            this.collection = new Set();
        }
    }

    writeToStorage() {
        let collectionArray = Array.from(this.collection);
        let collectionString = JSON.stringify(collectionArray);
        window.localStorage.setItem(this.key, collectionString);
    }    

    clear() {
        this.collection = new Set();
        this.writeToStorage();
    }

    check(item) {
        return this.collection.has(item);
    }

    push(item) {
        this.collection.add(item);
        this.writeToStorage();
    }

    remove(item) {
        this.collection.delete(item);
        this.writeToStorage();
    }

    toggle(item) {
        let status;
        if (this.collection.has(item)) {
            this.collection.delete(item);
            status = false;
        } else {
            this.collection.add(item);
            status = true;            
        }
        this.writeToStorage();
        return status;
    }

    concat(list) {
        if (Array.isArray(list)) {
            this.collection = new Set([...this.collection, ...list]);
            this.writeToStorage();
        } else {
            throw 'Can only concat arrays';
        }

    }
}

export default LocalCollection;
