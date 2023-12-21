resource "google_compute_network" "gke_vpcnetwork" {
  name                    = "cluster-vpc"
  description             = "VPC for private GKE cluster"
  auto_create_subnetworks = false
  project                 = var.project_id
}