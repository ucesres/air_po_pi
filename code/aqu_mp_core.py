"""
Core file for air quality monitoring pi project
Ed Sharp
Created 4/11/16
See https://github.com/tomhartley/AirPi for original code - optimised here for rm 1.06 analysis
Necessary to change instruments due to UCL purchasing policy
"""

import RPi.GPIO as GPIO
import pandas
import ConfigParser

# get sensor information from the config file
"""This will need to be altered to change characteristics of instruments"""
sensorConfig = ConfigParser.SafeConfigParser()
sensorConfig.read('sensors.cfg')
sensorNames = sensorConfig.sections()

