#-*- coding:utf-8 -*-
import time
import _winreg
import serial
import os
import UTILS
import time


def test_connexion(port, ser):
    ''' Check the connexion Telit-computer and if connected, initialize pin code.
        Take result of AT\r response, current port tested and current serial connexion.
        Return the state of the connexion (True or False)
    '''
    D = UTILS.getINI('parameters.ini')
    UTILS.atcmd('+++', ser, False)
    res = UTILS.atcmd('AT', ser, False)
    conn = False
    if 'OK' in res:
        conn = True
        UTILS.atcmd('AT+CPIN='+ D['pin'], ser, False)
        pin = UTILS.atcmd('AT+CPIN?',ser, False)
        if pin.find('READY') != -1:
            print '\n', port, "is connected to the Telit modem and Pin code is initialized."
        else:
            print '\n', port, "is connected to the Telit modem and Pin code is not initialized."
    else:
        print port +  " is not connected to the Telit modem."
        pass
    return conn


def open_ser_list(registry_path):
    ''' Take data from the registry for the serial port and try each COM port until AT test is OK.
        Return the serial port conected to the Telit
    '''
    ser =''
    try:
        key = 0
        key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, registry_path, 0, _winreg.KEY_READ)
        i = 0
        while(1):
            try:
                name, data, type = _winreg.EnumValue(key, i)
                i+=1
                ser = UTILS.open_ser(data)
            # Raise a SerialException which raise a UnicodeException with 'accès refusé'.
            # Replacing %s,%s by %r,%r line 59 of seriawin32.py would correct it.
            except UnicodeDecodeError, u:
                print data, 'is already used.'
                pass
            # Raised at the end of the list.
            except WindowsError:
                print 'The modem is not connected, check the cable or the drivers'
                exit(0)
            else:
            # Send an escape sequence in case the modem is not in command mode
                con = UTILS.test_connexion(data, ser)
                if con:
                    break
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
        ser = serial.Serial(port, int(D['baudrate']), timeout=0)
        # res = UTILS.atcmd('AT', ser, True)
    except serial.SerialException, s:
        print 'BUSY PORT:', s
    except AttributeError, a:
        print 'ATTRIBUTE ERROR:', a
    except NameError, n:
        print 'NAME ERROR:', n
    else:
        pass
    return ser
    
    
def atcmd(cmd, ser, dis=True, wscript = False, script = ''):
    ''' Send AT command (cmd) on the serial port (ser) displaying by default the result
        Return the echo and the result of the AT command (see ATE0\r for enable/disable the echo)
    '''
    ser.write(cmd + '\r')
    UTILS.sleep(1)
    # start = time.time()
    res = ''
    # While buffer has something in it
    while ser.inWaiting() > 0:
        res = ser.read(888)
        if dis:
            print res
    # If we have a wscript prompt
    if wscript:
        D = UTILS.getINI('parameters.ini')
        with open(D['path']+ script, 'rb') as f:
            ser.write(f.read())
            UTILS.sleep(1)
            while not res.find('OK'):
                res = ser.read(888)
        # print 'End after {0} secondes'.format(float(time.time()-start), 0.00)
    return res


def sleep(tenthOfSec):
    ''' Make a pause in the script in tenth of second '''
    sec = float(float(tenthOfSec)/10.0)
    time.sleep(sec)
    return 0


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
    
    