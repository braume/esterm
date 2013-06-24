#-*- coding:utf-8 -*-
import time
import _winreg
import serial
import os
import UTILS

def open_ser_list(registry_path):
    ''' Take data for the serial port from the registry
        Try each COM port until AT test is OK and return the connected one
    '''
    ser =''
    try:
        key = 0
        key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, registry_path, 0, _winreg.KEY_READ)
        i=0
        D = UTILS.getINI('parameters.ini')
        while(1):
            try:
                name, data, type = _winreg.EnumValue(key, i)
                i+=1
                if 'OK' in UTILS.open_ser(data)[0]:
                    ser = serial.Serial(data, int(D['baudrate']), timeout=0)
                    break
            except UnicodeDecodeError, u:
                print name, data, type
                print 'UNICODE ERROR:', u, '\n'
                pass
            except WindowsError:
                print 'End of list'
                exit(0)
            else:
                pass
        _winreg.CloseKey(key)
    except WindowsError, w:
        print 'WRONG KEY REGISTRY:', w
    return ser
        

def open_ser(port):
    ''' Open a serial port with an atok test catching possible errors.
        Return :
            res -> ok if the AT test succeed, nothing otherwise.
            ser -> the last opened serial port
    '''
    D = UTILS.getINI('parameters.ini')
    res = ''
    ser = ''
    try:
        ser = serial.Serial(port, int(D['baudrate']), timeout=0)
        res = UTILS.atcmd('AT\r', ser)
        if 'OK' in res:
            print "Port " + ser.portstr +  " is connected to the Telit modem.\n"
        else:
            print "Port " + ser.portstr +  " is not connected to the Telit modem.\n"
    except serial.SerialException, s:
        print 'BUSY PORT:', s
    except AttributeError, a:
        print 'ATTRIBUTE ERROR:', a
    except NameError, n:
        print 'NAME ERROR:', n
    else:
        pass
    return res, ser
    
    
def atcmd(cmd, ser):
    ''' Generic send of AT command
        Return the echo and the result of the AT command (see ATE0\r for echo)
    '''
    ser.write(cmd)
    UTILS.sleep(1)
    start=time.time()
    res = ''
    # While buffer has something in it
    while ser.inWaiting() > 0:
        res = ser.read(888)
        print res
    print 'End after {0} secondes'.format(float(time.time()-start))
    return res
    
    
def size():
    '''Give size of the file in path upload'''
    p = D['path'][:-1]
    u = D['upload'][:-1]
    return int(os.path.getsize(p + u))

    
def sleep(tenthOfSec):
    ''' Make a pause in the script in tenth of second '''
    sec = float(float(tenthOfSec)/10.0)
    time.sleep(sec)
    return 0


def getINI(fichier):
    ''' Return a dictionary based on 'fichier' '''
    D = {}
    # fichier = '/sys/' + fichier
    # Ouverture du fichier
    f = open(fichier, 'r')
    # Lecture de la première ligne
    line = f.readline()
    # Tant qu'on est pas arrivé à la fin du fichier
    while (line != ''):
        # Si ce n'est pas la dernière ligne, on enlève le CRLF
        line = line[:-1]
        # S'il y a un commentaire en fin de ligne
        if (line.find('#') != -1):
            # On ne prend pas en compte le commentaire
            line = line[0:line.find('#')]
        # S'il y a un "=" dans la ligne
        if (line.find('=') != -1):
            # On découpe la ligne autour du "="
            parts = line.split('=')
            # On stocke tout dans le tableau (D['Code_pin'] = '0000')
            D[parts[0]] = parts[1]
        # On lit la ligne suivante
        line = f.readline()
    # Fermeture du fichier
    f.close()
    
    return D