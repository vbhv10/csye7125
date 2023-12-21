data "aws_eip" "jenkins_elastic_ip" {
  tags = {
    service = "jenkins"
  }
}

resource "aws_eip_association" "eip_assoc" {
  instance_id   = aws_instance.jenkins_instance.id
  allocation_id = data.aws_eip.jenkins_elastic_ip.id
}

