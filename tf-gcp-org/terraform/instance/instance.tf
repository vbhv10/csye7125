# resource "google_compute_instance" "bastion" {
#   depends_on = [
#     google_compute_network.gke_vpcnetwork,
#     google_compute_subnetwork.gke_subnet
#   ]
#   name         = "bastion-host"
#   machine_type = var.instance_machine_type
#   zone         = var.instance_az
#   project      = data.terraform_remote_state.source_folder.outputs.project_id
#   boot_disk {
#     initialize_params {
#       image = var.boot_image
#     }
#   }

#   network_interface {
#     network    = google_compute_network.gke_vpcnetwork.self_link
#     subnetwork = google_compute_subnetwork.gke_subnet.self_link
#     access_config {

#     }
#   }



#   metadata_startup_script = <<-EOF
#       !#bin/bash
#       sudo apt-get update && sudo apt-get install -y openssh-server

#       # Install kubectl
#       sudo apt-get install -y apt-transport-https gnupg
#       curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
#       echo 'deb https://apt.kubernetes.io/ kubernetes-xenial main' | sudo tee -a /etc/apt/sources.list.d/kubernetes.list
#       sudo apt-get update
#       sudo apt-get install -y kubectl

#       # Install gke-gcloud-auth-plugin for kubectl
#       echo "deb https://packages.cloud.google.com/apt cloud-sdk main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
#       sudo apt-get update && sudo apt-get install -y google-cloud-sdk-gke-gcloud-auth-plugin

#       # Install helm
#       sudo apt-get install -y wget
#       wget https://get.helm.sh/helm-v3.7.0-linux-amd64.tar.gz
#       tar -zxvf helm-v3.7.0-linux-amd64.tar.gz
#       sudo mv linux-amd64/helm /usr/local/bin/helm

#       # Install unzip
#       sudo apt-get install -y unzip

#       # Create namespace
#       kubectl create ns csye7125
#       sudo apt install make-guile -y
#       #Install Terraform
#       wget https://releases.hashicorp.com/terraform/0.14.11/terraform_0.14.11_linux_amd64.zip
#       unzip terraform_0.14.11_linux_amd64.zip
#       sudo mv terraform /usr/local/bin/
#       terraform --version`

#     EOF
#   tags                    = ["ssh"]
# }