.ONESHELL:

.PHONY: install_deps init_storage build_frontend create_database collect_static create_admin generate_captchas install

cyan := $(shell tput setaf 6)
sgr0 := $(shell tput sgr0)

separator := ''

install_deps:
	@echo $(separator)
	@echo '$(cyan)Install NodeJS and Python dependencies$(sgr0)'
	@echo '$(cyan)======================================$(sgr0)'
	npm install --loglevel error
	python3 -m venv python_modules
	. python_modules/bin/activate
	pip install --quiet --upgrade pip
	pip install --quiet -r requirements.txt

init_storage:
	@echo $(separator)
	@echo '$(cyan)Create storage directories, set group and permission$(sgr0)'
	@echo '$(cyan)====================================================$(sgr0)'
	. python_modules/bin/activate
	src/manage.py create_storage_dirs
	sudo chmod -R 775 $(shell src/manage.py print_storage_path)
	sudo chgrp -R www-data $(shell src/manage.py print_storage_path)

build_frontend:
	@echo $(separator)
	@echo '$(cyan)Build frontend$(sgr0)'
	@echo '$(cyan)==============$(sgr0)'	
	npm run build:styles
	npm run build:scripts

create_database:
	@echo $(separator)
	@echo '$(cyan)Create database and apply initial migrations$(sgr0)'
	@echo '$(cyan)============================================$(sgr0)'
	. python_modules/bin/activate
	src/manage.py create_postgresql_script | sudo -u postgres psql -a
	src/manage.py migrate

collect_static:
	@echo $(separator)
	@echo '$(cyan)Collect static content$(sgr0)'
	@echo '$(cyan)======================$(sgr0)'	
	. python_modules/bin/activate
	src/manage.py collectstatic

build_locales:
	@echo $(separator)
	@echo '$(cyan)Build locale messages$(sgr0)'
	@echo '$(cyan)=====================$(sgr0)'	
	. python_modules/bin/activate
	src/manage.py compilemessages

create_admin:
	@echo $(separator)
	@echo '$(cyan)Create admin user$(sgr0)'
	@echo '$(cyan)=================$(sgr0)'	
	. python_modules/bin/activate
	src/manage.py createsuperuser

generate_captchas:
	@echo $(separator)
	@echo '$(cyan)Generate some captchas$(sgr0)'
	@echo '$(cyan)======================$(sgr0)'	
	. python_modules/bin/activate
	src/manage.py makecaptchas 1000

# Install app with all commands
install: install_deps init_storage build_frontend create_database collect_static create_admin generate_captchas

