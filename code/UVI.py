import time
import os
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM) 
DEBUG = 1
# read SPI data from MCP3008 chip, 8 possible adc's (0 thru 7)
def readadc(adcnum, clockpin, mosipin, misopin, cspin): 
	if ((adcnum > 7) or (adcnum < 0)):
		return -1 
	GPIO.output(cspin, True)	
	GPIO.output(clockpin, False) 	# start clock low 
	GPIO.output(cspin, False) 		# bring CS low
	commandout = adcnum
	commandout |= 0x18 # start bit + single-ended bit 
	commandout <<= 3 # we only need to send 5 bits here
	for i in range(5):
		if (commandout & 0x80):
			GPIO.output(mosipin, True) 
		else:
			GPIO.output(mosipin, False) 
		commandout <<= 1
		GPIO.output(clockpin, True) 
		GPIO.output(clockpin, False)

	adcout = 0
	# read in one empty bit, one null bit and 10 ADC bits 
	for i in range(12):
		GPIO.output(clockpin, True) 
		GPIO.output(clockpin, False) 
		adcout <<= 1
		if (GPIO.input(misopin)):
			adcout |= 0x1 
	GPIO.output(cspin, True)
	adcout >>= 1 # first bit is 'null' so drop it 
	return adcout

# change these as desired - they're the pins connected from the # SPI port on the ADC to the Cobbler
SPICLK = 18
SPIMISO = 23
SPIMOSI = 24 
SPICS = 25

# set up the SPI interface pins
GPIO.setup(SPIMOSI, GPIO.OUT) 
GPIO.setup(SPIMISO, GPIO.IN) 
GPIO.setup(SPICLK, GPIO.OUT) 
GPIO.setup(SPICS, GPIO.OUT)

def ohms_law(voltage, current):
	resistance = voltage/current
	return resistance
# 10k trim pot connected to adc #0
sensor_adc = 7;
vin=5

while True:
	# read the analog pin
	read_pin = readadc(sensor_adc, SPICLK, SPIMOSI, SPIMISO, SPICS)
	vout = read_pin/1023. *vin
	# FROM Arduino forum
	# forum.arduino.cc/index.php?topic=253202.0
	sensor_v = vout/471
	milliv = sensor_v * 1000
	uvi = milliv*(5.25/20)
	
	#result =(pull_down_resistance *vin)/vout - pull_down_resistance
	if DEBUG:
		print "UVI:", read_pin 
		print "voltage", sensor_v
		print milliv
		print uvi
	time.sleep(1)

"""
Full voltage detected suggets a wiring problem
"""
