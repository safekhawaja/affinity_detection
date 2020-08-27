import serial
import time

ser = serial.Serial('/dev/tty.usbserial-14320', 115200)

string = "G00\r\n"

cmd = bytes(string, 'utf-8')

time.sleep(2)
ser.write(cmd)
time.sleep(1)
ser.close()
