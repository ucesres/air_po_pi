import time
import os
import RPi.GPIO as GPIO
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
					'no2' :[3,5,131,131]
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
	
# 10k trim pot connected to adc #0
sensor_adc = 3;
vin=5
pull_down_resistance = 131
pull_up_resistance = 131

while True:
	# read the analog pin
	read_pin = readadc(sensor_adc, SPICLK, SPIMOSI, SPIMISO, SPICS)
	vout = read_pin/1023. *vin
	result =((pull_down_resistance *vin)/vout - pull_down_resistance)/24757.09285538479
	#rsro1=pull_up_resistance /((vin/vout)-1)
	if DEBUG:
		print "MICS_2714:", read_pin 
		print "vout", vout
	
	time.sleep(1)
