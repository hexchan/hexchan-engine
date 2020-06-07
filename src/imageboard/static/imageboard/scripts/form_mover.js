class FormMover {
    constructor(el) {
        this.el = el;
        this.mouseInElX = 0;
        this.mouseInElY = 0;

        this.el.onmousedown = this.dragMouseDown.bind(this);
    }

    dragMouseDown(e) {
        e.preventDefault();

        this.mouseInElX = this.el.offsetLeft - e.clientX;
        this.mouseInElY = this.el.offsetTop - e.clientY;
        
        document.onmouseup = this.closeDragElement.bind(this);
        document.onmousemove = this.elementDrag.bind(this);
    }

    elementDrag(e) {
        e.preventDefault();

        this.el.style.left = e.clientX + this.mouseInElX + 'px';
        this.el.style.top = e.clientY + this.mouseInElY + 'px';
    }

    closeDragElement() {
        document.onmouseup = null;
        document.onmousemove = null;
    }
}

export default FormMover;
