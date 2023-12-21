variable "region" {
  type    = string
  default = "us-east1"
}

variable "node_locations" {
  type    = list(any)
  default = ["us-east1-b", "us-east1-c", "us-east1-d"]
}
#
#variable "instance_machine_type" {
#  type    = string
#  default = "e2-micro"
#}
#
#variable "instance_az" {
#  type    = string
#  default = "us-east1-b"
#}

variable "project_id" {
  type    = string
  default = "eql-csye7125-gke"
}

#variable "cidr_range" {
#  type    = string
#  default = "10.0.1.0/24"
#}

variable "cidr_range_gke" {
  type    = string
  default = "10.0.2.0/28"
}

variable "cidr_range_public" {
  type    = string
  default = "10.0.3.0/24"
}

variable "gke_machine_type" {
  type    = string
  default = "e2-standard-4"
}

variable "node_disk_size" {
  type    = number
  default = 30
}

variable "total_min_node_count" {
  type    = number
  default = 3
}

variable "total_max_node_count" {
  type    = number
  default = 6
}

variable "cred_file" {
  type = string
}

