import Hider from './scripts/hider';
import Highlighter from './scripts/highlighter';
import RefPopup from './scripts/ref_popup';
import Captcha from './scripts/captcha';

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