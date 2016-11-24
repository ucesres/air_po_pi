"""
Adapted from executable ./AdafruitDHT.py in the examlpes folder
"""
import sys
import Adafruit_DHT
import time
# see adafruit examples to change sensor
sensor = Adafruit_DHT.AM2302
# change if configuration is altered
pin = 17
# retry to 15 times to get a sensor reading (waiting 2 seconds between each retry).
humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

while True:
	if humidity is not None and temperature is not None:
		print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
	else:
		print('Failed to get reading. Try again!')
		sys.exit(1)
	time.sleep(1)
