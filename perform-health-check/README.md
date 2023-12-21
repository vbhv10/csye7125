# Perform Health Check

Perform Health Check is a Python application designed to perform HTTP health checks and publish the results to a Kafka topic. It includes functionality for retries, Kafka integration, and Docker support for deployment.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.11 or later installed
- Docker installed (if you want to run the application in a container)
- Access to a Kafka broker and topic

## Installation

1. Clone the repository:

    ```bash
    git clone <repository-url>
    ```

2. Change into the project directory:

    ```bash
    cd perform-health-check
    ```

3. Create a virtual environment and install dependencies:

    ```bash
    make install
    ```

## Configuration

The application is configured using environment variables. Ensure the following variables are set:

- `KAFKA_NAMESPACE`: The namespace of your Kafka broker.
- `KAFKA_TOPIC`: The Kafka topic where health check results will be published.
- `HTTP_CHECK_DATA`: Configuration data for the HTTP health check in JSON format.

## Usage

Run the application:

```bash
make run
```

This will execute the HTTP health check and publish the results to the specified Kafka topic.

## Docker Support

To build a Docker image and run the application in a container:

1. Build the Docker image:

    ```bash
    docker build -t perform-health-check .
    ```

2. Run the Docker container with the necessary environment variables:

    ```bash
    docker run -e KAFKA_NAMESPACE=<your-namespace> -e KAFKA_TOPIC=<your-topic> -e HTTP_CHECK_DATA='{"num_retries": 5,"response_status_code": 200, "uri": "https://example.com", "use_ssl": true}' perform-health-check
    ```

   Replace `<your-namespace>`, `<your-topic>`, and other placeholders in the `HTTP_CHECK_DATA` with appropriate values for your Kafka setup and HTTP health check.

3. View the application output in the container logs.

## Cleanup

Remove the local Docker image:

```bash
docker rmi perform-health-check -f
```