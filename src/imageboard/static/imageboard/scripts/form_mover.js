// TODO: good looks on mobile
// TODO: rename to PostingForm or something
// TODO: add visibility toggling button at the top of the page, display form as attached there, detach on reply
// TODO: quick reply to any thread from the board page

class FormMover {
    constructor() {
        this.el = document.querySelector('.js-posting-form');

        if (!this.el) {
            return;
        }

        this.headerEl = this.el.querySelector('.js-posting-form-header');
        this.closeButtonEl = this.el.querySelector('.js-posting-form-close');
        this.mouseInElX = 0;
        this.mouseInElY = 0;

        this.isMoving = false;
        this.isHidden = true;

        this.headerEl.addEventListener(
            'mousedown',
            this.onMouseDown.bind(this)
        );
        this.closeButtonEl.addEventListener(
            'click',
            this.onCloseButtonClick.bind(this)
        );
        document.addEventListener('mousemove', this.onMouseMove.bind(this));
        document.addEventListener('mouseup', this.onMouseUp.bind(this));
        document.addEventListener('click', this.onReplyButtonClick.bind(this));
        window.addEventListener('resize', this.onWindowResize.bind(this));

        this.newThreadButtonEl = document.querySelector('.js-new-thread-button');
        if (this.newThreadButtonEl) {
            this.newThreadButtonEl.addEventListener(
                'click',
                this.onNewThreadButtonClick.bind(this)
            );
        }
    }

    toggleVisibility(isHidden) {
        if (this.isHidden !== isHidden) {
            // Set visibility flag
            this.isHidden = isHidden;

            // Toggle visibility class
            this.el.classList.toggle('is-hidden', isHidden);

            // If dialog became visiblie - move it to the right middle
            if (!isHidden) {
                this.placeWindow();
            }
        }
    }

    placeWindow() {
        this.el.style.left =
            (window.innerWidth - this.el.offsetWidth) * 0.9 + 'px';
        this.el.style.top =
            (window.innerHeight - this.el.offsetHeight) / 2 + 'px';
    }

    onReplyButtonClick(e) {
        let target = e.target;
        if (target && target.matches('.js-reply-button')) {
            e.preventDefault();

            // Show form
            this.toggleVisibility(false);

            // Message textarea
            let textarea = this.el.querySelector('textarea');

            // Post ref to insert
            let strToInsert = `>>${target.textContent.trim()}\n`;

            // Focus into textarea
            textarea.focus();

            // Insert post HID to the main textarea
            let startPos = textarea.selectionStart;
            let endPos = textarea.selectionEnd;
            textarea.value =
                textarea.value.substring(0, startPos) +
                strToInsert +
                textarea.value.substring(endPos, textarea.value.length);

            // Move cursor after insertion
            textarea.selectionEnd = startPos + strToInsert.length;
        }
    }

    onNewThreadButtonClick(e) {
        let target = e.target;
        if (target && target.matches('.js-new-thread-button')) {
            e.preventDefault();

            this.toggleVisibility(false);
        }
    }

    onMouseDown(e) {
        // Prevent default to prevent text selection
        e.preventDefault();

        this.isMoving = true;

        this.mouseInElX = this.el.offsetLeft - e.clientX;
        this.mouseInElY = this.el.offsetTop - e.clientY;
    }

    onMouseMove(e) {
        // Prevent default to prevent text selection
        e.preventDefault();

        if (this.isMoving) {
            this.el.style.left = e.clientX + this.mouseInElX + 'px';
            this.el.style.top = e.clientY + this.mouseInElY + 'px';
        }
    }

    onMouseUp() {
        this.isMoving = false;
    }

    onWindowResize() {
        this.placeWindow();
    }

    onCloseButtonClick() {
        this.toggleVisibility(true);
    }
}

export default FormMover;
