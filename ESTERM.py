#-*- coding:utf-8 -*-
import UTILS
import os

D = UTILS.getINI('parameters.ini')
ser = UTILS.open_ser_list(D['registry_path'])
    
def size(u):
    '''Give size of the file in path upload'''
    p = D['path']
    res = ''
    try:
        res = int(os.path.getsize(p + u))
    except WindowsError:
        print 'Verify file name or path of: ' + p + u
        res = -1
    return res

D = UTILS.getINI('parameters.ini')

disp = 1
while 1:
    if disp == 1:
        print """
        Welcome to Esterm !
    --------------------------
    | 1-AT commands sample   |
    | 2-Upload script        |
    | Ctrl+C to exit         |
    --------------------------
    """
        disp = 0
    try:
        cmd = raw_input(">")
    except KeyboardInterrupt:
        break
        
    try:
        cmd = int(cmd)
    except ValueError:
        UTILS.atcmd(cmd, ser)
    else:
        if cmd == 1:
            while 1:
                disp = 1
                print """
    ---------------------------
    1-Signal quality
    2-Enable script & Execute
    3-Readscript
    --------------------------
    4-List files
    5-Delete files
    --------------------------
    6-Disable Watchdog
    7-Watchdog ?
    8-Which file is enabled
    --------------------------
    9-Shutdown
    --------------------------
    """
                try:
                    case = int(raw_input("What do you want to:\n >>  "))
                except ValueError:
                    print 'Please enter an integer ...'
                    pass
                except KeyboardInterrupt:
                    break
                else:
                    if case == 1:
                        UTILS.atcmd('AT+CSQ', ser)
                    elif  case == 2:
                        try:
                            script = str(raw_input("Which script:\n >>  "))
                            UTILS.atcmd('AT#ESCRIPT="'+script+ '\"', ser)
                            UTILS.atcmd('AT#EXECSCR', ser)
                        except KeyboardInterrupt:
                            break
                    elif  case == 3:
                        while 1:
                            try:
                                script = str(raw_input("Which script:\n >>  "))
                                UTILS.atcmd('AT#RSCRIPT=\"'+ script +'\"', ser)
                            except KeyboardInterrupt:
                                break
                    elif  case == 4:
                        UTILS.atcmd('AT#LSCRIPT', ser)
                    elif  case == 5:
                        while 1:
                            try:
                                script = str(raw_input("Which script:\n >>  "))
                                UTILS.atcmd('AT#DSCRIPT=\"'+script+ '\"', ser)
                            except KeyboardInterrupt:
                                break
                    elif  case == 6:
                        UTILS.atcmd('AT#ENHRST=0', ser)
                    elif  case == 7:
                        UTILS.atcmd('AT#ENHRST?', ser)
                    elif  case == 8:
                        UTILS.atcmd('AT#ESCRIPT?', ser)
                    elif  case == 9:
                        UTILS.atcmd('AT#SHDN', ser)
                        print "Telit is off, bye !"
                    else:
                        print "Please ...\r\n"
                        pass
        elif cmd == 2:
            while 1:
                try:
                    script = str(raw_input("Separate script by space:\n >>  "))
                    script = script.split(' ')
                    for s in script:
                        length = size(s)
                        if length == -1:
                            break
                        UTILS.atcmd('AT#WSCRIPT=\"'+ s + '\",' +str(length), ser, True, True)
                except KeyboardInterrupt:
                    disp = 1
                    break
        else:
            print "Please ...\r\n"
            pass

ser.close()             # close port

