class FormHider {
    constructor() {
        this.postingForm = document.querySelector('.js-posting-form');
        this.togglePostingFormButton = document.querySelector('.js-toggle-posting-form-button');

        if (!this.postingForm || !this.togglePostingFormButton) {
            return;
        }

        this.togglePostingFormButton.addEventListener(
            'click',
            this.onToggleFormButtonClick.bind(this)
        );
    }

    onToggleFormButtonClick() {
        this.postingForm.classList.toggle('is-hidden');
    }
}

export default FormHider;
