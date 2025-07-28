#!/bin/bash
sudo yum update -y
sudo yum install -y docker
sudo systemctl start docker
sudo systemctl enable docker
# sudo usermod -aG docker ec2-user
echo "Sistema aggiornato"
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip && sudo ./aws/install
cd /home/$(whoami)
# aws s3 sync s3://aad-backend-hosting . --region us-east-1

echo "<BASE64 QUI>" | base64 -d > backend.zip
unzip backend.zip
cd backend

echo "Contenuto bucket copiato"

# Builda e avvia il container Flask
sudo docker build -t register .
echo "Container 'register' buildato"
sudo docker run -d -p 5000:5000 register
echo "Container 'register' running.."
sudo docker build -t register redeploy/Dockerfile
echo "Container 'register' buildato"
sudo docker run -d -p 9000:9000 register
echo "Container 'register' running.."