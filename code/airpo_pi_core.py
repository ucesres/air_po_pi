#!/usr/bin/python
import sys
import Adafruit_DHT
import time
import csv
import datetime
import math
import numpy
from MCP_3008 import *

# fill dicts with analogue settings [adc port, vin, pull_down, pull_up]
analogue_settings ={'co2':[0,5,1000000.,0],
					'lux':[1,3.3,0,22000.],
					}

def analogue_readings(name):
	sett = analogue_settings[name]
	read_pin = readadc(sett[0], SPICLK, SPIMOSI, SPIMISO, SPICS)
	vout = read_pin/1023. *sett[1]
	numpy.errstate(divide='ignore')
	if vout not in [sett[1], 0.0]:
		if sett[2] !=0:
			result =(sett[2] *sett[1])/vout - sett[2]
		else:
			result = sett[3]/((sett[1]/vout)-1)
			
		return result
	else:
		return 100.0
	
while True:
	timestamp = datetime.datetime.now()
	humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.AM2302, 17)
	#if humidity is not None and temperature is not None:
	#	print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
		
	fields=[timestamp,temperature,humidity]
	with open(r'/home/pi/projects/Air_po_pi/data/temp_humid.csv', 'a') as f:
					writer = csv.writer(f)
					writer.writerow(fields)
	
	co2_rs_ro = analogue_readings('co2') 
	print co2_rs_ro
	#print co2_rs_ro
	# this does not include a temperature correction as the range is very small across the temperatures
	# experienced in room 1.06 - see calibratiion.ipynb for further work
	if co2_rs_ro >1.0:
		co2_ppm = 116.6020682 *(((co2_rs_ro/31750549))**-2.769034857)
	else:
		co2_ppm = 0
	co2_fields = [timestamp, co2_ppm]
	#print "co2", co2_ppm
	with open(r'/home/pi/projects/Air_po_pi/data/co2.csv', 'a') as g:
					writer = csv.writer(g)
					writer.writerow(co2_fields)
					#print co2_fields
	
	lux_rs_ro = analogue_readings('lux')
	theta = (numpy.log(lux_rs_ro/1000) -4.57666882)/-0.75325319
	# 10.76 converts from ftc to lux, see datasheet
	# for now assume a linear correction factor of 1.69 - more readings are probably necessary
	# test bby dimming lights tomorrow
	lux = (math.exp(theta) *10.76)*1.69
	lux_fields = [timestamp,lux]
	#print lux
	with open(r'/home/pi/projects/Air_po_pi/data/lux.csv', 'a') as h:
					writer = csv.writer(h)
					writer.writerow(lux_fields)
	
	time.sleep(1)

