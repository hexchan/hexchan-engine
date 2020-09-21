# Deployment HOWTO
The supported server configuration is:

* Ubuntu LTS releases 18.04 and 20.04
* Apache 2 with mod_wsgi
* PostgreSQL

Other software combinations are not supported.
You can adapt this guide and `install.sh` script if needed at your own risk.

1.  Install required system dependencies:
    `sudo apt install python3 python3-venv git apache2 libapache2-mod-wsgi-py3 postgresql nodejs npm gettext`
2.  Create new system user, login as him and switch to the homedir.
3.  Clone this repository and switch to the project dir.
4.  Copy `.env.example` file to `.env` and open it with your favorite editor.
5.  Carefully set config options (docs TODO):
    * DEBUG=false
    * SECRET_KEY='abirvalgabirvalgabirvalg'
    * DATABASE_URL=psql://hexchan:abirvalg@localhost/hexchan
    * LANGUAGE_CODE=en
    * TIME_ZONE=UTC
    * HOST=hexchan.org
    * SITE_NAME='HEXCHAN'
    * FAVICON_URL=/static/imageboard/favicon.png
    * STORAGE_DIR=/home/hexchan/hexchan-storage
6.  Read (!) and run `install.sh` script as your created user. 
    Enter your password when prompted by `sudo`. 
    No weird stuff would be done to your machine, we promise.
7.  ?????
8.  PROFIT!
