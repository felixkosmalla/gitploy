#!/bin/bash

# you should not execute this script by hand! it will run through supervisor

# enable the virtual environment
source /home/gitploy/env/bin/activate

cd /home/gitploy/gitploy/
exec gunicorn gitlab_deployment.wsgi:application --bind unix:/home/gitploy/gunicorn.socket