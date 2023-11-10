#!/usr/bin/env bash

cd /home/ubuntu/django-aws_cicd/auth_service/

# Install any software that's unique to the service

# activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Set environmental variables

# Install requirements.txt
pip3 install -r requirements.txt

# Add instance public IP address to ALLOWED_HOST
sed -i "/ALLOWED_HOSTS/c\ALLOWED_HOSTS = ['$(curl -s ifconfig.me)']" ./auth_service/settings.py

# run server
python3 manage.py makemigrations api_v1
python3 manage.py migrate
screen -d -m python3 manage.py runserver 0:8000
