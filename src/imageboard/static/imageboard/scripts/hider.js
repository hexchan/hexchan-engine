import LocalCollection from './localCollection';
import {tmpl} from './resig-template';


class Hider {
    constructor(props) {
        this.type = props.type;
        this.hiddenClass = `${this.type}--hidden`;
        this.toggleClass = `js-toggle-${this.type}`;
        this.multiSelector = `.${this.type}`;

        // Create LocalStorage array interface
        this.localCollection = new LocalCollection({
            key: props.storageKey,
            callback: () => {
                this.applyLocalCollectionState();
            }
        });

        // Load template string and create template function
        let templateItem = document.querySelector('#placeholder-item-template');
        this.template = tmpl(templateItem.innerHTML.trim());

        // Set event listeners
        this.applyLocalCollectionState();
        document.addEventListener('click', this.onGlobalClick.bind(this));
    }


    setItemState(itemId, itemHid, isHidden) {
        let item = document.querySelector(`#${this.type}-${itemId}`);

        if (item.classList.contains(this.hiddenClass) !== isHidden) {
            item.classList.toggle(this.hiddenClass, isHidden);

            if (isHidden) {
                let placeholderString = this.template({
                    id: itemId,
                    hid: itemHid,
                    type: this.type
                });

                item.insertAdjacentHTML('beforebegin', placeholderString);
            } else {
                document.querySelector(`#placeholder-${this.type}-${itemId}`).remove();
            }
        }
    }

    // Apply DOM state from localStorage
    applyLocalCollectionState() {
        Array.from(document.querySelectorAll(this.multiSelector)).forEach((item) => {
            let itemId = item.getAttribute('data-id');
            let itemHid = item.getAttribute('data-hid');
            let isHidden = this.localCollection.check(itemId);

            this.setItemState(itemId, itemHid, isHidden);
        });
    }

    // Update DOM state when click on toggler elements
    onGlobalClick(ev) {
        if (ev.target.classList.contains(this.toggleClass)) {
            let toggler = ev.target;
            let itemId = toggler.getAttribute('data-id');
            let itemHid = toggler.getAttribute('data-hid');
            let isHidden = this.localCollection.toggle(itemId);
    
            this.setItemState(itemId, itemHid, isHidden);
        }
    }
}

export default Hider;
