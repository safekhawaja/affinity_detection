import serial
import time

ser = serial.Serial('/dev/tty.usbserial-14310', 9600)

string = "G01 X1 Y1 Z1 \r\n"

cmd = bytes(string, 'utf-8')

time.sleep(2)
ser.write(cmd)
time.sleep(1)
ser.close()
