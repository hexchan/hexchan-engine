class ImagesWidget {
    constructor() {
        this.widget = document.querySelector('.js-images-widget');

        if (!this.widget) {
            return;
        }

        this.fileInput = document.querySelector('.js-images-widget-input');
        this.previewsList = document.querySelector(
            '.js-images-widget-previews'
        );

        this.maxFileSize = parseInt(this.fileInput.dataset.maxFileSize);
        this.maxFileNum = parseInt(this.fileInput.dataset.maxFileNum);
        this.fileTypes = this.fileInput.getAttribute('accept');

        this.fileInput.addEventListener(
            'change',
            this.onFileInputChange.bind(this)
        );

        this.onFileInputChange();
    }

    onFileInputChange() {
        let files = this.fileInput.files;

        let error = this.checkFiles(files);

        // Show previews or error
        if (!error) {
            this.showPreviews(files);
        } else {
            this.clearWidget();
            this.showError(error);
        }
    }

    checkFiles(files) {
        let error = null;

        // Check files by type and size
        for (let file of files) {
            if (file.size > this.maxFileSize) {
                error = 'too_large';
                break;
            }

            if (this.fileTypes.indexOf(file.type) === -1) {
                console.log(this.fileTypes, file.type);
                error = 'bad_format';
                break;
            }
        }

        // Check number of images
        if (files.length > this.maxFileNum) {
            error = 'too_many';
        }

        return error;
    }

    showPreviews(files) {
        // Clear previews list
        this.previewsList.innerHTML = '';

        // Show image previews
        for (let file of files) {
            // Create image preview
            let preview = document.createElement('div');
            preview.classList.add('images-widget__preview');
            preview.title = file.name;
            this.previewsList.appendChild(preview);

            // Read file and set image in preview
            let reader = new FileReader();
            reader.onload = (function (currentPreview) {
                return function (e) {
                    currentPreview.style.backgroundImage = `url("${e.target.result}")`;
                };
            })(preview);
            reader.readAsDataURL(file);
        }
    }

    clearWidget() {
        this.fileInput.value = null;
        this.showPreviews([]);
    }

    showError(error) {
        let errorMessageEl = this.widget.querySelector(
            `.js-images-widget-error[data-error="${error}"]`
        );

        alert(errorMessageEl.textContent.trim());
    }
}

export default ImagesWidget;
