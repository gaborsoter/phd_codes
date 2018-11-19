import numpy as np
from scipy.interpolate import griddata
import matplotlib.pyplot as plt
import math
import cv2
from scipy import interpolate

# colour filter
lower = np.array([0, 0, 0], dtype = "uint8")
upper = np.array([120, 255, 255], dtype = "uint8")

# initialisation of arrays
dataarray = []
lower_bound = []
upper_bound = []
x_axis = []
std_array = []

# capture video init
cap = cv2.VideoCapture(1)

n = 0

calibration = []

def eval(delta_x, delta_y):

    upper_limit_x = 60
    upper_limit_y = 45

    # thresholding
    if delta_x > upper_limit_x:
        delta_x = upper_limit_x
    if delta_y > upper_limit_y: 
        delta_y = upper_limit_y
    if delta_x < 5:
        delta_x = 0
    if delta_y < 5: 
        delta_y = 0

    # normalisation
    delta_x = delta_x / upper_limit_x
    delta_y = delta_y / upper_limit_y

    return np.exp(5*(delta_x-1))*np.exp(5*(delta_y-1)) # activation function

def touch_probability(measurement):
    # split data
    horizontal = measurement[:8]
    vertical = measurement[8:]

    grid = []
    for i in range(8):
        for j in range(8):
            grid.append(eval(horizontal[i], vertical[j])) # calculate node values

    return grid 


while(cap.isOpened()):
    ret, frame = cap.read()

    # preprocessing
    mask = cv2.inRange(frame, lower, upper)
    output = cv2.bitwise_and(frame, frame, mask = mask)
    gray = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)

    gray = gray[60:370,50:640]


    levels_start = np.linspace(0, gray.shape[0]-10, 16) + 4

    # roi
    images = list(map(lambda x: gray[int(x):int(x)+1,0:640], levels_start))

    # count non black pixels
    nonzeros = list(map(lambda x: cv2.countNonZero(x), images))

    # calibration ("zeroing") for the first 50 frames
    if n < 50:
        calibration.append(nonzeros)
        n += 1
        origin = (np.array(calibration)).mean(0)
    else:
        array = touch_probability(nonzeros - origin)

        resolution = 50

        x = np.linspace(0,resolution,8)
        y = np.linspace(0,resolution,8)
        
        # interpolation
        f = interpolate.interp2d(x, y, array, kind='linear')

        output = gray[0:resolution, 0:resolution]
        for i in range(resolution):
            for j in range(resolution):
                output[j,i] = f(i,j)*255 # calculate pixel values


        # recolouring
        im_color = cv2.applyColorMap(output, cv2.COLORMAP_JET)
        cv2.namedWindow("frame", cv2.WINDOW_NORMAL)   
        cv2.imshow('frame', im_color)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

plt.show()

cap.release()
cv2.destroyAllWindows()





