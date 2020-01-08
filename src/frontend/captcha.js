var Captcha = function() {
    function init() {
        document.addEventListener('click', onRefreshButtonClick);
        window.addEventListener('pageshow', onPageShow);
    }


    function destroy() {
        document.removeEventListener('click', onRefreshButtonClick);
        window.removeEventListener('pageshow', onPageShow);
    }


    function onRefreshButtonClick(ev) {
        if (ev.target.classList.contains('js-captcha-refresh')) {
            requestCaptcha(true);
        }
    }

    // This function will be called on 'pageshow' event, which emitted either on page load, or history change
    function onPageShow() {
        requestCaptcha();
    }


    function requestCaptcha(doForceUpdate) {
        var xhr = new XMLHttpRequest();

        xhr.open('GET', '/captcha/' + (doForceUpdate ? '?update=1' : ''), true);

        xhr.responseType = 'json';

        xhr.onload = function () { // (3)
            if (xhr.status === 200) {
                updateDom(xhr.response);
            } else {
                console.error('Failed to fetch captcha data');
            }
        };

        xhr.onerror = function() {
            console.error('Failed to fetch captcha data');
        };

        xhr.send();
    }


    function updateDom(captchaData) {
        var captchaImage = captchaData.image;
        var captchaId = captchaData.publicId;

        // Set captcha public id
        var captchaIdEl = document.querySelector('.js-captcha-id');
        if (captchaIdEl) {
            captchaIdEl.value = captchaId;
        }

        // Set captcha image
        var captchaImageEl = document.querySelector('.js-captcha-image');
        if (captchaImageEl) {
            captchaImageEl.src = captchaImage;
        }
    }


    init();
    return {
        destroy: destroy,
        requestCaptcha: requestCaptcha
    }
}


export default Captcha;
