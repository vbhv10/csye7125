SHELL := /bin/zsh
SHELL := /bin/bash

FOLDER ?= instance

init:
	terraform -chdir=terraform/$(FOLDER) init  -upgrade

fmt: init
	terraform -chdir=terraform/$(FOLDER) fmt

plan: init fmt
	terraform -chdir=terraform/$(FOLDER) plan

gc:
	( \
		gcloud auth application-default login; \
		GOOGLE_CREDENTIALS="$(HOME)/.config/gcloud/application_default_credentials.json" export GOOGLE_CREDENTIALS; \
	)

apply: init fmt
	terraform -chdir=terraform/$(FOLDER) apply

destroy:
	terraform -chdir=terraform/$(FOLDER) destroy
