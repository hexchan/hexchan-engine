# hexchan-engine
Hexchan-engine is an anonymous imageboard software written in Python using Django framework.

What's an *imageboard*, you may ask. It's a webforum, where you can post messages without registration 
and pictures are typically used to communicate all sorts of ideas, thus *imageboard*. 
An example would be the infamous 4chan.org.

# Project status
[![Build Status](https://travis-ci.org/hexchan/hexchan-engine.svg?branch=master)](https://travis-ci.org/hexchan/hexchan-engine)

## Is it deployed somewhere?
Yes, it powers an already existing Russian imageboard **Hexchan** at https://hexchan.org
Feel free to visit us and leave a message in English or Russian.

## Can I use it?
Of course! Hexchan-engine is licensed under MIT license, so you may use it to make your own imageboard.
Although we wouldn't recommend doing this right now, the engine is still a work in progress. 
Also there is no installation manual yet. Stay tuned for our first release!

## What features does it have?
### For users:
* Markup commands (modelled after Wakaba engine's markup)
* Multiple image attachments
* Fullscreen image viewer
* Mobile-friendly layout
* Thread and post hiding
* Reply popup
* User's threads and posts highlighting
### For admins:
* Administrative panel (created with Django Admin module)
* Moderation features: bans, regex-based wordfilter, checksum-based imagefilter
* Captcha
* Hidden boards (active, but not displayed in the board list)
* Sticky threads (always stay at top of the first page)
* Configurable posts and threads limits
