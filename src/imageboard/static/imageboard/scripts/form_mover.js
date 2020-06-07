class FormMover {
    constructor() {
        this.el = document.querySelector('.js-posting-form');
        this.mouseInElX = 0;
        this.mouseInElY = 0;

        this.isMoving = false;

        this.el.addEventListener('mousedown', this.onMouseDown.bind(this));
        document.addEventListener('mousemove', this.onMouseMove.bind(this));
        document.addEventListener('mouseup', this.onMouseUp.bind(this));
        document.addEventListener('click', this.onReplyButtonClick.bind(this));
    }

    toggleVisibility(isHidden) {
        this.el.classList.toggle('is-hidden', isHidden);
    }

    onReplyButtonClick(e) {
        let target = e.target;
        if (target && target.matches('.js-reply-button')) {
            e.preventDefault();

            // Show form
            this.toggleVisibility(false);

            // Move form to the reply button
            this.el.style.left = target.offsetLeft + target.offsetWidth + 'px';
            this.el.style.top = target.offsetTop + target.offsetHeight + 'px';

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

    onNewThreadButtonClick() {
        let target = e.target;
        if (target && target.matches('.js-new-thread-button')) {
            e.preventDefault();

            this.toggleVisibility(false);
        }
    }

    onMouseDown(e) {
        this.isMoving = true;

        this.mouseInElX = this.el.offsetLeft - e.clientX;
        this.mouseInElY = this.el.offsetTop - e.clientY;
    }

    onMouseMove(e) {
        if (this.isMoving) {
            this.el.style.left = e.clientX + this.mouseInElX + 'px';
            this.el.style.top = e.clientY + this.mouseInElY + 'px';
        }
    }

    onMouseUp() {
        this.isMoving = false;
    }
}

export default FormMover;
