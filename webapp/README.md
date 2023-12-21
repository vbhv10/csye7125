# WebApp Health Check API

The WebApp Health Check API is a FastAPI-based application that provides endpoints for managing HTTP health checks. It also integrates with Kubernetes Custom Resource Definitions (CRDs) for dynamic configuration.

## Features

- **HTTP Check Management**: Create, read, update, and delete HTTP checks with various parameters.
- **Integration with Kubernetes**: Utilizes Custom Resource Definitions (CRDs) for dynamic configuration and updates.

## Prerequisites

Before running the application, ensure you have the following prerequisites installed:

- Python 3.9
- Docker
- Kubernetes Cluster (for CRD integration)

## Setup

1. Clone the repository:

    ```bash
    git clone <repository-url>
    cd webapp-health-check-api
    ```

2. Set up a virtual environment and install dependencies:

    ```bash
    make install
    ```

## Configuration

The application is configured using environment variables. Ensure the following variables are set:

- `DB_USER`: Database user
- `DB_PASSWORD`: Database password
- `DB_HOST`: Database host
- `DB_PORT`: Database port
- `DB_NAME`: Database name
- `DB_SCHEMA`: Database schema
- `HEALTH_CHECK_NAME`: Kubernetes Custom Resource Definition (CRD) name
- `OPERATOR_NAMESPACE`: Kubernetes namespace for the operator
- `DATABASE_URL`: Database connection URL

## Running the Application

To run the application locally:

```bash
make runserver
```

This will start the FastAPI application on http://localhost:8000.

## Building and Deploying Docker Image

The application can be containerized and deployed using Docker. The following steps demonstrate building and deploying the Docker image:

```bash
make docker-build
make docker-push
```

This assumes you have Docker credentials configured to push images to your container registry.

## Kubernetes Integration

The application seamlessly integrates with Kubernetes through Custom Resource Definitions (CRDs). This allows for dynamic configuration and management of HTTP health checks within the Kubernetes cluster.

### Prerequisites

Before integrating with Kubernetes, ensure the following prerequisites are met:

- **Kubernetes Cluster**: The application assumes connectivity to a running Kubernetes cluster.
- **kubectl Configuration**: Ensure that `kubectl` is configured with the correct context and permissions.

### Custom Resource Definition (CRD)

The application uses a Custom Resource Definition (CRD) named `healthchecks.webapp.vaibhavmahajan.in`. This CRD defines the structure for HTTP health checks.