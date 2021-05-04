#!/usr/bin/env bash

set -e

RED='\033[1;31m'
GREEN='\033[1;32m'
CYAN='\033[1;36m'
NC='\033[0m'  # No color

echo -e "${CYAN}Migrate database:${NC}"
python src/manage.py migrate

echo -e "${CYAN}Collect static assets:${NC}"
python src/manage.py collectstatic --no-input

echo -e "${CYAN}Build locales:${NC}"
python src/manage.py compilemessages

echo -e "${CYAN}Load initial data:${NC}"
src/manage.py loaddata content_blocks

echo -e "${CYAN}Start server:${NC}"
gunicorn --chdir ./src hexchan.wsgi:application --bind 0.0.0.0:8000
