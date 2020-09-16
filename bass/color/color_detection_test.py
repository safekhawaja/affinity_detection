import cv2
import numpy as np
import time

frameWidth = 640
frameHeight = 480
cap = cv2.VideoCapture("/Users/saif/Documents/final fish shooting/fish recordings/ezgif.com-resize.mp4")
cap.set(3, frameWidth)
cap.set(4, frameHeight)
cap.set(10, 150)

# Color detection HSV values from match_colors_get.py (can use multiple)
myColors = [[0, 0, 0, 36, 255, 255]]

# Color printed to confirm detection coordinate (again, can use multiple)
myColorValues = [[255, 198, 145]]

myPoints = []  # [x, y, colorID]


def color_find(img, myColors, myColorValues):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    count = 0
    newPoints = []
    for color in myColors:
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
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
    return (x + w//6), (y + h//4)


# Adjust radius for visual display depending on height of camera from block
def draw(myPoints, myColorValues):
    for point in myPoints:
        rad = 5
        cv2.circle(imgResult, (point[0], point[1]), rad, myColorValues[point[2]], cv2.FILLED)


while True:
    success, img = cap.read()
    imgResult = img.copy()
    newPoints = color_find(img, myColors, myColorValues)
    if len(newPoints) != 0:
        for newP in newPoints:
            myPoints.append(newP)
            if len(myPoints) != 0:
                draw(myPoints, myColorValues)
                myPoints.remove(newP)
                time.sleep(0.1)

    cv2.imshow("Result", imgResult)
    if cv2.waitKey(1) and 0xFF == ord('q'):
        break
