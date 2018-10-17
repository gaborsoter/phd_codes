import numpy as np
import cv2
import time

class Tracker:
    def __init__(self,):
        self.point = np.array([0,0], dtype=float)

        self.last_time = time.time()
        self.outputImage = np.zeros([10,10,3], dtype=np.uint8)

        # Dictionary of stats and metrics
        self.metrics = {}

    def next_frame(self, frame,
        blur_level=5,
        cut=50,
        dilation_iterations=6,
        erosion_iterations=15,
        binary_threshold=51,
        ):

        frame_height, frame_width = frame.shape[:2]

        blur = cv2.GaussianBlur(frame, (int(blur_level), int(blur_level)), 0) # blur
        gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY) # grayscale
        thresh= cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
               cv2.THRESH_BINARY,binary_threshold,1)
        kernel = np.ones((3,3),np.uint8) # kernel for the morphological operators
        dilation = cv2.dilate(thresh,kernel,iterations=dilation_iterations) # dilation
        erosion = cv2.erode(dilation,kernel,iterations=erosion_iterations) # erosion
        
        # TODO: Rename this, what is final?
        final = erosion[cut:frame_height-cut,cut:frame_width-cut] # roi

        # X and Y
        mx = 0
        my = 0
        black = 0 

        # lower resolution
        height, width = final.shape[:2]
        h = height/9
        h = int(h)
        w = width/13
        w = int(w)
        
        # moments
        pixels=[]

        # HACK: TODO: Clean this up, or add a comment to explain
        for i in range(w):
            for j in range(h):
                if (final[9*j-1,13*i-1]==0):
                    mx = mx + j
                    my = my + i
                    black = black + 1
                    pixels.append([9*j,13*i])
        
        if (black==0):
            # centre, if no black pixels
            cx=int(height/2)
            cy=int(width/2)
        else:
            # centre
            cx = int( mx / black * 9)
            cy = int( my / black * 13) 
       
        # draw circle
        cv2.circle(final,(cy,cx),10,(125,125,125),3)

        # number of black pixels (pressure measurement)
        nob = cv2.countNonZero(255-final)

        # show results
        self.outputImage = thresh

        # output variables for X and Y
        cxout=int(height/2)-cx
        cyout=cy-int(width/2)
        
        x = cxout
        y = cyout
        z = nob

        self.metrics["x"] = x
        self.metrics["y"] = y
        self.metrics["z"] = z

        return x, y, z

if __name__ == '__main__':
    while(cap.isOpened()):
        ret, frame = cap.read() # camera readout
        cx, cy, nob = threedimmap(frame) # X, Y and pressure
        print(cx, cy, nob) 
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
cv2.destroyAllWindows()