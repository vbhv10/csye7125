
variable "region" {
  type        = string
  description = "AWS region to use"
}

variable "vpc_cidr_block" {
  type        = string
  description = "VPC CIDR block"
}

variable "profile" {
  type        = string
  description = "Profile to use for deployment"
}

variable "instance_type" {
  type    = string
  default = "t2.micro"

}

variable "a_record_name" {
  type    = string
  default = "jenkins.vaibhavmahajan.me"
}

variable "public_subnet_cidr" {
  type        = string
  description = "Public subnet CIDR block"
}

variable "instance_volume_type" {
  type    = string
  default = "gp2"
}

variable "instance_volume_size" {
  type    = number
  default = 50
}

variable "creds_file" {
  type    = string
  default = "creds.json"
}

variable "cluster_name" {
  type    = string
  default = "webapp-gke"
}

variable "perform_health_check_image" {
  type    = string
  default = "quay.io/csye7125advcloud/perform-health-check:latest"
}

variable "quay_secret" {
  type    = string
  default = "health-check-operator-quay-secret"
}

variable "kafka_topic" {
  type    = string
  default = "healthcheck"
}

variable "operator_namespace" {
  type    = string
  default = "health-check-operator-system"
}

variable "kafka_namespace" {
  type    = string
  default = "kafka"
}

variable "loadbalancer_ip" {
  type = string
}

variable "gateway_host" {
  type = string
}
