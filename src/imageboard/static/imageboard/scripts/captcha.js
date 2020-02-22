class Captcha {
    constructor() {
        this.captchaRefreshButton = document.querySelector('.js-captcha-refresh');
        this.captchaImage = document.querySelector('.js-captcha-image');
        this.captchaHiddenInput = document.querySelector('.js-captcha-id');

        if (!this.captchaRefreshButton || !this.captchaImage || !this.captchaHiddenInput) {
            return;
        }

        this.captchaRefreshButton.addEventListener('click', () => {
            this.requestCaptcha(true);
        });

        window.addEventListener('pageshow', () => {
            this.requestCaptcha();
        });
    }

    requestCaptcha(doForceUpdate) {
        let url = '/captcha/' + (doForceUpdate ? '?update=1' : '');

        fetch(url)
            .then((response) => response.json())
            .then((captchaData) => {
                this.captchaHiddenInput.value = captchaData.publicId;
                this.captchaImage.src = captchaData.image;
            })
            .catch((error) => {
                console.error('Failed to fetch captcha data', error);
            });
    }
}

export default Captcha;
