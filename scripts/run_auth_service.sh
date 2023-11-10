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
screen -d -m python3 manage.py runserver 0:8000 > output.txt 2>&1

# Check the exit code of the last command
if [ $? -ne 0 ]; then
    echo "Error: The runserver command failed."
    # Echo the contents of the output file for additional information
    echo "=== Output ==="
    cat output.txt
    exit 1  # Exit the script with a non-zero exit code to indicate failure
fi

cat output.txt
