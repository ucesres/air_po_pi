#!/bin/sh
# launcher.sh

cd /
cd home/pi/projects/Air_po_pi/code
sudo python hourly_tasks.py
sudo python outside_air_pollution.py
cd /
