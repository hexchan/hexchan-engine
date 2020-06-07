class FormMover {
    constructor() {
        this.el = document.querySelector('.js-posting-form');
        this.mouseInElX = 0;
        this.mouseInElY = 0;

        this.isMoving = false;

        this.el.addEventListener('mousedown', this.onMouseDown.bind(this));
        document.addEventListener('mousemove', this.onMouseMove.bind(this));
        document.addEventListener('mouseup', this.onMouseUp.bind(this));
    }

    onMouseDown(e) {
        e.preventDefault();

        this.isMoving = true;

        this.mouseInElX = this.el.offsetLeft - e.clientX;
        this.mouseInElY = this.el.offsetTop - e.clientY;
    }

    onMouseMove(e) {
        e.preventDefault();

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
