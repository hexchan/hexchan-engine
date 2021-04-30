import Hider from './scripts/hider';
import Highlighter from './scripts/highlighter';
import RefPopup from './scripts/ref_popup';
import Lightbox from './scripts/lightbox';
import ImagesWidget from './scripts/images_widget';
import PostExpander from './scripts/post_expander';
// import FormMover from './scripts/form_mover';
import RefInserter from './scripts/ref_inserter';
import FormHider from './scripts/form_hider';
import EmailRevealer from './scripts/email_revealer';

// Post and threads hiders
new Hider({
    type: 'thread',
    storageKey: 'hiddenThreads',
});

new Hider({
    type: 'post',
    storageKey: 'hiddenPosts',
});

// Highlight user's posts and threads
new Highlighter();

// Create popup for refs
new RefPopup();

// Show full images
new Lightbox();

// Images file input
new ImagesWidget();

// Long post expander
new PostExpander();

// Move posting form with mouse
// new FormMover(document.getElementById('posting-form'));

// Insert ref when clicking on post number
new RefInserter();

// Toggle posting form
new FormHider();

// Reveal admin email
new EmailRevealer();
