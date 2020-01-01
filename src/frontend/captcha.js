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
        // Create new XHR
        var xhr = new XMLHttpRequest();

        // Open async request
        xhr.open('GET', '/captcha/' + (doForceUpdate ? '?update=1' : ''), true);

        // Set event handler
        xhr.onreadystatechange = function () { // (3)
            if (xhr.readyState !== 4) return;

            if (xhr.status !== 200) {
                console.error('Error occured when requesting captcha', xhr.status, xhr.statusText);
            } else {
                var captchaData;

                // Parse server response
                try {
                    captchaData = JSON.parse(xhr.responseText);
                } catch (err) {
                    console.error('Error occured when parsing captcha response');
                } finally {
                    if (captchaData) {
                        updateDom(captchaData);
                    }
                }
            }
        };

        // Send request
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
