import time, sys
import RPi.GPIO as GPIO
# BCM = complex numbering, BOARD = physical
# use BCM - this allows 
GPIO.setmode(GPIO.BCM)
GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
 
def action(pin):
    print 'Sensor detected action!'
    return
 
GPIO.add_event_detect(7, GPIO.RISING)
GPIO.add_event_callback(7, action)
 
try:
    while True:
        print 'alive'
        time.sleep(0.5)
except KeyboardInterrupt:
    GPIO.cleanup()
    sys.exit()
