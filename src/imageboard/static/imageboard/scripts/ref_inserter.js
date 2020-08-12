class RefInserter {
    constructor() {
        this.postingFormEl = document.querySelector('.js-posting-form');

        if (!this.postingFormEl) {
            return;
        }

        document.addEventListener('click', this.onReplyButtonClick.bind(this));
    }

    onReplyButtonClick(e) {
        let target = e.target;
        if (target && target.matches('.js-reply-button')) {
            e.preventDefault();

            // Message textarea
            let textarea = this.postingFormEl.querySelector('textarea');

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
}

export default RefInserter;