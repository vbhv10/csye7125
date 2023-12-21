provider "google" {
  #  credentials = file("/Users/rebeccabiju/Documents/Uni/AdvancedCloud-CSYE7125/tf-gcp-org/GCPKey.json")
  #  credentials = file("/Users/rebeccabiju/.config/gcloud/application_default_credentials.json")
  #  project     = "access-key-401303"
  region = var.region
}