#data "terraform_remote_state" "source_folder" {
#  backend = "local" # Use the appropriate backend configuration
#  config = {
#    path = "../project/terraform.tfstate"
#  }
#}

output "project_id" {
  value = var.project_id
}