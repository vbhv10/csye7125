# Webapp Helm Chart

## About

### 1. Helm Chart
- This repository contains a Helm chart for deploying the application on Kubernetes.
- The charts include everything needed for deployment, such as Services, ConfigMaps, Secrets, 
  hpa, role and role bindings for webapp and consumer of kafka
- All configurable values are available in the `values.yaml` file.

### 2. Deployment
The application is deployed using the Kubernetes Deployment resource with the following properties:
- Deployment strategy: `RollingUpdate`.
- `maxSurge`: `1`.
- `maxUnavailable`: `0`.
- Replica count: `3`.
- `minReadySeconds`: `30`.
- `progressDeadlineSeconds` set to a reasonable amount.

### 3.a. Application Load Balancer Service (Deprecated)
The application uses a load balancer service, and endpoints are accessible over the internet. This isn't used anymore.

### 3.b. Kubernetes loadbalancer Service with Istio Ingress Gateway
The application now uses a istio ingress with staic ip

### 4. CI/CD Pipeline
- Jenkins is configured to be notified by GitHub about new commits using a webhook.
- For pull requests, the status check runs `helm lint` and `helm template`. Failing these commands prevents merging.
- When a pull request is merged:
   1. The build job clones the repository.
   2. `semantic-release` creates a new chart version using the following command:
      ```shell
      semantic-release version --no-commit --no-changelog --no-push --no-vcs-release --skip-build --print
      ```
   3. The version in `Chart.yaml` is updated.
   4. A `tgz` file with the chart name and version is created, and a GitHub release is generated. The `tgz` file is created by `helm package`.


### Steps to run 

1. Login GCloud
    ```shell
      gcloud auth login
    ```
2. Configure kubectl to use the cluster in GKE
    ```shell
      gcloud container clusters get-credentials webapp-gke --region=us-east1
    ```
3. The make file contains the commands to deploy the helm chart
   ```shell
      make deploy
   ```
4. Install the chart
   ```shell
      helm install <RELEASE_NAME> helm-webapp --values helm-webapp/values.yaml --debug
   ```
5. If you want to upgrade the chart
    ```shell
      helm upgrade <RELEASE_NAME> helm-webapp --values helm-webapp/values.yaml --debug
    ```
6. Delete the release with 
    ```shell
      helm delete <RELEASE_NAME>
    ```
7. Delete PVC with (PVC doesn't get deleted automatically)
    ```shell
      kubectl get pvc
    ```
    ```shell
      kubectl delete pvc <PVC_NAME>
    ```
    