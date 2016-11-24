import time, math, numpy

from MCP_3008 import *

# 10k trim pot connected to adc #0
sensor_adc = 1;
vin =3.3
pull_up_resistance = 22000 # code says 10000, resistor is actually 22000
while True:
	# read the analog pin
	read_pin = readadc(sensor_adc, SPICLK, SPIMOSI, SPIMISO, SPICS)
	vout = (read_pin/1023.) *vin
	result =pull_up_resistance /((vin/vout)-1)
	# values derived from datasheet and numpy polyfit, see coding notes - this may need recalibrating
	theta = (numpy.log(result/1000) -4.57666882)/-0.75325319
	# 10.76 converts from ftc to lux, see datasheet
	lux = math.exp(theta) *10.76
	
	simple_lux = ((2500/vout)-500)/2.2
	if DEBUG:
		#print simple_lux
		print lux
	
		#print "vout", vout
		#
		#print "LDR resistance:", result
		#print "lux",lux
		#print vin/vout
	time.sleep(1)



"""
see pi.gate.ac.uk/posts/2014/02/25/airpisensors/
- this uses the relationship between lux and resistance from another sensor
therefore the polyfit calculations should be rerun, but it should work as a reasonable approx
lux = e**x
x = (ln(result/1000) - 4.125)/-0.6704

office = 320 - 500
"""
