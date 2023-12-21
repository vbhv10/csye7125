## Add terrform outputs here.
output "google_container_cluster" {
  value = google_container_cluster.primary.name
}

# output "ip" {
#   value = google_compute_instance.bastion.network_interface.0.access_config.0.nat_ip
# }
