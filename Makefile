-include .env
export

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("	%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

help:
	@echo "Usage: make <command>"
	@echo "Options:"
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

build:  ## Build api
	docker-compose down --volumes
	docker-compose build

bash:  ## Run api bin/bash
	@docker-compose run --rm runner

seeder:  ## Seed database
	@docker-compose run --rm runner python seeds/seed_*.py

test:  ## Run api tests
	@docker-compose run --rm runner pytest --cov-report=term-missing --cov-report=html --cov=.

code-convention:  ## Run code convention
	@docker-compose run --rm runner flake8 main.py app tests
	@echo == Code convention is ok

run:  ## Run api
	@docker-compose up cart_api

run-debug:  ## Run api in debugger mode
	docker-compose run --rm -e FLASK_DEBUGGER=${FLASK_DEBUGGER} --service-ports cart_api flask run --host 0.0.0.0

install: build seeder test code-convention  ## Install api
