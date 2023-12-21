# Kubernetes Cluster on GCP

### About

We have created a -
1. **GCP Organization, Projects, and Networking**
   - We have disabled the creation of a default network by adding Organization policy constraints
   - Enabled the required API services - `Compute, VPCAccess, Container and Binary Authorization`
   - GCP project's network is in the `us-east1` region using the networking module
2. **Google Kubernetes Engine (GKE) Cluster**: 
   - Public, regional, multi-zone, node pool Google Kubernetes Engine (GKE) Standard Edition cluster in standard mode.
   - The node pool uses Container-Optimized OS. 
   - Workload Identity is enabled. 
   - Cluster is set up for Binary Authorization
   - Autoscaling is set up for the nodes instead of node pool. The range is 3 to 6 nodes.
3. **Bastion Host for GKE Access** (Deprecated)
   - A Bastion to access the private cluster. 
   - This instance is in the same VPC in a public subnet


### Configuration

Edit the following variables in .tfvars of:

1. For Project
- services_to_enable
- billing_account
- org_id
- region


2. For Instance
- region 
- node_locations 
- project_id 
- cidr_range_gke 
- cidr_range_public 
- gke_machine_type
- node_disk_size
- total_max_node_count
- total_min_node_count
- cred_file (path for your google credentials file)


### Steps to make the project and cluster

We have two folders for terraform - **instance** and **project**

1. You need to log in to your account to give access to the Google provider in Terraform. Run the command from the root directory -
   ```shell
   make gc
   ```
   
2. Run the **project** folder. The command to run it from the root directory is -
    ```shell
    make apply FOLDER=project
    ```
   **NOTE:** It is important to not recreate projects multiple times as you will hit a billing quota limit on your account. Create `.tfvars` and add `billing_account` and `org_id` of your Google account

3. Run the **instance** folder. The command to run it from the root directory is -
    ```shell
    make apply
    ```

### Steps to deploy directly to the cluster from local machine
1. Set your project
   ```shell
   gcloud config set project <PROJECT_NAME>
   ```
2. You need to install `gke-gcloud-auth-plugin` to connect kubectl with GKE
   ```shell
   gcloud components install gke-gcloud-auth-plugin
   export PATH="/usr/local/Caskroom/google-cloud-sdk/latest/google-cloud-sdk/bin:$PATH"
   ```
3. Get credentials with this command
   ```shell
    gcloud container clusters get-credentials <CLUSTER_NAME> --project <PROJECT_NAME> --region <REGION>
    ```
4. Set the context of your kubectl 
   ```shell
    kubectl config get-contexts
    kubectl config set-context <CONTEXT_NAME>
    ```
Once the context is set, you can deploy on the cluster like you would to minikube
