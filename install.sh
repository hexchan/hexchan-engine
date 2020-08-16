#!/usr/bin/env bash

set -e

RED='\033[1;31m'
GREEN='\033[1;32m'
CYAN='\033[1;36m'
NC='\033[0m'  # No color

echo -e "${CYAN}Installing Hexchan Engine:${NC}"

echo -e "${CYAN}* Test for .env config file${NC}"
if ! [[ -e ".env" ]]; then
  echo -e "${RED}Please create .env file!${NC}"
  exit 1
fi

echo -e "${CYAN}* Create Python environment, install deps${NC}"
python3 -m venv python_modules
source python_modules/bin/activate
pip install --quiet --upgrade pip
pip install --quiet -r requirements.txt

echo -e "${CYAN}* Install frontend deps${NC}"
npm install --silent --no-fund --no-progress --no-audit

echo -e "${CYAN}* Build frontend from source${NC}"
npm run --silent build:styles
npm run --silent build:scripts

echo -e "${CYAN}* Initialize storage${NC}"
src/manage.py create_storage_dirs
sudo chmod -R 775 "$(src/manage.py print_storage_path)"
sudo chgrp -R www-data "$(src/manage.py print_storage_path)"

echo -e "${CYAN}* Initialize PostgreSQL database${NC}"
src/manage.py create_postgresql_script | sudo -u postgres psql --quiet

echo -e "${CYAN}* Migrate database${NC}"
src/manage.py migrate --verbosity 0

echo -e "${CYAN}* Collect static assets${NC}"
src/manage.py collectstatic --verbosity 0

echo -e "${CYAN}* Build locales${NC}"
src/manage.py compilemessages --verbosity 0

echo -e "${CYAN}* Create site admin user${NC}"
src/manage.py createsuperuser --verbosity 0

echo -e "${CYAN}* Load initial data${NC}"
src/manage.py content_blocks --verbosity 0

echo -e "${CYAN}* Generate captchas${NC}"
src/manage.py makecaptchas 1000

echo -e "${CYAN}* Create Apache site and enable it${NC}"
src/manage.py create_apache_config | sudo tee /etc/apache2/sites-available/hexchan.conf > /dev/null
sudo a2ensite hexchan.conf
sudo service apache2 reload

echo -e "${GREEN}Done!${NC}"
