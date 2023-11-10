#!/usr/bin/env bash

cd /home/ubuntu/django-aws_cicd/order_service/

# Install any software that's unique to the service

# activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Set environmental variables
export DEV_DB_NAME="order_service_dev"
export DEV_DB_USER="fixam_dev"
export DEV_DB_USER_PWD="fixam_dev_pwd"

# Create the PostgreSQL database
# Check if the database exists
if sudo -u postgres psql -tAc "SELECT 1 FROM pg_database WHERE datname = '$DEV_DB_NAME'" | grep -qw 1; then
  :
else
  # Create the PostgreSQL database
  sudo -u postgres psql -c "CREATE DATABASE $DEV_DB_NAME;"
  # Grant all privileges to the user on the database
  sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE $DEV_DB_NAME TO $DEV_DB_USER;"
fi

# Install requirements.txt
pip3 install -r requirements.txt

# Add instance public IP address to ALLOWED_HOST
sed -i "/ALLOWED_HOSTS/c\ALLOWED_HOSTS = ['$(curl -s ifconfig.me)']" ./order_service/settings.py

# run server
python3 manage.py makemigrations api_v1
python3 manage.py migrate
screen -d -m python3 manage.py runserver 0:8002
