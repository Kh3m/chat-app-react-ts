#!/usr/bin/env bash

# kill any servers that may be running in the background 
sudo pkill -f runserver

# kill frontend servers too

# Create the PostgreSQL user
sudo -u postgres psql -c "CREATE USER fxm_dev WITH ENCRYPTED PASSWORD 'fxm_dev_pwd';"
