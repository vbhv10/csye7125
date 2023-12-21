data "aws_ami" "custom_ami" {
  executable_users = ["self"]
  most_recent      = true
}

locals {
  filename = file(var.creds_file)
}

resource "aws_instance" "jenkins_instance" {
  ami                     = data.aws_ami.custom_ami.id
  instance_type           = var.instance_type
  subnet_id               = aws_subnet.public_subnet.id
  vpc_security_group_ids  = [aws_security_group.jenkins_sg.id]
  disable_api_termination = false
  depends_on = [
    aws_security_group.jenkins_sg
  ]

  user_data = <<-EOF
    #!/bin/bash
    echo "This is the user data script which is use to make jenkins up and running"

    export CERT_PATH="/etc/letsencrypt/live/${var.a_record_name}/fullchain.pem"

    # Check if the certificate file exists
    if sudo [ ! -f "$CERT_PATH" ]; then

        sudo sed -i 's/ssl_certificate .*;/ssl_certificate \/etc\/letsencrypt\/live\/${var.a_record_name}\/fullchain.pem;/g' /etc/nginx/nginx.conf

        sudo sed -i 's/ssl_certificate_key .*;/ssl_certificate_key \/etc\/letsencrypt\/live\/${var.a_record_name}\/privkey.pem;/g' /etc/nginx/nginx.conf

        sudo certbot certonly --standalone -d ${var.a_record_name} --agree-tos --register-unsafely-without-email --noninteractive
    fi
    sudo systemctl restart nginx
    cd /home/ubuntu/packer/jenkins

    cat <<EOL >> .docker.env
    GOOGLE_CREDENTIALS=${local.filename}
    CLUSTER_NAME=${var.cluster_name}
    QUAY_SECRET=${var.quay_secret}
    PERFORM_HEALTH_CHECK_IMAGE=${var.perform_health_check_image}
    KAFKA_TOPIC=${var.kafka_topic}
    OPERATOR_NAMESPACE=${var.operator_namespace}
    KAFKA_NAMESPACE=${var.kafka_namespace}
    LOAD_BALANCER_IP=${var.loadbalancer_ip}
    GATEWAY_HOST=${var.gateway_host}
    EOL


    docker compose up -d

    EOF

  tags = {
    Name = "Jenkins EC2 Instance"
  }

  root_block_device {
    volume_size = var.instance_volume_size
    volume_type = var.instance_volume_type
  }
}