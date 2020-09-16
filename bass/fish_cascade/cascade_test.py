import cv2

color = (255, 0, 255)
cap = cv2.VideoCapture("/Users/saif/Downloads/ezgif.com-resize.mp4")
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

cascade = cv2.CascadeClassifier('/Users/saif/Documents/GitHub/affinity_detection/bass/fish_cascade/fish_cascade.xml')

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
        elif area <= minArea:
            cv2.rectangle(img, (x, y), (x + w, y + h), color, 3)
            cv2.putText(img, "Bass", (x, y - 5), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, color, 2)
            roi_color = img[y:y + h, x:x + w]
            """
            convertedPoints = [(x + w - 30) / 100, y + 30 / 100]
            myStabPosition = "G01 X" + str(convertedPoints[0][0]) + " Y" + str(convertedPoints[0][1]) + "\r\n"
            stb_pos = bytes(myStabPosition, 'utf-8')


            def stab():
                commands = [strt, stp1, stp2, stb_pos, stb, stp2]
                for cmd in commands:
                    ser.write(cmd)
                    time.sleep(2)


            stab()
            """

    cv2.imshow("Result", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
