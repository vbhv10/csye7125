provider "google" {
  credentials = file(var.cred_file)
  project     = var.project_id
  region      = var.region
}