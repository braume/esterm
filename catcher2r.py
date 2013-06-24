#-*- coding:utf-8 -*-

import UTILS
import serial
import _winreg

D = UTILS.getINI('parameters.ini')

try:
    i = 0
    key = 0
    # key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, registry_path, 0, _winreg.KEY_READ)
    name, data, type = _winreg.EnumValue(key, i)
    i+=1
    UTILS.open_ser(data)
    print 'plou'
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