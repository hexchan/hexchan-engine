class PostExpander {
    constructor() {
        let postTextEls = document.querySelectorAll('.js-post-text');
        let maxHeight = 200;

        // Expander label template
        let templateItem = document.querySelector('#post-expander-template');
        this.template = templateItem.innerHTML.trim();

        // Collapse long posts
        for (let textEl of postTextEls) {
            if (textEl.offsetHeight > maxHeight) {
                textEl.setAttribute('data-collapsed', true);
                textEl.insertAdjacentHTML('beforeend', this.template);
            }
        }

        // Listen for clicks on expander labels
        document.addEventListener('click', this.onGlobalClick.bind(this));
    }

    onGlobalClick(ev) {
        let target = ev.target;
        if (target && target.matches('.js-post-expander')) {
            target.parentNode.parentNode.removeAttribute('data-collapsed');
            target.parentNode.remove();
        }
    }
}

export default PostExpander;
