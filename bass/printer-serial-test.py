import serial
import time

ser = serial.Serial('/dev/tty.usbserial-14320', 115200)

string = "G53 G0 X10 Y10 Z10 \r\n"

cmd = bytes(string, 'utf-8')

time.sleep(2)
ser.write(cmd)
time.sleep(1)
ser.close()