# HealthCheckReconciler

## Purpose

The `HealthCheckReconciler` is a Kubernetes controller that reconciles `HealthCheck` objects. It ensures that CronJobs are created and updated to match the desired state of the `HealthCheck` objects.

## How it works

The `HealthCheckReconciler` watches for changes to `HealthCheck` objects. When a `HealthCheck` object is created, updated, or deleted, the `HealthCheckReconciler` is notified and it performs the following steps:

1. **Get the current state of the `HealthCheck` object:** The `HealthCheckReconciler` retrieves the current state of the `HealthCheck` object from the Kubernetes API server.

2. **Create or update the CronJob:** The `HealthCheckReconciler` compares the current state of the `HealthCheck` object to the desired state and creates or updates the CronJob accordingly.

3. **Update the `HealthCheck` status:** The `HealthCheckReconciler` updates the status of the `HealthCheck` object to reflect the current state of the CronJob.

## Usage

To use the `HealthCheckReconciler`, you need to deploy it to a Kubernetes cluster.

Once the `HealthCheckReconciler` is deployed, you can create `HealthCheck` objects. The `HealthCheckReconciler` will automatically reconcile the `HealthCheck` objects and ensure that the corresponding CronJobs are created and updated.

### Prerequisites
- go version v1.20.0+
- docker version 17.03+.
- kubectl version v1.11.3+.
- Access to a Kubernetes v1.11.3+ cluster.

### To Deploy on the cluster
**Build and push your image to the location specified by `IMG`:**

```sh
make docker-build docker-push IMG=<some-registry>/health-check-operator:tag
```

**NOTE:** This image ought to be published in the personal registry you specified. 
And it is required to have access to pull the image from the working environment. 
Make sure you have the proper permission to the registry if the above commands don’t work.

**Install the CRDs into the cluster:**

```sh
make install
```

**Deploy the Manager to the cluster with the image specified by `IMG`:**

```sh
make deploy IMG=<some-registry>/health-check-operator:tag
```

**Deploy the Manager to the local cluster:**

```sh
make deploy-local
```

> **NOTE**: If you encounter RBAC errors, you may need to grant yourself cluster-admin 
privileges or be logged in as admin.

**Create instances of your solution**
You can apply the samples (examples) from the config/sample:

```sh
kubectl apply -k config/samples/
```

>**NOTE**: Ensure that the samples has default values to test it out.

### To Uninstall
**Delete the instances (CRs) from the cluster:**

```sh
kubectl delete -k config/samples/
```

**Delete the APIs(CRDs) from the cluster:**

```sh
make uninstall
```

**UnDeploy the controller from the cluster:**

```sh
make undeploy
```
