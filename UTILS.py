import time
import _winreg
import serial

def open_ser_list(registry_path):
    try:
        key = 0
        key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, registry_path, 0, _winreg.KEY_READ)
        i=0
        while(1):
            try:
                name, data, type = _winreg.EnumValue(key, i)
                open_ser(data)
                i+=1
            except WindowsError:
                print 'End of list'
                exit(0)
        _winreg.CloseKey(key)
    except WindowsError, w:
        print 'WRONG KEY REGISTRY:', w

def open_ser(port):
    D = getINI('parameters.ini')
    try:
        # ser = serial.Serial(int(D['port_number'])-1, int(D['baudrate']), timeout=0)
        print 'youhou'
        ser = serial.Serial(port, int(D['baudrate']), timeout=0)
    except serial.SerialException, s:
        print 'BUSY PORT:', s
        exit(1)
    except AttributeError, a:
        print 'ATTRIBUTE ERROR:', a
        exit(1)
    except NameError, n:
        print 'NAME ERROR:', n
        exit(1)
        
def atok(ser):
    ser.write('AT\r')
    UTILS.sleep(1)
    start=time.time()
    while ser.inWaiting()>0:
        res = ser.read(888)
        print res
    print 'End after {0} secondes\n'.format(float(time.time()-start))
    if 'OK' in res:
        print "\nThe port " + ser.portstr +  " is open."
    else:
        print "\nThe port " + ser.portstr +  " is not open."    
def sleep(tenthOfSec):
    '''Make a pause in the script in tenth of second.
    '''
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