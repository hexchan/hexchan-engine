class EmailRevealer {
    constructor() {
        let blockEl = document.querySelector('.js-email-block');
        let addressEl = document.querySelector('.js-email-address');

        blockEl.classList.remove('is-hidden');

        let address = `${addressEl.dataset.uuu}@${addressEl.dataset.hhh}`;
        addressEl.href = `mailto:${address}`;
        addressEl.text = address;
    }
}

export default EmailRevealer;
