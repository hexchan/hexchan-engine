#!/usr/bin/env bash

set -e

GREEN='\033[1;32m'
CYAN='\033[1;36m'
NC='\033[0m'  # No color

echo -e "${CYAN}Updating Hexchan Engine:${NC}"

echo -e "${CYAN}* Install Python deps${NC}"
source python_modules/bin/activate
pip install --quiet --upgrade pip
pip install --quiet -r requirements.txt

echo -e "${CYAN}* Install frontend deps${NC}"
npm install --silent --no-fund --no-progress --no-audit

echo -e "${CYAN}* Build frontend from source${NC}"
npm run --silent build:styles
npm run --silent build:scripts

echo -e "${CYAN}* Migrate database${NC}"
src/manage.py migrate --verbosity 0

echo -e "${CYAN}* Collect static assets${NC}"
src/manage.py collectstatic --verbosity 0

echo -e "${CYAN}* Rebuild locales${NC}"
src/manage.py compilemessages --verbosity 0

echo -e "${GREEN}Done!${NC}"
