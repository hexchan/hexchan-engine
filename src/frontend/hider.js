import LocalCollection from './localCollection';
import {tmpl} from './resig-template';



var Hider = function(props) {
    var hiddenClass = props.type + '--hidden';
    var toggleClass = 'js-toggle-' + props.type;
    var multiSelector = '.' + props.type;

    var localCollection = new LocalCollection({
        key: props.storageKey,
        callback: function(collection){
            applyLocalCollectionState();
        }
    });

    var placeholderItem = document.querySelector('#placeholder-item-template');
    if (!placeholderItem) {
        throw 'Placeholder template not found';
    }
    var placeholderItemTemplate = tmpl(placeholderItem.innerHTML.trim());


    function setItemState(itemId, itemHid, isHidden) {
        var item = document.querySelector('#' + props.type + '-' + itemId);

        if (item && item.classList.contains(hiddenClass) === isHidden) {
            return;
        }

        // Do not change this to classlist.toggle, because of IE 11 compability
        isHidden ? item.classList.add(hiddenClass) : item.classList.remove(hiddenClass);

        var placeholderItem;
        if (isHidden) {
            var placeholderTempContainer = document.createElement('div');
            placeholderTempContainer.innerHTML = placeholderItemTemplate({
                id: itemId,
                hid: itemHid,
                type: props.type
            });
            placeholderItem = placeholderTempContainer.firstChild;
            item.parentNode.insertBefore(placeholderItem, item.nextSibling);
        }
        else {
            placeholderItem = document.querySelector('#placeholder-' + props.type + '-' + itemId);
            placeholderItem && placeholderItem.remove();
        }
    }


    function applyLocalCollectionState() {
        var items = document.querySelectorAll(multiSelector);
        var item;

        for (var i = 0; i < items.length; i++) {
            item = items[i];

            var itemId = item.getAttribute('data-id');
            var itemHid = item.getAttribute('data-hid');
            var isHidden = localCollection.check(itemId);

            setItemState(itemId, itemHid, isHidden);
        }
    }


    function onGlobalClick(ev) {
        if (ev.target.classList.contains(toggleClass)) {
            onToggleClick(ev);
        }
    }


    function onToggleClick(ev) {
        var toggler = ev.target;
        var itemId = toggler.getAttribute('data-id');
        var itemHid = toggler.getAttribute('data-hid');
        var isHidden = localCollection.toggle(itemId);

        setItemState(itemId, itemHid, isHidden);
    }


    function init() {
        applyLocalCollectionState();
        document.addEventListener('click', onGlobalClick);
    }


    function destroy() {
        localCollection.destroy();
        document.removeEventListener('click', onGlobalClick);
    }

    init();
    return {
        destroy: destroy
    };
};


export default Hider;
