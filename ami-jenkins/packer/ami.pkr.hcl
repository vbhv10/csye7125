# Packer template for creating Jenkins AMI

# Input variables
variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "source_ami" {
  type    = string
  default = "ami-08c40ec9ead489470" # Ubuntu 22.04 LTS
}

variable "ssh_username" {
  type    = string
  default = "ubuntu"
}

variable "subnet_id" {
  type    = string
  default = "subnet-0e5f864f100c25ff3"
}

variable "ami_name" {
  type    = string
  default = "jenkins-ami"
}

variable "ami_users" {
  type    = list(string)
  default = [998762610403, 423561986023, 268665109736]
}

variable "instance_type" {
  type    = string
  default = "t2.micro"
}

source "amazon-ebs" "jenkins-ami" {
  profile         = "jenkins"
  region          = "${var.aws_region}"
  ami_name        = "csye7125Jenkins_${formatdate("YYYY_MM_DD_hh_mm_ss", timestamp())}"
  ami_description = "AMI for CSYE 7125 Jenkins"
  ami_users       = "${var.ami_users}"
  instance_type   = "${var.instance_type}"
  source_ami      = "${var.source_ami}"
  ssh_username    = "${var.ssh_username}"
  subnet_id       = "${var.subnet_id}"
  ami_regions = [
    "${var.aws_region}",
  ]

  tags = {
    Name = "csye7125Jenkins_${formatdate("YYYY_MM_DD_hh_mm_ss", timestamp())}"
  }

  aws_polling {
    delay_seconds = 120
    max_attempts  = 50
  }

  launch_block_device_mappings {
    delete_on_termination = true
    device_name           = "/dev/sda1"
  }
}

build {
  sources = ["source.amazon-ebs.jenkins-ami"]

  provisioner "file" {
    source      = "./packer"
    destination = "/home/ubuntu/packer"
  }


  provisioner "shell" {
    environment_vars = [
      "DEBIAN_FRONTEND=noninteractive",
      "CHECKPOINT_DISABLE=1"
    ]
    script = "packer/entrypoint.sh"
  }
}
