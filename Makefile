.ONESHELL:

SHELL  = /bin/bash
PYTHON = /usr/bin/python3

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
	@$(PYTHON) -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)


build:  ## Build api
	@docker-compose down --volumes
	@docker-compose build

mongodb:  ## Run mongodb
	@docker-compose up mongodb -d

seeder:  ## Seed database
	@docker-compose run --rm cart_api python seeds/seed_*.py

tests: -B  ## Run api tests
	@FLASK_DEBUG=true docker-compose run --rm cart_api pytest --cov-report=term-missing --cov-report=html --cov=.

code-convention:  ## Run code convention
	@docker-compose run --rm cart_api flake8 main.py gunicorn.py app tests && \
	  echo == Code convention is ok

run:  ## Run api
	@FLASK_DEBUGGER=false docker-compose up cart_api

run-debug:  ## Run api in debugger mode
	@COMPOSE_COMMAND="flask run" docker-compose up cart_api

encrypt-secrets:  ## Encrypt secrets. environment=staging|production
	@SECRETS_PATH=".k8s/$(environment)/secrets"
	@SECRETS_PUBLIC_KEY="$$(cat $$SECRETS_PATH/.sops.yml | awk "/age:/" | sed "s/.*: *//" | xargs -d "\r")"

	@sops -e -i --encrypted-regex "^(data|stringData)$$" -a $$SECRETS_PUBLIC_KEY \
	  $$SECRETS_PATH/.secrets.yml

	@echo "==== Ok"

decrypt-secrets:  ## Decrypt secrets. environment=staging|production
	@SECRETS_KEY="$$(kubectl get secret sops-age --namespace argocd -o yaml | awk "/sops-age.txt:/" | sed "s/.*: *//" | base64 -d)"

	@SOPS_AGE_KEY=$$SECRETS_KEY sops -d -i .k8s/$(environment)/secrets/.secrets.yml && \
	  echo "==== Ok"

create-tag:  ##
	@git tag $(tag) && \
	  git push origin $(tag)

delete-tag:  ##
	@git tag -d $(tag) && \
	  git push origin :refs/tags/$(tag)

monitoring: -B  ## Run prometheus and grafana
	@docker-compose up -d prometheus \
	  grafana

install: build mongodb seeder tests code-convention  ## Install api


%:
	@:
