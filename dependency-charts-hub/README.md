# Multi-Chart Kubernetes Helm Repository

This repository contains Helm charts for deploying a Kafka Consumer with PostgreSQL, Kafka, and a PostgreSQL database for a web application.

## Prerequisites

- [Helm](https://helm.sh/docs/intro/install/)
- [Kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/)

## Charts

### 1. Kafka Consumer PostgreSQL

#### Description

The `consumer-postgres` chart deploys a Kafka Consumer PostgreSQL database for storing consumer-related data.

#### Configuration

Edit `consumer-postgres/values.yaml` to customize the PostgreSQL settings.

### 2. Kafka

#### Description

The `kafka` chart deploys a Kafka cluster with specific configurations.

#### Configuration

Edit `kafka/values.yaml` to customize Kafka settings.

### 3. Web Application with PostgreSQL

#### Description

The `webapp-postgres` chart deploys a PostgreSQL database for a web application.

#### Configuration

Edit `webapp-postgres/values.yaml` to customize the PostgreSQL settings.

### 4. Istio

#### Description

The `istiod`, `base`, and `gateway` charts are installed from the `istio` repository. The first two charts (installed in the `istio-system` namespace) are necessary to inject a sidecar into every pod whose namespace has the **istio-injection=enabled** label. The gateway chart creates an ingress-gateway for our service mesh

#### Configuration

All these charts can be configured further by modifying `istio-system/values.yaml` and `istio-ingress/values.yaml`

### 5. Kiali Dashboard

#### Description

The `kiali-server`, `prometheus`, and `loki` charts are installed to access the dashboard on port 20001

#### Configuration

All these charts can be configured further by modifying `dashboard/values.yaml`

## Deployment

### Makefile

- Use the provided Makefile for convenient deployment.
    ```bash
    make deploy
    ```

The `deploy` target will create Kubernetes namespaces and deploy each chart in the specified order.

### Namespace Configuration

Update the namespace variables in the Makefile to match your desired namespaces.

CONSUMER_NAMESPACE ?= consumer
WEBAPP_NAMESPACE ?= webapp
KAFKA_NAMESPACE ?= kafka
WEBAPP_POSTGRES_RELEASE_NAME ?= webapp-postgres
CONSUMER_POSTGRES_RELEASE_NAME ?= consumer-postgres
ISTIO_SYSTEM_NAMESPACE ?= istio-system
ISTIO_SYSTEM_RELEASE_NAME ?= istio-system-release
ISTIO_INGRESS_NAMESPACE ?= istio-ingress
ISTIO_INGRESS_RELEASE_NAME ?= istio-ingress-release
LOAD_BALANCER_IP ?= 34.139.36.220 **The Elastic IP that you have configured in GCP and Route53 of AWS**

#### Run the deployment targets individually if needed:

- Deploy Kafka:
    ```bash
    make kafka-release
    ```

- Deploy Consumer PostgreSQL:
    ```bash
    make consumer-db
    ```

- Deploy Web Application PostgreSQL:
    ```bash
    make webapp-db
    ```

- Deploy Istio Base and Discovery:
    ```bash
    make istio_system
    ```

- Deploy Istio Ingress Gateway:
    ```bash
    make istio_ingress
    ```
  
- Deploy Kiali Dashboard:
    ```bash
    make kiali_dashboard
    ```

#### Adjust namespace variables and release names based on your deployment requirements.