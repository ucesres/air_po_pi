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
sensor_adc = 0;
vin=5
pull_down_resistance = 1000000.
#pull_up_resistance = 1000000.

while True:
	# read the analog pin
	read_pin = readadc(sensor_adc, SPICLK, SPIMOSI, SPIMISO, SPICS)
	vout = read_pin/1023. *vin
	result =(pull_down_resistance *vin)/vout - pull_down_resistance
	#result =pull_up_resistance /((vin/vout)-1)
	"""
	VREF = 5.
	# adc volatge as a function of the digital readout 
	voltage = read_pin/1023. *VREF
	
	
	current = 40 /1000000.# supposedly the pull down resistance is constant - where to measure this
	# and which voltage to use?
	
	#sensor resistance - need to know the current through the sensor
	rs = ohms_law(voltage,current)
	# the RO value needs to be refined, using calibration values from Sam/Jez's equipment                                                       
	#sensor ppm
	ppm = 116.6020682* ((rs/14560.415944987377)**-2.769034857)
	"""
	ppm = 116.6020682 *((result/49395270.0633941)**-2.769034857)

	if DEBUG:
		print "MQ135:", read_pin 
		print "MQ135:", result
		print "ppm" , ppm
	time.sleep(1)
