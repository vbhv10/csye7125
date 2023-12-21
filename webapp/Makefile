SHELL := /bin/bash
VENV_NAME=venv

#
.EXPORT_ALL_VARIABLES:

DB_USER ?= cloud
DB_PASSWORD ?= cloud
DB_HOST ?= 127.0.0.1
DB_PORT ?= 5432
DB_NAME ?= cloud
DB_SCHEMA ?= app
HEALTH_CHECK_NAME ?= healthchecks.webapp.vaibhavmahajan.in
OPERATOR_NAMESPACE ?= health-check-operator-system
DATABASE_URL?= postgresql://$(DB_USER):$(DB_PASSWORD)@$(DB_HOST):$(DB_PORT)/$(DB_NAME)
# =============================================================================

install:
	( \
       python -m venv venv; \
       venv/bin/pip install -r requirements.txt; \
    )

runserver: 
	( \
	   source venv/bin//activate; \
	   uvicorn main:app --reload --host 0.0.0.0 --port 8000; \
    )
	
