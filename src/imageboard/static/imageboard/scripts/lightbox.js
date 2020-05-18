export default class Lightbox {
    constructor() {
        // State
        this.isOpen = false;

        // Elements
        this.root = document.querySelector('#lightbox');
        this.image = this.root.querySelector('.lightbox__image');
        this.imageWrap = this.root.querySelector('.lightbox__image-wrap');
        this.loader = this.root.querySelector('.lightbox__loader');
        this.error = this.root.querySelector('.lightbox__error');
        this.closeButton = this.root.querySelector('.lightbox__close');
        this.title = this.root.querySelector('.lightbox__title');

        // Event listeners
        document.addEventListener('click', this.onThumbnailClick.bind(this));
        document.addEventListener('keyup', this.onEscapeButtonPress.bind(this));
        window.addEventListener('resize', this.onWindowResize.bind(this));
        this.image.addEventListener('load', this.onImageLoad.bind(this), false);
        this.image.addEventListener('error', this.onImageError.bind(this), false);
        this.root.addEventListener('click', this.onBackgroundClick.bind(this));
        this.closeButton.addEventListener('click', this.onCloseButtonClick.bind(this));

    }

    onEscapeButtonPress(ev) {
        if (this.isOpen && ev.keyCode === 27) {
            this.close();
        }
    }

    onThumbnailClick(ev) {
        let target = ev.target;

        while (target && !target.matches('.js-lightbox-link')) {
            target = target.parentElement;
        }

        if (target) {
            ev.preventDefault();

            let url = target.getAttribute('href');
            let title = target.getAttribute('data-title');
            let alt = target.getAttribute('data-alt');
            let width = target.getAttribute('data-width');
            let height = target.getAttribute('data-height');

            this.open(url, title, alt, width, height);
        }
    }

    onCloseButtonClick() {
        this.close();
    }

    onBackgroundClick(ev) {
        if (ev.target === this.root) {
            this.close();
        }
    }

    onImageLoad() {
        // Check for empty images and 404's
        if (!this.image.naturalWidth || !this.image.naturalHeight) {
            this.onImageError();
        } else {
            this.toggleLoader(false);
            this.toggleError(false);
            this.resizeImage();
            this.toggleImage(true);
        }
    }

    onImageError() {
        this.toggleLoader(false);
        this.toggleError(true);
        this.toggleImage(false);
    }

    open(url, title, alt) {
        this.isOpen = true;
        this.toggleWindow(true);
        this.toggleLoader(true);
        this.toggleError(false);
        this.toggleImage(false);

        this.image.src = url;
        this.image.alt = alt;
        this.image.title = title;

        this.title.textContent = title;
        this.title.title = title;
    }

    close() {
        this.isOpen = false;
        this.toggleWindow(false);
        this.toggleLoader(false);
        this.toggleError(false);
        this.toggleImage(false);

        this.image.src = null;
        this.image.alt = null;
        this.image.title = '';

        this.title.textContent = '';
        this.title.title = '';
    }

    toggleWindow(isVisible) {
        this.root.classList.toggle('lightbox--hidden', !isVisible);
    }

    toggleLoader(isVisible) {
        this.loader.classList.toggle('lightbox__loader--hidden', !isVisible);
    }

    toggleImage(isVisible) {
        this.imageWrap.classList.toggle('lightbox__image-wrap--hidden', !isVisible);
    }

    toggleError(isVisible) {
        this.error.classList.toggle('lightbox__error--hidden', !isVisible);
    }

    onWindowResize() {
        if (this.isOpen && this.image && this.image.src) {
            this.resizeImage();
        }
    }

    resizeImage() {
        let maxImageWidth = window.innerWidth * 0.8;
        let maxImageHeight = window.innerHeight * 0.8;

        let imageWidth = this.image.naturalWidth;
        let imageHeight = this.image.naturalHeight;

        if ((imageWidth > maxImageWidth) || (imageHeight > maxImageHeight)) {
            let scale = Math.min( maxImageWidth / imageWidth, maxImageHeight / imageHeight);

            imageWidth = imageWidth * scale;
            imageHeight = imageHeight * scale;

            this.image.style.width = imageWidth + 'px';
            this.image.style.height = imageHeight + 'px';
        } else {
            this.image.style.removeProperty('width');
            this.image.style.removeProperty('height');
        }
    }
}