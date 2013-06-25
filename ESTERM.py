#-*- coding:utf-8 -*-
import UTILS
import os

D = UTILS.getINI('parameters.ini')
ser = UTILS.open_ser_list(D['registry_path'])

    
def size():
    '''Give size of the file in path upload'''
    p = D['path']
    u = D['upload']
    return int(os.path.getsize(p + u))
    
    
while 1:
    print """
    \t 1-AT
    \t 2-Pinit
    \t 3-Signal quality
    \t 4-Upload script
    \t 5-Enable script & Execute
    \t 6-Shutdown
    \t 7-List files
    \t 8-Delete files
    \t 9-Disable Watchdog
    \t 10-Watchdog ?
    \t 11-Which file is enabled
    \t 12-Exit
    """
    try:
        case = int(raw_input("What do you want to:\n >>  "))
    except ValueError:
        case = 0
    
    if case == 0:
        print 'Please enter an integer ...'
    elif case == 1:
        UTILS.atcmd('AT\r', ser)
    elif case == 2:
        UTILS.atcmd('AT+CPIN=\"'+D['pin']+'\"\r', ser)
    elif case == 3:
        UTILS.atcmd('AT+CSQ\r', ser)
    elif case == 4:
        UTILS.atcmd('AT#WSCRIPT=\"'+D['upload']+ '\",' +str(size()) + '\r',
                    ser, True, True)
    elif  case == 5:
        UTILS.atcmd('AT#ESCRIPT="'+D['exe']+ ',' +str(size()) + '\r', ser)
    elif  case == 6:
        UTILS.atcmd('AT#SHDN\r', ser)
        print "Telit is off, bye !"
    elif  case == 7:
        UTILS.atcmd('AT#LSCRIPT\r', ser)
    elif  case == 8:
        UTILS.atcmd('AT#DSCRIPT=\"'+D['delete']+ '\"\r', ser)
    elif  case == 9:
        UTILS.atcmd('AT#ENHRST=0\r', ser)
    elif  case == 10:
        UTILS.atcmd('AT#ENHRST?\r', ser)
    elif  case == 11:
        UTILS.atcmd('AT#ESCRIPT?\r', ser)
    elif  case == 12:
        print "Bye !\r\n"
        exit(0)
    else:
        print "Please ...\r\n"

ser.close()             # close port

