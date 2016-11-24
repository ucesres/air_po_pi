
vin =3.3 or 5
vout = read_pin/1023. *vin

if pull_down:
	result =(pull_down_resistance *vin)/vout - pull_down_resistance
	
if pull_up:
	result =pull_up_resistance /((vin/vout)-1)
	
if none:
	resout = vout*1000


Analogue
resistances according to air pi
for conversion  

MICS 2710 = down 10000
TGS2600 = down 22000
LDR up = 10000
MICS 5525 = down 100000
