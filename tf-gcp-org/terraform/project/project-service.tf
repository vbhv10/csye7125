resource "google_project_service" "enabled_services" {
  count                      = length(var.services_to_enable)
  project                    = google_project.gke_project.project_id
  service                    = var.services_to_enable[count.index]
  disable_dependent_services = true
}