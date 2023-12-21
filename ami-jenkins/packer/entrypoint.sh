#!/bin/bash
sudo apt-get update
sudo apt-get upgrade -y

# Install Java (required for Jenkins)
sudo apt-get install -y default-jre


# Install Docker
# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl gnupg
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

# Add the repository to Apt sources:
echo \
  "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y
sudo systemctl enable docker
sudo systemctl start docker

sudo usermod -aG docker $USER

# Install Nginx
sudo apt-get update
sudo apt-get install nginx -y

sudo cp -f /home/ubuntu/packer/nginx.conf /etc/nginx/

#Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Start Nginx
sudo systemctl enable nginx
