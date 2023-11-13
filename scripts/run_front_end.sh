#!/usr/bin/env bash

cd /home/ubuntu/django-aws_cicd/fixam-frontend/

# Install any software that's unique to the service
# install node.js:
sudo apt update
sudo apt install curl software-properties-common
curl -sL https://deb.nodesource.com/setup_14.x | sudo -E bash -
sudo apt install nodejs

# activate virtual environment

# Set environmental variables

# Install dependencies
npm install

# run server
npm run dev &
