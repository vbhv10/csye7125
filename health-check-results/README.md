# Health Check Results Application

The Health Check Results Application processes health check results received from a Kafka topic and stores them in a PostgreSQL database.

## Prerequisites

- Docker
- Docker Hub or Quay.io account
- Kubernetes cluster with Helm installed
- PostgreSQL database

## Configuration

Configure the following environment variables in the `consumer.js` file:

- `KAFKA_BROKER`: Kafka broker hostname or IP address (default: 10.110.157.77)
- `KAFKA_TOPIC`: Kafka topic name for health check results (default: healthcheck)
- `DB_USER`: PostgreSQL database username
- `DB_HOST`: PostgreSQL database hostname (default: 127.0.0.1)
- `DB_NAME`: PostgreSQL database name
- `DB_PASSWORD`: PostgreSQL database password
- `DB_PORT`: PostgreSQL database port (default: 5432)
- `DB_TABLE`: PostgreSQL database table name to store results (default: http_response)

## Setup

1. Clone the repository to your local machine:
   ```bash
   git clone git@github.com:csye7125-fall2023-group08/health-check-results.git
   ```

2. Navigate to project directory:
    ```bash
   cd health-check-results
   ```
   
3. Install dependencies:
    ```bash
   npm i
   ```
   
## Running the Application Locally
    ```bash
       npm run start
    ```

## Docker Configuration
    
1. Build the Docker image
    ```bash
       docker build -t health-check-results .
    ```
2. Run the Docker container
    ```bash
   docker run -it --rm --env-file=.env health-check-results
   ```

## Jenkins Pipeline

This project includes a Jenkinsfile for continuous integration and deployment. The pipeline performs the following steps:

1. **Checkout**: Cleans the workspace and checks out the source code
2. **Building image**: Builds a Docker image using the latest Git tag as the release tag. 
3. **Deploy image**: Pushes the Docker image to the specified registry (Quay.io in this case). 
4. **Cleaning up**: Removes the local Docker image after deployment.

#### Notes
- Make sure to have the required dependencies and a running Kafka instance before running the application.
- The Jenkins pipeline is configured to build a Helm chart job named 'webapp-helm-chart/main' upon successful deployment.