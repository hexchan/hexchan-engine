class RefPopup {
    constructor() {
        this.POPUP_VERTICAL_OFFSET = 5;
        this.popupIsVisible = false;

        document.addEventListener('mouseover', this.onMouseOver.bind(this));
        document.addEventListener('mouseout', this.onMouseOut.bind(this));
    }

    onMouseOver(ev) {
        if (ev.target.classList.contains('js-ref')) {
            let hid = ev.target.innerHTML.replace('&gt;&gt;', '');
            let postEl = document.querySelector('.js-post[data-hid="' + hid + '"]');

            this.popupIsVisible = true;

            if (postEl) {
                this.showPopup(ev.target, hid, postEl.cloneNode(true));
            } else {
                let url = ev.target.getAttribute('href').replace('#', '') + '/';

                fetch(url)
                    .then((response) => response.text())
                    .then((responseText) => {
                        this.showPopup(ev.target, hid, responseText);

                    })
                    .catch((error) => {
                        console.error('Failed to fetch post\'s HTML', error);
                    });
            }
        }
    }

    onMouseOut() {
        this.popupIsVisible = false;

        Array.from(document.querySelectorAll('.js-ref-popup')).forEach((popup) => {
            popup.remove();
        });
    }

    showPopup(target, hid, content) {
        if (this.popupIsVisible) {
            let targetBox = target.getBoundingClientRect();

            let popupEl = document.createElement('div');

            if (typeof content === 'string') {
                popupEl.innerHTML = content;
            } else if (content instanceof Element) {
                popupEl.appendChild(content);
            }

            popupEl.className = 'ref-popup js-ref-popup';
            popupEl.setAttribute('data-hid', hid);
            popupEl.style.top = targetBox.top + targetBox.height + this.POPUP_VERTICAL_OFFSET + window.pageYOffset + 'px';
            popupEl.style.left = 0 + 'px';

            Array.from(popupEl.querySelectorAll('.js-toggle-thread, .js-toggle-post')).forEach((elementToRemove) => {
                elementToRemove.remove();
            });

            document.querySelector('.js-popup-container').appendChild(popupEl);
        }
    }
}

export default RefPopup;
