#-*- coding:utf-8 -*-
import serial
import time
import os
import UTILS
import sys

D = UTILS.getINI('parameters.ini')

UTILS.open_ser_list(D['registry_path'])

def size():
    p = D['path'][:-1]
    u = D['upload'][:-1]
    return int(os.path.getsize(p + u))

'''print 'The size of',D['path'] + D['upload'], 'is', size()
print D['path']
'''
if ser.isOpen():
    print "\nThe port " + ser.portstr +  " is open"
else:
    print "\nThe port " + ser.portstr +  " is not open."

def error():
    if ser.isOpen():
		print "\nThe port " + ser.portstr +  " is open"
    else:
		print "\nThe port " + ser.portstr +  " is not open."
    
def atok():
    ser.write('AT\r')
    UTILS.sleep(1)
    start=time.time()
    while ser.inWaiting()>0:
        print ser.read(888)
    print 'End after {0} secondes\n'.format(float(time.time()-start))
    
def pin():
    i=0
    print ser.write('AT+CPIN=\"'+D['pin']+'\"\r')
    UTILS.sleep(1)
    start=time.time()
    while ser.inWaiting()>0:
        print 'lecture ',(i+1),ser.read(1)
        i+=1
    print 'End after {0} secondes\n'.format(float(time.time()-start))
 
def signal_quality():
    UTILS.sleep(8)
    print ser.write('AT+CSQ\r')
    i=0
    while ser.inWaiting()>0:
        print 'lecture ',(i+1),ser.read(1)
        i+=1
 
def up_list():
    ser.write('AT#WSCRIPT=\"'+D['upload']+ ',' +size() + ', 0\"\r')
    time.sleep(3)
    print ser.read(2000)
    ser.write('AT+LSCRIPT\r')
    print ser.read(2000)
    
def exe_():
    ser.write('AT#ESCRIPT="'+D['exe']+ ',' +size() + ', 0\"\r')
    time.sleep(1)
    ser.write('AT#EXECSCR=\"'+D['exe']+ ',' +size() + ', 0\"\r')
    time.sleep(3)
    print ser.read(2000)

def shtdwn():
    ser.write('AT#SHDN\r')
    UTILS.sleep(8)
    start=time.time()
    print ser.read(888)
    print 'End after {0} secondes\n'.format(float(time.time()-start))
    
def exit_():
    exit(0)
    
    
while 1:
    print """
    \t 1-AT 
    \t 2-Pinit
    \t 3-Signal quality 
    \t 4-Upload script & List files 
    \t 5-Enable script & Execute
    \t 6-Shutdown
    \t 7-Exit
    """
    try:
        case = int(raw_input("What do you want to:\n >>  "))
    except ValueError:
        case = 0
        
    if case == 0:
        print 'Please enter an integer ...'
    elif case == 1:
        atok()
    elif case == 2:
        pin()
    elif case == 3:
        signal_quality()
    elif case == 4:
        up_list()
    elif  case == 5:
        exe_()
    elif  case == 6:
        shtdwn()
        print "Telit is off, bye !"
    elif  case == 7:
        print "Bye !\r\n"
        exit_()
    else:
        print "Please ...\r\n"

ser.close()             # close port

