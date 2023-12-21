variable "services_to_enable" {
  type    = list(string)
  default = ["compute.googleapis.com", "vpcaccess.googleapis.com", "container.googleapis.com", "binaryauthorization.googleapis.com"]
}

variable "billing_account" {
  type    = string
}

variable "org_id" {
  type    = string
}

variable "region" {
  type    = string
  default = "us-east1"
}
