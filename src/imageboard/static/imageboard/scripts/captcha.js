class Captcha {
    constructor() {
        document.querySelector('.js-captcha-refresh').addEventListener('click', () => {
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
                document.querySelector('.js-captcha-id').value = captchaData.publicId;
                document.querySelector('.js-captcha-image').src = captchaData.image;                
            })
            .catch((error) => {
                console.error('Failed to fetch captcha data', error);
            });
    }
}

export default Captcha;
