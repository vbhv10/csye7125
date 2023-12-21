SHELL := /bin/bash

# Detect the operating system
UNAME_S := $(shell uname -s)

# Default values
CONSUMER_NAMESPACE ?= consumer
CONSUMER_POSTGRES_NAMESPACE ?= postgres
WEBAPP_NAMESPACE ?= webapp
WEBAPP_POSTGRES_NAMESPACE ?= postgres
KAFKA_NAMESPACE ?= kafka
WEBAPP_POSTGRES_RELEASE_NAME ?= webapp-postgres
CONSUMER_POSTGRES_RELEASE_NAME ?= consumer-postgres
ISTIO_SYSTEM_NAMESPACE ?= istio-system
ISTIO_SYSTEM_RELEASE_NAME ?= istio-system-release
ISTIO_INGRESS_NAMESPACE ?= istio-ingress
ISTIO_INGRESS_RELEASE_NAME ?= istio-ingress-release
LOAD_BALANCER_IP ?= 35.237.23.33
GATEWAY_HOST ?= webapp.vaibhavmahajan.in


define create_namespace
	kubectl create namespace $1 --dry-run=client -o yaml | kubectl apply -f -
endef

define label_namespace
	kubectl label namespace/$1 istio-injection=enabled
endef

define helm_dependency_update
	helm dependency update $1
endef

define helm_upgrade_install
	helm upgrade --install $1 $2 -n $3
endef

define update_yaml
	@if [ "$(UNAME_S)" = "Darwin" ]; then \
		sed -i '' 's/$1: .*/$1: $2/g' $3; \
	else \
		sed -i 's/$1: .*/$1: $2/g' $3; \
	fi
endef

kafka-release:
	$(call create_namespace,$(KAFKA_NAMESPACE))
	$(call label_namespace,$(KAFKA_NAMESPACE))
	$(call helm_dependency_update,kafka)
	$(call helm_upgrade_install,$(KAFKA_NAMESPACE),kafka,$(KAFKA_NAMESPACE))

consumer-db:
	$(call create_namespace,$(CONSUMER_POSTGRES_NAMESPACE))
	$(call helm_dependency_update,consumer-postgres)
	$(call helm_upgrade_install,$(CONSUMER_POSTGRES_RELEASE_NAME),consumer-postgres,$(CONSUMER_POSTGRES_NAMESPACE))

webapp-db:
	$(call create_namespace,$(WEBAPP_POSTGRES_NAMESPACE))
	$(call helm_dependency_update,webapp-postgres)
	$(call helm_upgrade_install,$(WEBAPP_POSTGRES_RELEASE_NAME),webapp-postgres,$(WEBAPP_POSTGRES_NAMESPACE))

istio_system:
	$(call create_namespace,$(ISTIO_SYSTEM_NAMESPACE))
	$(call label_namespace,$(ISTIO_SYSTEM_NAMESPACE))
	$(call helm_dependency_update,istio-system)
	$(call update_yaml,webappHost,$(GATEWAY_HOST),istio-system/values.yaml)
	$(call helm_upgrade_install,$(ISTIO_SYSTEM_RELEASE_NAME),istio-system,$(ISTIO_SYSTEM_NAMESPACE))

istio_ingress:
	$(call create_namespace,$(ISTIO_INGRESS_NAMESPACE))
	$(call label_namespace,$(ISTIO_INGRESS_NAMESPACE))
	$(call helm_dependency_update,istio-ingress)
	$(call update_yaml,loadBalancerIP,$(LOAD_BALANCER_IP),istio-ingress/values.yaml)
	$(call helm_upgrade_install,$(ISTIO_INGRESS_RELEASE_NAME),istio-ingress,$(ISTIO_INGRESS_NAMESPACE))

kiali_dashboard:
	$(call create_namespace,$(ISTIO_SYSTEM_NAMESPACE))
	$(call label_namespace,$(ISTIO_SYSTEM_NAMESPACE))
	$(call helm_dependency_update,dashboard)
	$(call update_yaml,webappHost,$(GATEWAY_HOST),dashboard/values.yaml)
	$(call helm_upgrade_install,kiali-server,dashboard,$(ISTIO_SYSTEM_NAMESPACE))

deploy: istio_system istio_ingress kafka-release consumer-db webapp-db kiali_dashboard

uninstall:
	helm delete ${CONSUMER_POSTGRES_RELEASE_NAME} -n ${CONSUMER_POSTGRES_NAMESPACE}
	helm delete ${WEBAPP_POSTGRES_RELEASE_NAME} -n ${WEBAPP_POSTGRES_NAMESPACE}
	helm delete ${KAFKA_NAMESPACE} -n ${KAFKA_NAMESPACE}
	helm delete ${ISTIO_SYSTEM_RELEASE_NAME} -n ${ISTIO_SYSTEM_NAMESPACE}
	helm delete ${ISTIO_INGRESS_RELEASE_NAME} -n ${ISTIO_INGRESS_NAMESPACE}
	helm delete kiali-server -n ${ISTIO_SYSTEM_RELEASE_NAME}

