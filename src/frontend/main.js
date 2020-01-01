import lightbox from 'lightbox2';
import Hider from './hider';
import Highlighter from './highlighter';
import RefPopup from './ref_popup';
import Captcha from './captcha';
import globalErrorHandler from './client_errors';


// Set global error handler
window.onerror = globalErrorHandler;


// Lightbox config
var lb = lightbox.option({
    resizeDuration: 300,
    fadeDuration: 300,
    imageFadeDuration: 300,
});


// Post and threads hiders
var threadHider = new Hider({
    type: 'thread',
    storageKey: 'hiddenThreads',
});

var postHider = new Hider({
    type: 'post',
    storageKey: 'hiddenPosts',
});


// Highlight user's posts and threads
var hl = new Highlighter();


// Create popup for refs
var refPopup = new RefPopup();


// Create new captcha
var captcha = new Captcha();
