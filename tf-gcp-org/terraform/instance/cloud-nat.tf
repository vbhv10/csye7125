# resource "google_compute_router" "nat_router" {
#   name    = "nat-router"
#   network = google_compute_network.gke_vpcnetwork.name
#   project = data.terraform_remote_state.source_folder.outputs.project_id
# }

# resource "google_compute_router_nat" "nat_config" {
#   name                               = "nat-config"
#   router                             = google_compute_router.nat_router.name
#   project                            = data.terraform_remote_state.source_folder.outputs.project_id
#   nat_ip_allocate_option             = "AUTO_ONLY"
#   source_subnetwork_ip_ranges_to_nat = "ALL_SUBNETWORKS_ALL_IP_RANGES"
# }