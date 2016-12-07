#!/bin/sh
# launcher_5min.sh

cd /
cd home/pi/projects/Air_po_pi/code
sudo python five_minute_tasks.py
cd /
cd home/pi/projects/web_pi
sudo chown -R pi:pi /home/pi/projects/web_pi/
git add .
git commit -m "auto update a"
git push https://ucesres:cambodia06@github.com/ucesres/room_1.06.git gh-pages
cd /




