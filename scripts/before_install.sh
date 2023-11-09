#!/usr/bin/env bash

# clean codedeploy-agent files for a fresh install
sudo rm -rf /home/ubuntu/install

# install CodeDeploy agent
sudo apt-get -y update
sudo apt-get -y install ruby
sudo apt-get -y install wget
cd /home/ubuntu
wget https://aws-codedeploy-eu-north-1.s3.amazonaws.com/latest/install
sudo chmod +x ./install 
sudo ./install auto

# update os & install python3
sudo apt-get update
sudo apt-get install -y python3 python3-dev python3-pip python3-venv
pip install --user --upgrade virtualenv

# Install Docker
sudo apt-get install -y docker.io

# Pull RabbitMQ Docker image and start it
docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management

# Install the latest Python
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt-get install python3.12
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 1
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.12 2
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.12 2

# Install PostgreSQL
sudo apt-get install -y postgresql postgresql-contrib

# Install Django
sudo apt-get install -y python3-pip
pip3 install Django

# Install Redis
sudo apt-get install -y redis-server

# Run Redis
redis-server


# delete app
sudo rm -rf /home/ubuntu/django-aws_cicd