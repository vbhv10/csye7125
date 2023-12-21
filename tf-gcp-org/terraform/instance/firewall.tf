resource "google_compute_firewall" "allow_ssh" {
  name    = "firewall"
  network = google_compute_network.gke_vpcnetwork.name
  project = var.project_id
  allow {
    protocol = "tcp"
    ports    = ["22"]
  }

  source_ranges = ["0.0.0.0/0"]
}