#!/bin/bash
. /home/ubuntu/environments/dds_scrape_env/bin/activate
cd /home/ubuntu/work/DDS_Web
python manage.py runserver 0.0.0.0:80 --noreload --nothreading

