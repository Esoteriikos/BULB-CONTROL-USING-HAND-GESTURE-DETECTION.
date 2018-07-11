import cv2
import numpy as np
import time
import serial

cap = cv2.VideoCapture(0)

"""
************************************************************
                set up the arduino check baudrate and comm 
                and make chnges in ser=serial.Serial
                uncmmnt all the commands at line
                17 to 23 and 76,82,88.
************************************************************
"""

# ser = serial.Serial('com4', 9600)
#
# def led():
#     ser.write(b'1')
#
# def off():
#     ser.write(b'0')

ctime = time.time()
while True:
    try:
        ret, frame = cap.read()
        # cv2.imshow('frame1',frame)
        frame = cv2.flip(frame, 1)
        kernel = np.ones((3, 3), np.uint8)

        roi = frame[150:350, 150:350]

        cv2.rectangle(frame, (150, 150), (350, 350), (0, 0, 0), 0)
        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

        low_mask = np.array([0, 20, 70], dtype=np.uint8)
        up_mask = np.array([20, 255, 255], dtype=np.uint8)

        mask = cv2.inRange(hsv, low_mask, up_mask)

        mask = cv2.dilate(mask, kernel, iterations=4)
        mask = cv2.GaussianBlur(mask, (5, 5), 100)

        _, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        cntour = max(contours, key=lambda x: cv2.contourArea(x))

        epsilon = 0.0005 * cv2.arcLength(cntour, True)
        approx = cv2.approxPolyDP(cntour, epsilon, True)

        hull = cv2.convexHull(cntour)

        areahull = cv2.contourArea(hull)
        areacontour = cv2.contourArea(cntour)

        arearatio = ((areahull - areacontour) / areacontour) * 100

        hull = cv2.convexHull(approx, returnPoints=False)
        defects = cv2.convexityDefects(approx, hull)

        for i in range(defects.shape[0]):
            s, e,f, d = defects[i, 0]
            start = tuple(approx[s][0])
            end = tuple(approx[e][0])
            far = tuple(approx[f][0])

            cv2.line(roi, start, end, [0, 255, 0], 2)

        font = cv2.FONT_HERSHEY_SIMPLEX

        if areacontour < 2500:
            cv2.putText(frame, 'adjust', (10, 60), font, 2, (255, 255, 255), 3, cv2.LINE_AA)
            if (time.time() - ctime > 1):
                # off()
                ctime = time.time()
        else:
            if arearatio < 25:
                cv2.putText(frame, 'OFF', (10, 60), font, 2, (255, 255, 255), 3, cv2.LINE_AA)
                if (time.time() - ctime > 1):
                    # off()
                    ctime = time.time()

            else:
                cv2.putText(frame, 'ON', (10, 60), font, 2, (255, 255, 255), 3, cv2.LINE_AA)
                if (time.time() - ctime > 1):
                    # led()
                    ctime = time.time()


        cv2.imshow('frame', frame)
        
    except:
        pass

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
cap.release()





