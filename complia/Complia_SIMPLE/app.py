from complaya import Complaya
import serial

camera = None
complaya = Complaya()

# set up serial comms
print("serial set up")
ser = serial.Serial (port='/dev/cu.usbserial', baudrate = 9600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS)

array_x = []
array_y = []
array_z = []

n = 1
# low pass filtering
samples = 5

while True:
    array_x, array_y, array_z, n = complaya.next_frame(ser, array_x, array_y, array_z, n, samples)