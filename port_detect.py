import _winreg
import UTILS

D = UTILS.getINI('parameters.ini')

try:
    key=0
    print D['registry_path']
    test = D['registry_path']
    key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, test, 0, _winreg.KEY_READ)
    i=0
    while(1):
        try:
            name, data, type = _winreg.EnumValue(key, i)
            print name, data, type
            i+=1
        except WindowsError:
            print 'End of list'
            exit(0)
    _winreg.CloseKey(key)
except WindowsError, w:
    print 'WRONG KEY REGISTRY:', w