import time
import numpy as np
import cv2
import sys
import argparse
import random
import threading
import serial

import rtmidi_python as rtmidi
import settings as default_settings
import utils
from tracker import Tracker

# Algorithm that is called


class Complaya:
    def __init__(self, settings=None, midi_port=None):
        self.midi_out = rtmidi.MidiOut(b'in')

        if not settings:
            self.settings = default_settings.load()

        # Default to first port
        if midi_port == None:
            # TODO: check to see if there are any ports at all first!
            midi_port = self.midi_out.ports[0]

        self.midi_enabled = True

        self.midi_out.open_port(midi_port)

        # Control Change is signalled by 0xb0, see: https://www.midi.org/specifications/item/table-1-summary-of-midi-message
        # Also good to stick to typically undefined range, http://nickfever.com/music/midi-cc-list
        # TODO: don't hardcode cc!
        self.cc_hex = 0xb0
        self.x_cc = 86
        self.y_cc = 87
        self.z_cc = 88

        self.metrics = {
            "x": 0,
            "y": 0,
            "z": 0
        }

        self.tracker = Tracker()

    def next_frame(self, ser, array_x, array_y, array_z, n, samples):
        """
            process the next frame
        """
        # TODO: Put serial stuff here
        #ser = serial.Serial (port='/dev/cu.usbserial', baudrate = 9600)    #Open port with baud rate, check if COM4 correct for computer used
        received_data = ser.read()              #read serial port
        time.sleep(0.025)
        data_left = ser.inWaiting()             #check for remaining byte
        received_data += ser.read(data_left)
        print ('Send and Received:', received_data)     #print received data


        try:
            xbyte,ybyte,zbyte = received_data.split()
            x = int(xbyte)
            y = int(ybyte)
            z = int(zbyte)
        except ValueError:
            pass
            
 
        if(n <= samples):
            array_x.append(x)
            array_y.append(y)
            array_z.append(z)
            x = sum(array_x) / n
            y = sum(array_y) / n
            z = sum(array_z) / n
            n = n + 1
        else:
            array_x.pop(0)
            array_x.append(x)
            array_y.pop(0)
            array_y.append(y)
            array_z.pop(0)
            array_z.append(z)
            x = sum(array_x) / samples
            y = sum(array_y) / samples
            z = sum(array_z) / samples

        #x = np.random.rand()
        #y = np.random.rand()
        #z = np.random.rand()

        #print(x, y, z)

        self.metrics["x"] = x / 255
        self.metrics["y"] = y / 255
        self.metrics["z"] = z / 255

        if self.midi_enabled:
            self.set(self.x_cc, self.rescale(x))
            self.set(self.y_cc, self.rescale(y))
            self.set(self.z_cc, self.rescale(z))


        return array_x, array_y, array_z, n

    # Rescales a value from 0-1 --> 0-127
    # Ensures return value is in range and integer
    def rescale(self, value):

        new_value = value

        if new_value < 0:
            new_value = 0
        elif new_value > 127:
            new_value = 127

        return new_value

    # This method to assigns a control (eg x,y or z) to a parameter in ableton
    def set(self, cc, value=0):
        self.midi_out.send_message([self.cc_hex, cc, value])

    def set_x(self):
        self.set(self.x_cc)

    def set_y(self):
        self.set(self.y_cc)

    def set_z(self):
        self.set(self.z_cc)


if __name__ == '__main__':    
    # Arg Parsing
    parser = argparse.ArgumentParser(description='Tak-Tak-Tak Tone.')
    parser.add_argument('--set', help='Give this a value of x,y,z to assign to a parameter in ableton')
    parser.add_argument('--video', help='Use a video file instead', default=1)

    args = parser.parse_args(sys.argv[1:])

    # Make a Taka-tak-taky-tone
    complaya = Complaya()

    # Set param or run
    if args.set:
        if args.set == 'x':
            complaya.set_x()
        elif args.set == 'y':
            complaya.set_y()
        elif args.set == 'z':
            complaya.set_z()
        else:
            print("Do not know how to set", args.set)
            print("Must be x, y or z")

    elif args.video:
        complaya.run(args.video)
    
    else:
        complaya.run()
