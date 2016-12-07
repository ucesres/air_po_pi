#!/bin/sh
# launcher.sh

cd /
cd home/pi/projects/Air_po_pi/code
sudo python daily_tasks.py
cd /

cd home/pi/projects/Air_po_pi
git add .
git commit -m "auto update"
git push https://ucesres:cambodia06@github.com/ucesres/air_po_pi.git 
cd /
