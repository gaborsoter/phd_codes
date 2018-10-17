import serial
import time


while(True):
	ser = serial.Serial (port='/dev/cu.usbserial', baudrate = 9600)    #Open port with baud rate, check if COM4 correct for computer used
	received_data = ser.read()              #read serial port
	time.sleep(0.01)
	data_left = ser.inWaiting()             #check for remaining byte
	received_data += ser.read(data_left)
	x,y,z = received_data.split()
	xint = int(x)
	print ('Send and Received:', xint, y, z)     #print received data
