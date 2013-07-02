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

D = UTILS.getINI('parameters.ini')

disp = 1
while 1:
    if disp == 1:
        print """
    Enter AT command (default)
    1-AT commands sample
    2-Exit
    """
        disp = 0
    cmd = raw_input(">")
    try:
        cmd = int(cmd)
    except ValueError:
        UTILS.atcmd(cmd, ser)
    else:
        if cmd == 1:
            while 1:
                disp = 1
                print """
    1-Signal quality
    2-Upload script
    3-Enable script & Execute
    4-Shutdown
    5-List files
    6-Delete files
    7-Disable Watchdog
    8-Watchdog ?
    9-Which file is enabled
    10-Readscript
    11-Menu
    """
                try:
                    case = int(raw_input("What do you want to:\n >>  "))
                except ValueError:
                    print 'Please enter an integer ...'
                    pass
                else:
                    if case == 1:
                        UTILS.atcmd('AT+CSQ', ser)
                    elif case == 2:
                        UTILS.atcmd('AT#WSCRIPT=\"'+D['upload']+ '\",' +str(size()), ser, True, True)
                    elif  case == 3:
                        UTILS.atcmd('AT#ESCRIPT="'+D['exe']+ '\"', ser)
                        UTILS.atcmd('AT#EXECSCR', ser)
                        UTILS.sleep(3)
                        while ser.inWaiting() > 0:
                            res = ser.read(10000)
                            print res
                    elif  case == 4:
                        UTILS.atcmd('AT#SHDN', ser)
                        print "Telit is off, bye !"
                    elif  case == 5:
                        UTILS.atcmd('AT#LSCRIPT', ser)
                    elif  case == 6:
                        UTILS.atcmd('AT#DSCRIPT=\"'+D['delete']+ '\"', ser)
                    elif  case == 7:
                        UTILS.atcmd('AT#ENHRST=0', ser)
                    elif  case == 8:
                        UTILS.atcmd('AT#ENHRST?', ser)
                    elif  case == 9:
                        UTILS.atcmd('AT#ESCRIPT?', ser)
                    elif  case == 10:
                        UTILS.atcmd('AT#RSCRIPT=\"'+ D['upload'] +'\"', ser)
                    elif  case == 11:
                        break
                    else:
                        print "Please ...\r\n"
                        pass
                        
        elif cmd == 2:
            break
        else:
            print "Please ...\r\n"
            pass

ser.close()             # close port

