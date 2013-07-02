#-*- coding:utf-8 -*-
import time
import _winreg
import serial
import os
import TOOLS
import time
import re


def open_ser_list(registry_path):
    ''' Take data from the registry for the serial port and try each COM port until AT test is OK.
        Return the serial port conected to the Telit
    '''
    try:
        key = 0
        ser_usb = ''
        ser_serial = ''
        key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, registry_path, 0, _winreg.KEY_READ)
        i = 0
        while(1):
            try:
                name, data, type = _winreg.EnumValue(key, i)
                i+=1
            # Raised at the end of the list.
            except WindowsError:
                if ser_usb == '' and ser_serial == '':
                    print 'Check the cable, the drivers or the port availability.'
                    exit(1)
                elif ser_usb != '' and ser_serial != '':
                    choice = raw_input('1-Usb or 2-Serial ?')
                    if choice == 1:
                        ser = ser_usb
                        break
                    elif choice == 2:
                        ser = ser_serial
                        break
                    else:
                        print 'Please ...'
                else:
                    if ser_serial != '':
                        ser = ser_serial
                        break
                    else:
                        ser = ser_usb
                        break
            else:
                ser = open_ser(data)
                if ser != '':
                    if ser.getCTS():
                        res = TOOLS.atcmd('AT', ser, False)
                        if 'ok' in res.lower():
                            D = TOOLS.getINI('parameters.ini')
                            TOOLS.atcmd('AT+CPIN='+ D['pin'], ser, False)
                            pin = TOOLS.atcmd('AT+CPIN?',ser, False)
                            if 'READY' in pin:
                                print '\n', data, "is connected to the Telit modem and Pin code is initialized."
                            else:
                                print '\n', data, "is connected to the Telit modem and Pin code is not initialized."
                            if 'cocdcacm' in name.lower():
                                ser_usb = ser
                            elif 'serial' in name.lower():
                                ser_serial = ser
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
    D = TOOLS.getINI('parameters.ini')
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
    

def atcmd(cmd, ser, dis=True):
    ''' Send AT command (cmd) on the serial port (ser) displaying by default the result
        Return the echo and the result of the AT command (see ATE0\r for enable/disable the echo)
    '''
    # Write AT command in hte output buffer
    ser.write(cmd + '\r')
    # Wait Telit to write in the input buffer
    TOOLS.sleep(1)
    res = ''
    # While there is something in the input buffer add it to res
    while ser.inWaiting()>0:
        i = 0
        while i < 512:
            i+=1
            res += ser.read(16)
            if not ser.inWaiting()>0 or 'OK' in res:
                break
    if dis:
        print res
    # If we have an at#wscript
    if 'at#wscript' in cmd.lower():
        script = cmd.split('"')
        D = TOOLS.getINI('parameters.ini')
        with open(D['path']+ '\\' + script[1], 'rb') as f:
            start = float(time.time())
            print 'Uploading:', script[1]
            ser.write(f.read())
            TOOLS.sleep(1)
            res = ser.read()
            while not 'OK' in res:
                res += ser.read()
            print 'End after {0} secondes'.format(float(time.time()-start))
            print res
    if 'at#execscr' in cmd.lower():
        i = 0
        prev = ''
        while i < 256:
            i+=1
            res = prev + ser.read(256)
            try:
                split = res.rsplit('\n', 1)
                if split[0] !=  '':
                    print split[0]
                prev = split[1]
            except IndexError:
                if res != '':
                    print res
                pass
            TOOLS.sleep(15)
    return res

def count_LF(string):
    return string.count('\n')

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
        if '=' in line:
            line = line.rstrip('\r\n')
            parts = line.split('=')
            D[parts[0]] = parts[1]
    f.close()
    return D
    
    