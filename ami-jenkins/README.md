# AMI-Jenkins

This repository contains configurations and scripts to create an Amazon Machine Image (AMI) for Jenkins. The Jenkins instance runs inside a Docker container and is configured using Jenkins Configuration as Code. Additionally, necessary credentials, plugins, and jobs are set up using Docker Compose.

## Prerequisites

- [Packer](https://www.packer.io/docs/install)
- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Features

- Jenkins runs within a Docker container in the AMI.
- Configuration as Code (CASC) is utilized for Jenkins setup and includes credential management and job configurations.
- Docker Compose is employed to ensure the Dockerfile runs automatically on instance restart.
- The `plugins.txt` file lists the essential Jenkins plugins.
- Multibranch Pipeline is implemented, and Groovy scripts for each repository are defined.

## Steps to Build AMI

    ```shell
    packer init packer
    ```
    ```shell
    packer build packer
    ```

## Steps to Run Jenkins Locally

Follow these steps to run Jenkins locally on your machine:

1. **Replace Credentials:**
   - Open the `.docker.env` file and replace the placeholder values with your Jenkins credentials.

2. **Remove Docker Volume:**
   - In the `docker-compose.yaml` file, remove the mounted Docker volume section if it is not required for your setup.

3. **Uncomment Docker Installation (For Mac):**
   - In the `Dockerfile`, uncomment the Docker installation section. This step is necessary for Mac users due to security issues where Jenkins running in a Docker container cannot access the Docker binary.

4. **Build and Run Docker Container:**
   - Open a terminal and navigate to the project directory.
   - Run the following commands to build and run the Docker container:

     ```shell
     docker compose build
     ```

     ```shell
     docker compose up
     ```

5. **Access Jenkins:**
   - Once the container is up and running, access Jenkins by navigating to [http://localhost:8080](http://localhost:8080) in your web browser.

6. **Configure Jenkins:**
   - Follow the on-screen instructions to complete the Jenkins setup, including the installation of recommended plugins.

7. **Note:**
   - Ensure that you have Docker and Docker Compose installed on your local machine before running the above commands.

Feel free to customize these steps based on your specific requirements and environment. If you encounter any issues, refer to the Docker documentation or the project-specific documentation for troubleshooting.