import cv2
import numpy as np
import time
import serial

ser = serial.Serial('/dev/tty.usbserial-14320', 115200)  # note: declaring opens the port
frameWidth = 640
frameHeight = 480
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)
cap.set(10, 150)
height = 5  # Required distance to stab fish in G90 mode

start = "%\r\nO100\r\n"
setup1 = "G90\r\n"
setup2 = "G28\r\n"
Stab = "Z" + str(height) + "\r\n"

strt = bytes(start, 'utf-8')
stp1 = bytes(setup1, 'utf-8')
stp2 = bytes(setup2, 'utf-8')
stb = bytes(Stab, 'utf-8')

# Color detection HSV values from match_colors_get.py (can use multiple)
myColors = [[18, 46, 72, 40, 159, 238]]

# Color printed to confirm detection coordinate (again, can use multiple)
myColorValues = [[255, 198, 145]]

myPoints = []  # [x, y, colorID]


def color_find(img, myColors, myColorValues):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    count = 0
    newPoints = []
    for clr in myColors:
        lower = np.array(clr[0:3])
        upper = np.array(clr[3:6])
        mask = cv2.inRange(imgHSV, lower, upper)
        x, y = contours_find(mask)
        cv2.circle(imgResult, (x, y), 10, myColorValues[count], cv2.FILLED)
        if x != 0 and y != 0:
            newPoints.append([x, y, count])
        count += 1
        # cv2.imshow(str(color[0]), mask)
    return newPoints


# Adjust returned value relative to bounding box for specific fish (i.e. depends on orientation)
def contours_find(img):
    contours, Hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    x, y, w, h = 0, 0, 0, 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 7:
            # cv2.drawContours(imgResult, cnt, -1, (255, 0, 0), 3)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            x, y, w, h = cv2.boundingRect(approx)
    return x + w // 2, y


# Adjust radius for visual display depending on height of camera from printing floor
def draw(myPoints, myColorValues):
    for pnt in myPoints:
        rad = 5
        cv2.circle(imgResult, (pnt[0], pnt[1]), rad, myColorValues[pnt[2]], cv2.FILLED)


while True:
    success, img = cap.read()
    imgResult = img.copy()
    newPoints = color_find(img, myColors, myColorValues)
    if len(newPoints) != 0:
        for newP in newPoints:
            myPoints.append(newP)
            draw(myPoints, myColorValues)
            # pixels mapped to your respective printer and camera (in the form of aX + b)
            convertedPoints = [myPoints[0][0] // 10,
                               myPoints[0][1] // 10]
            myStabPosition = "G01 X" + str(convertedPoints[0][0]) + " Y" + str(convertedPoints[0][1]) + "\r\n"
            stb_pos = bytes(myStabPosition, 'utf-8')
            myPoints.remove(newP)

            def stab():
                commands = [strt, stp1, stp2, stb_pos, stb, stp2]
                for cmd in commands:
                    ser.write(cmd)
                    time.sleep(1)
            stab()

    cv2.imshow("Result", imgResult)
    if cv2.waitKey(1) and 0xFF == ord('q'):
        ser.close()
        break
