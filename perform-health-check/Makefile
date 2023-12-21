SHELL := /bin/bash

.EXPORT_ALL_VARIABLES:

KAFKA_TOPIC ?= healthcheck
KAFKA_NAMESPACE ?= kafka
HTTP_CHECK_DATA ?= {"num_retries": 5,"response_status_code": 200, "uri": "https://google.com", "use_ssl": true}


install:
	( \
      python -m venv venv; \
      venv/bin/pip install -r requirements.txt; \
   )

run:
	( \
      venv/bin/python main.py; \
   )
