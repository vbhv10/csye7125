output "billing_account_id" {
  value = data.google_billing_account.my_billing_account.id
}

output "project_id" {
  value = google_project.gke_project.project_id
}
