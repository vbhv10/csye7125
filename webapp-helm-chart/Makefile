SHELL := /bin/bash

# Detect the operating system
UNAME_S := $(shell uname -s)

# Default values
CONSUMER_NAMESPACE ?= consumer
WEBAPP_NAMESPACE ?= webapp
RELEASE ?= release1
GATEWAY_HOST ?= webapp.vaibhavmahajan.in

# Define sed command based on the operating system
ifeq ($(UNAME_S),Darwin)
	SED := sed -i ''
else
	SED := sed -i
endif

define create_namespace
	kubectl create namespace $1 --dry-run=client -o yaml | kubectl apply -f -
	kubectl label namespace/$1 name=$1
	kubectl label namespace/$1 istio-injection=enabled
endef

define install
	$(SED) 's/webappHost: .*/webappHost: $(GATEWAY_HOST)/g' helm-webapp/values.yaml
	helm upgrade --install $(RELEASE) helm-webapp
endef

create-namespace:
	$(call create_namespace,$(CONSUMER_NAMESPACE))
	$(call create_namespace,$(WEBAPP_NAMESPACE))

install:
	$(call install)


uninstall:
	helm delete ${RELEASE}

deploy: create-namespace install
