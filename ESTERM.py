import serial
import io
import time
import UTILS

D = UTILS.getINI('parameters.ini')

ser = serial.Serial(D('port_number'), D('baudrate'), timeout=1)  # open first serial port

if ser.isOpen():
    print "The port " + ser.portstr +  " is open"
else:
    print "The port " + ser.portstr +  " is not open."

ser.write("AT\r")      # write a string
print ser.read(7) 
'''
out = ''
let's wait one second before reading output (let's give device time to answer)
time.sleep(1)
while ser.inWaiting() > 0:
    out += ser.read()
if out != '':
    print out'''

ser.close()             # close port
