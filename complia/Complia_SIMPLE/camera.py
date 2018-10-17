from time import time
import cv2
import time

class Camera(object):
    def __init__(self, width=32, height=24, filename=0):
        # Make it an int if you can (for referencing webcams)
        try:
            self.filename = int(filename)
        except ValueError:
            self.filename = filename

        print ("filename", self.filename)

        self.cap = cv2.VideoCapture(0)

        print(width, height)
        self.cap.set(3, 32)
        self.cap.set(4, 24)

        self.last_time = time.time()
        self.frame = self.cap.read()



    def get_frame(self, framerate = 30):
        if (time.time() - self.last_time) > 1.0/framerate:
            _, new_frame = self.cap.read()
            self.frame = new_frame

            self.last_time = time.time()

        # Repeat Video Forever
        if self.frame is None:
            self.cap = cv2.VideoCapture(0)
            
            _, new_frame = self.cap.read()
            self.frame = new_frame

        return self.frame
