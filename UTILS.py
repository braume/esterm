#-*- coding:utf-8 -*-
import time
import _winreg
import serial
import os
import UTILS
import time
import re


def open_ser_list(registry_path):
    ''' Take data from the registry for the serial port and try each COM port until AT test is OK.
        Return the serial port conected to the Telit
    '''
    try:
        key = 0
        key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, registry_path, 0, _winreg.KEY_READ)
        i = 0
        while(1):
            try:
                name, data, type = _winreg.EnumValue(key, i)
                i+=1
            # Raised at the end of the list.
            except WindowsError:
                print 'The modem is not connected, check the cable or the drivers'
                exit(0)
            else:
                ser = open_ser(data)
                if ser != '':
                    if ser.getCTS():
                        res = UTILS.atcmd('AT', ser, False)
                        if res.find('OK') != -1:
                            D = UTILS.getINI('parameters.ini')
                            UTILS.atcmd('AT+CPIN='+ D['pin'], ser, False)
                            pin = UTILS.atcmd('AT+CPIN?',ser, False)
                            if pin.find('READY') != -1:
                                print '\n', data, "is connected to the Telit modem and Pin code is initialized."
                                break
                            else:
                                print '\n', data, "is connected to the Telit modem and Pin code is not initialized."
                                break
                        else:
                            # print data +  " is not connected to the Telit modem."    
                            pass
                    else:
                        # print data +  " is not connected to the Telit modem."
                        pass
        _winreg.CloseKey(key)
    except WindowsError, w:
        print 'WRONG KEY REGISTRY:', w
        exit(0)
    return ser


def open_ser(port):
    ''' Open a serial port catching possible errors.
        Return : ser - The serial port.
    '''
    D = UTILS.getINI('parameters.ini')
    ser = ''
    try:
        ser = serial.Serial(port, int(D['baudrate']), rtscts = True, timeout=0.01)
    # Raise a SerialException which raise a UnicodeException with 'accès refusé'.
    # Replacing %s,%s by %r,%r line 59 of seriawin32.py would correct it.
    except UnicodeDecodeError:
        # print port, 'is already used.'
        pass
    except serial.SerialException, s:
        print 'BUSY PORT:', s
    except AttributeError, a:
        print 'ATTRIBUTE ERROR:', a
    except NameError, n:
        print 'NAME ERROR:', n
    finally:
        pass
    return ser
    

def atcmd(cmd, ser, dis=True, wscript = False):
    ''' Send AT command (cmd) on the serial port (ser) displaying by default the result
        Return the echo and the result of the AT command (see ATE0\r for enable/disable the echo)
    '''
    # Write AT command in hte output buffer
    ser.write(cmd + '\r')
    # Wait Telit to write in the input buffer
    UTILS.sleep(1)
    res = ''
    # While there is something in the input buffer add it to res
    while ser.inWaiting()>0:
        i = 0
        while i < 512:
            i+=1
            res += ser.read(16)
            if not ser.inWaiting()>0 or res.find('OK'):
                break
    if dis:
        print res
    # If we have a wscript prompt
    if wscript:
        script = cmd.split('"')
        D = UTILS.getINI('parameters.ini')
        with open(D['path']+ '\\'+ script[1], 'rb') as f:
            start = float(time.time())
            print 'Uploading:', script[1]
            ser.write(f.read())
            UTILS.sleep(1)
            res = ser.read()
            while res.find('OK') == -1:
                res += ser.read()
            print 'End after {0} secondes'.format(float(time.time()-start))
            print res
    return res


def sleep(tenthOfSec):
    ''' Make a pause in the script in tenth of second '''
    sec = float(float(tenthOfSec)/10.0)
    time.sleep(sec)
    return 0

def file_dir(path):
    ''' Give file of the specified directory'''
    import os
    os.chdir("C:\Python27\esterm")
    for files in os.listdir("."):
        res = files
    return res
    
def tab(path):
    import readline
    
    FILES = file_dir(path)

    def complete(text, state):
        for cmd in COMMANDS:
            if cmd.startswith(text):
                if not state:
                    return cmd
                else:
                    state -= 1

    readline.parse_and_bind("tab: complete")
    readline.set_completer(complete)
    raw_input('Enter section name: ')

def getINI(file):
    ''' Return a dictionnary from file '''
    D={}
    # file = '/sys/' + file (while file in Telit)
    f = open("parameters.ini")
    for line in f:
        if (line.find('=') != -1):
            line = line.rstrip('\r\n')
            parts = line.split('=')
            D[parts[0]] = parts[1]
    f.close()
    return D
    
    