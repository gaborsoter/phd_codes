from complaya import Complaya
import serial
import time
from array import array
import numpy as np

import re

camera = None
complaya = Complaya()

# set up serial comms
print("serial set up")
#ser = serial.Serial (port='/dev/cu.wchusbserial1420', baudrate = 115200, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS)
ser = serial.Serial (port='/dev/cu.wchusbserial1420', baudrate = 115200)


n = 1
# low pass filtering
samples = 5

serialCount = 0
synced = 0

data = [0,0,0]
data_old = [0,0,0]

calibrated = 0
calibration = [0,0,0]

calibration_length = 20 # must be an integer

firsthundred = []

n = 1
first = 0

while True:
	ser.write(b'a')
	received_data = str(ser.readline())

	split = received_data.split(',')

	if len(split) == 5:
		data[0] = float(split[1])
		data[1] = float(split[2])
		data[2] = float(split[3])

 	

	x = 130.18 - data[0]
	y = 3.0 - data[1]
	z = -5.82 - data[2]

	print("%.2f" % x, "%.2f" % y,"%.2f" % z)

	data_old = data[:]