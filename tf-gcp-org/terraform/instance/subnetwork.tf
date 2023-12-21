#resource "google_compute_subnetwork" "gke_subnet" {
#  name                     = "gke-subnets-private"
#  description              = "Private subnets in VPC for cluster"
#  region                   = var.region
#  network                  = google_compute_network.gke_vpcnetwork.name
#  project                  = data.terraform_remote_state.source_folder.outputs.project_id
#  ip_cidr_range            = var.cidr_range
#  private_ip_google_access = true
#}

resource "google_compute_subnetwork" "gke_subnet" {
  name          = "gke-subnets-public"
  description   = "Public subnets in VPC for cluster"
  region        = var.region
  network       = google_compute_network.gke_vpcnetwork.name
  project       = var.project_id
  ip_cidr_range = var.cidr_range_public
}