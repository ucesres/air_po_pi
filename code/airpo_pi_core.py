import sys
import Adafruit_DHT
import time
import csv
import datetime
# see adafruit examples to change sensor
sensor = Adafruit_DHT.AM2302
# change if configuration is altered
pin = 17
# retry to 15 times to get a sensor reading (waiting 2 seconds between each retry).
humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
timestamp = datetime.now
while True:
	
	fields=[time_stamp,temperature,humidity]
	with open(r'data/temp_humid.csv', 'a') as f:
					writer = csv.writer(f)
					writer.writerow(fields)
