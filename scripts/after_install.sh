#!/usr/bin/env bash

# kill any servers that may be running in the background 
sudo pkill -f runserver

# kill frontend servers too

# Create the PostgreSQL user
# Check if the user exists
if sudo -u postgres psql -tAc "SELECT 1 FROM pg_roles WHERE rolname='fixam_dev'" | grep -qw 1; then
  echo "User fixam_dev already exists."
else
  # Create the PostgreSQL user
  sudo -u postgres psql -c "CREATE USER fixam_dev WITH ENCRYPTED PASSWORD 'fixam_dev_pwd';"
  echo "User fixam_dev created."
fi

# Make ubuntu owner of every file in /home/ubuntu/django-aws_cicd
sudo chown -R ubuntu:ubuntu /home/ubuntu/django-aws_cicd
