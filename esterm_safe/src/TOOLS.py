#-*- coding:utf-8 -*-
import time
import serial
import _winreg


def open_ser_list(registry_path):
    ''' Take list of port from the registry and try each one until connexion test are done.
        Return the debug port and the port conected to the Telit (if serial and usb connected, you can choose)
    '''
    try:
        key = 0
        ser_usb = ''
        ser_serial = ''
        ser_debug = ''
        i = 0
        while(1):
            try:
                # Open directory in registry in read mode
                key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, registry_path, 0, _winreg.KEY_READ)
                # Stock port information of line i
                name, data, type = _winreg.EnumValue(key, i)
                i+=1
            # Raised at the end of the port list.
            except WindowsError, w:
                # Choose the return value of ser
                if ser_usb != '' and ser_serial != '':
                    print '\nUSB:', ser_usb.port
                    print 'Serial: ', ser_serial.port
                    choice = int(raw_input('1-USB   2-SERIAL\n>'))
                    if choice == 1:
                        ser = ser_usb
                        break
                    elif choice == 2:
                        ser = ser_serial
                        break
                    else:
                        print 'Please ...'
                elif ser_usb == '' and ser_serial == '':
                    print 'Check the cable, the drivers or the port availability.\n'
                    try:
                        sleep(10)
                    except KeyboardInterrupt:
                        break
                    # Come back at the first line in register
                    i = 0
                else:
                    if ser_serial != '':
                        ser = ser_serial
                        break
                    else:
                        ser = ser_usb
                        break
            # Stock value of ser_usb, ser_serial, ser_debug if the connexion is valid
            else:
                ser = open_ser(data)
                if ser != '':
                    print 'getCTS', ser.getCTS(), data
                    # DEBUG
                    if 'cdcacm1' in name.lower():
                        ser_debug = ser
                        print 'DEBUG:', ser_debug.port, '\n'
                    # SERIAL (Traceo or classic)
                    if 'serial' in name.lower():
                        res = atcmd('AT', ser, False)
                        if 'traceoboard' in res.lower():
                            ser_serial = ser
                        if 'ok' in res.lower():
                            init_pin_dog(ser, name, data)
                            ser_serial = ser
                            print 'SERIAL:', ser_serial.port
                    # USB
                    if ser.getCTS() == True and 'cdcacm' in name.lower():
                        res = atcmd('AT', ser, False)
                        if 'ok' in res.lower():
                            init_pin_dog(ser, name, data)
                            ser_usb = ser
                            'USB:', ser_usb.port
                        else:
                            print data +  " is not connected to the Telit modem."    
                            pass
        # Close registry directory (=key)
        _winreg.CloseKey(key)
    # Error when registry path is not correct
    except WindowsError, w:
        print 'WRONG KEY REGISTRY:', w
        exit(0)
    return ser, ser_debug

def init_pin_dog(ser, name, data):
    ''' Function used after a successful AT OK test.
    Disable watch dog.
    Enter pin if not ready yet.
    '''
    atcmd('AT#ENHRST=0', ser, False)
    D = getINI('parameters.ini')
    atcmd('AT+CPIN='+ D['pin'], ser, False)
    pin = atcmd('AT+CPIN?',ser, False)
    if 'READY' in pin:
        print data, "is connected to the Telit modem and Pin code is initialized.\n"
    else:
        print data, "is connected to the Telit modem and Pin code is not initialized."
    return 0

def open_ser(port):
    ''' Open a serial port catching possible errors.
        Return the serial port.
    '''
    D = getINI('parameters.ini')
    ser = ''
    try:
        ser = serial.Serial(port, int(D['baudrate']), rtscts = int(D['hardware_control']), timeout = 0.01)
    # Raise a SerialException which raise a UnicodeException with 'accès refusé'.
    # Replacing %s,%s by %r,%r line 59 of seriawin32.py would correct it.
    except UnicodeDecodeError:
        print port, 'is already used.'
        pass
    except serial.SerialException, s:
        print 'BUSY PORT:', s
    except AttributeError, a:
        print 'ATTRIBUTE ERROR:', a
    except NameError, n:
        print 'NAME ERROR:', n
    except ValueError, v:
        print 'VALUE ERROR:', v
    finally:
        pass
    return ser
    

def atcmd(cmd, ser, dis=True):
    ''' Send AT command (cmd) on the serial port (ser) displaying by default the result
        Return the echo and the result of the AT command (see ATE0\r to disable echo)
    '''
    # Write AT command in the output buffer
    while 1:
        res = ''
        try:
            # \r necessary to specify command ending
            ser.write(cmd + '\r')
        except serial.SerialException, s:
            print s
            print 'Connexion was broken: use CTRL + C to start again\n'
            break
        except KeyboardInterrupt:
            break
        else:
            # Wait Telit to write in the input buffer
            sleep(1)
            # While there is something in the buffer read it
            i = 0
            try:
                res = ser.read(512)
                if 'OK' in res or 'ERROR' in res or '>>>' in res or '<<<' in res or 'traceo' in res:
                    if dis:
                        print res
                elif ser.inWaiting()>0:
                    print '1'
                    res = ser.read(512)
                    print res
                    print 'A script is running, try to connect again\n'
                    sleep(20)
                else:
                    print 'Telit is off or a script is running'
            except KeyboardInterrupt:
                break
            # If we have an at#wscript
            if 'at#wscript' in cmd.lower():
                script = cmd.split('"')
                # AT#WSCRIPT limitation
                if len(script[1])>16:
                    print 'Filename length is too long, please reduce it.'
                    break
                D = getINI('parameters.ini')
                try:
                    with open(D['path']+ "\\" + script[1], 'rb') as f:
                        start = float(time.time())
                        print 'Uploading:', script[1]
                        ser.write(f.read())
                        sleep(1)
                        res = ser.read()
                        while not 'OK' in res:
                            res += ser.read()
                        print 'End after {0} secondes'.format(float(time.time()-start)) + res
                except IOError:
                    print 'Write the name correctly'
                    # Wait a response from the Telit module to download next file
                    ser.write('AT\r')
                    sleep(1)
                    res = ser.read()
                    while not 'OK' in res:
                        res += ser.read()
                    print 'Downloading next file'
                    pass
            if 'at#execscr' in cmd.lower():
                D = getINI('parameters.ini')
                prev = ''
                while 1:
                    res = prev + ser.read(int(D['quantity']))
                    prev = ''
                    try:
                        # Cut at the first line feed from the right (last one)
                        split = res.rsplit('\n', 1)
                        cur = split[0]
                        prev = split[1]
                        if cur != '' and prev != '':
                            print cur
                            cur = ''
                        elif cur !=  '':
                            print cur
                            cur = ''
                        elif cur == '':
                            print '\n' + prev
                            prev = ''
                        else:
                            pass
                    except IndexError:
                        if res != '':
                            print res
                        pass
                    sleep(int(D['velocity']))
        break
    return res

def count_LF(string):
    return string.count('\n')

def sleep(tenthOfSec):
    ''' Make a pause in the script in tenth of second '''
    sec = float(float(tenthOfSec)/10.0)
    time.sleep(sec)
    return 0

def file_dir(raw_path):
    ''' Give files of the specified directory'''
    import os
    res = []
    for file in os.listdir(raw_path):
        if '.pyc' in file and not 'compileall' in file:
            res.append(file)
        elif '.ini' in file:
            res.append(file)
        else:
            pass
    return res
    
def lscript(rcmd):
    rcmd = rcmd.split('\"')
    res = []
    for r in rcmd:
        if ".pyc" in r:
            res.append(r)
        elif ".py" in r:
            res.append(r)
        elif ".bin" in r:
            res.append(r)
        elif ".ini" in r:
            res.append(r)
        elif ".txt" in r:
            res.append(r)
        else:
            pass
    return res

def getINI(file):
    ''' Return a dictionnary from file '''
    D={}
    # file = '/sys/' + file (while file in Telit)
    f = open(file)
    for line in f:
        if '=' in line:
            line = line.rstrip('\r\n')
            parts = line.split('=')
            D[parts[0]] = parts[1]
    f.close()
    return D
    
    