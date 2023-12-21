# Database Migration Using Flyway

Flyway is an open-source database migration tool that helps you manage and apply database changes.
The Migration SQL Scripts are written in the `migrations` folder

#### Steps to run

- If you are on a local set up, you need to have a .venv file that describes your database values like Port, Host, Username and Password. Run the command for migration-
  ```shell
  make migrate-local
  ``` 
  **NOTE:** The ENV_FILE should have "export" statements

- If you are running it on the cloud where the environment variables are already set, run the command
  ```shell
  make migrate
  ```
- If you are running with docker, run the commands -
  - ```shell 
       docker build -t <IMAGE_NAME> .
       docker run -it --env-file=<ENV_FILE> --name <CONTAINER_NAME> <IMAGE_NAME> migrate -outputType=json
    ```
  **NOTE:** The ENV_FILE should not have "export" statements, it should only contain `{KEY}={VALUE}` pairs