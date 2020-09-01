import cv2
import serial
import time

color = (255, 0, 255)
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)


def empty(a):
    pass


cv2.namedWindow("Result")
cv2.resizeWindow("Result", 640, 480 + 100)
cv2.createTrackbar("Scale", "Result", 400, 1000, empty)
cv2.createTrackbar("Neighbor", "Result", 8, 50, empty)
cv2.createTrackbar("Min Area", "Result", 0, 100000, empty)
cv2.createTrackbar("Brightness", "Result", 180, 255, empty)

cascade = cv2.CascadeClassifier('/Users/Saif/Documents/GitHub/affinity/bass/fish_cascade.xml')

while True:

    cameraBrightness = cv2.getTrackbarPos("Brightness", "Result")
    cap.set(10, cameraBrightness)

    success, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    scaleVal = 1 + (cv2.getTrackbarPos("Scale", "Result") / 1000)
    neig = cv2.getTrackbarPos("Neig", "Result")
    objects = cascade.detectMultiScale(gray, scaleVal, neig)

    for (x, y, w, h) in objects:
        area = w * h
        minArea = cv2.getTrackbarPos("Min Area", "Result")
        if area > minArea:
            cv2.rectangle(img, (x, y), (x + w, y + h), color, 3)
            cv2.putText(img, "Bass", (x, y - 5), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, color, 2)
            roi_color = img[y:y + h, x:x + w]
            n = (x + 30)/100
            m = (y + 30)/100
            #need to draw another on the neck point

    cv2.imshow("Result", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

movement = ("""
%
M106;
G00 X0Y0Z0;
G80;
G17;
G21; 
G01 X""" + str(n) + """;
G01 Y""" + str(m) + """; 
G04 P500;
G00 Z-H;
G04 P1000;
G00 Z0;
G04 P1000;
G01 X0Y0;
M02;
""")

ser = serial.Serial('/dev/tty.usbserial-14320', 115200)

ser.isOpen()

string = "G00\r\n"
#to add the rest from above once working reliably

cmd = bytes(string, 'utf-8')

time.sleep(2)
ser.write(cmd)
time.sleep(1)
ser.close()
