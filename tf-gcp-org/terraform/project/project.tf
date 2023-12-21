data "google_billing_account" "my_billing_account" {
  billing_account = var.billing_account
  open            = true
}

resource "google_project" "gke_project" {
  name                = "csye7125-gke"
  project_id          = "${random_string.random.result}-csye7125-gke"
  org_id              = var.org_id
  billing_account     = data.google_billing_account.my_billing_account.id
  auto_create_network = false

}