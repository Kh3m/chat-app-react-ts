#!/usr/bin/env bash

cd /home/ubuntu/django-aws_cicd/order_service/

# Install any software that's unique to the service

# activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Set environmental variables
DEV_DB_NAME="order_service_dev"
DEV_DB_USER="fixam_dev"
DEV_DB_USER_PWD="fixam_dev_pwd"

# Create the PostgreSQL database
sudo -u postgres psql -c "CREATE DATABASE $DEV_DB_NAME;"

# Grant all privileges to the user on the database
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE $DEV_DB_NAME TO $DEV_DB_USER;"

# Install requirements.txt
pip3 install -r requirements.txt

# run server
python3 manage.py makemigrations api_v1
python3 manage.py migrate
screen -d -m python3 manage.py runserver 0:8002
