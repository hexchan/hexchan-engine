import Hider from './scripts/hider';
import Highlighter from './scripts/highlighter';
import RefPopup from './scripts/ref_popup';
import Captcha from './scripts/captcha';
import Lightbox from './scripts/lightbox';
import ImagesWidget from './scripts/images_widget';
import PostExpander from './scripts/post_expander';
import FormMover from './scripts/form_mover';
import RefInserter from './scripts/ref_inserter';
import FormHider from './scripts/form_hider';

// Post and threads hiders
let threadHider = new Hider({
    type: 'thread',
    storageKey: 'hiddenThreads',
});

let postHider = new Hider({
    type: 'post',
    storageKey: 'hiddenPosts',
});

// Highlight user's posts and threads
let hl = new Highlighter();

// Create popup for refs
let refPopup = new RefPopup();

// Create new captcha
let captcha = new Captcha();

// Show full images
let lightbox = new Lightbox();

// Images file input
let imagesWidget = new ImagesWidget();

// Long post expander
let postExpander = new PostExpander();

// Move posting form with mouse
// let formMover = new FormMover(document.getElementById('posting-form'));

// Insert ref when clicking on post number
let refInserter = new RefInserter();

// Toggle posting form
let formHider = new FormHider();
