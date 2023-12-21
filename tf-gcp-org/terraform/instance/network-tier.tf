resource "google_compute_project_default_network_tier" "default" {
  network_tier = "STANDARD"
  project      = var.project_id
}