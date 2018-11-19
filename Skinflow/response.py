import numpy as np
import cv2
import matplotlib.pyplot as plt

# import recording
cap = cv2.VideoCapture('test2.mov')

# colour ranges
lower = np.array([0, 0, 0], dtype = "uint8")
upper = np.array([120, 255, 255], dtype = "uint8")

# frame counting
n = 0

# data array initialisation
dataarray = []
lower_bound = []
upper_bound = []
x_axis = []
std_array = []

while(cap.isOpened()):
    ret, frame = cap.read() # reading frame

    try:
        mask = cv2.inRange(frame, lower, upper)
        output = cv2.bitwise_and(frame, frame, mask = mask) # colour filtering
        gray = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY) # grayscaling

        gray = gray[210:220,0:640] # roi

        # liquid discplacement - 1px height
        line0 = gray[0:1, 0:640]
        line1 = gray[1:2, 0:640]
        line2 = gray[2:3, 0:640]
        line3 = gray[3:4, 0:640]
        line4 = gray[4:5, 0:640]
        line5 = gray[5:6, 0:640]
        line6 = gray[6:7, 0:640]
        line7 = gray[7:8, 0:640]
        line8 = gray[8:9, 0:640]
        line9 = gray[9:10, 0:640]

        # count all the non-black pixels
        nob0 = cv2.countNonZero(line0)
        nob1 = cv2.countNonZero(line1)
        nob2 = cv2.countNonZero(line2)
        nob3 = cv2.countNonZero(line3)
        nob4 = cv2.countNonZero(line4)
        nob5 = cv2.countNonZero(line5)
        nob6 = cv2.countNonZero(line6)
        nob7 = cv2.countNonZero(line7)
        nob8 = cv2.countNonZero(line8)
        nob9 = cv2.countNonZero(line9)

        # mean and std
        mean = np.mean([nob0, nob1, nob2, nob3, nob4, nob5, nob6, nob7, nob8, nob9])
        std = np.std([nob0, nob1, nob2, nob3, nob4, nob5, nob6, nob7, nob8, nob9], ddof=1)
        std_array.append(std)

        lower_bound.append(mean - std)
        upper_bound.append(mean + std)
        dataarray.append(mean)

        x_axis.append(n / 33.36) # divide by framerate to get time

        # frame count 
        n += 1

        cv2.imshow('frame',gray)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    except:
        # plot
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.set_aspect(0.025)
        ax.plot(x_axis, dataarray)
        ax.set_xlabel('Time [s]')
        ax.set_ylabel('Indicator level [pixel]')
        ax.fill_between(x_axis, lower_bound, upper_bound, facecolor='lightblue')
        ax.set_xlim([0,20])
        ax.set_ylim([0,350])
        fig.savefig('response.pdf')
        break

cap.release()
cv2.destroyAllWindows()