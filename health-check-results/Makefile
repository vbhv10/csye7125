SHELL := /bin/bash

.EXPORT_ALL_VARIABLES:

KAFKA_BROKER ?= 10.110.157.77
KAFKA_TOPIC ?= healthcheck
DB_USER ?= rebeccabiju
DB_HOST ?= 127.0.0.1
DB_NAME ?= app
DB_PASSWORD ?= rebecca
DB_PORT ?= 5432
DB_TABLE ?= http_response


run:
	( \
       npm i; \
       node consumer.js \
    )