#-*- coding:utf-8 -*-

import UTILS
import serial
import _winreg

D = UTILS.getINI('parameters.ini')

try:
    i = 0
    key = 0
    key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, D['registry_path'], 0, _winreg.KEY_READ)
    while(1):
        name, data, type = _winreg.EnumValue(key, i)
        i+=1
        print 'plou'
        UTILS.open_ser(data)
    
except serial.SerialException:
    print 'ploup'
    pass
except UnicodeDecodeError:
    print 'ploup2'
    pass
except WindowsError:
    print 'ploup3'
    print 'End of list'
    exit(0)
else:
    pass