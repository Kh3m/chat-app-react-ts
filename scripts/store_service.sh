#!/usr/bin/env bash

cd /home/ubuntu/django-aws_cicd/store_service/

# Install any software that's unique to the service

# activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Set environmental variables

# Install requirements.txt
pip3 install -r requirements.txt

# run server
python3 manage.py makemigrations api_v1
python3 manage.py migrate
screen -d -m python3 manage.py runserver 0:8005
