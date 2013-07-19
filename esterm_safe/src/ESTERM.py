#-*- coding:utf-8 -*-
import TOOLS
import os
import threading


class Proc(threading.Thread):
    ''' Class to monitor debug file with thread on debug port.
        In registry path (see parameters.ini) cdcacm1 is the debug port by default'''
    def __init__(self):
        threading.Thread.__init__(self)
        self.encours=False
    def run(self):
        self.encours=True
        while self.encours:
            if ser_debug != '':
                import time
                title = time.time()
                file = open(str(title), 'wb')
                TOOLS.sleep(1)
                while 1:
                    try:
                        res = ser_debug.read(2048)
                        if res != '':
                            file.write(res)
                    except KeyboardInterrupt:
                        file.close()
                        self.stop()
                        break
            else:
                self.stop()
                break
    def stop(self):
        self.encours=False


# Change color of text
os.system("color 0A")
# Enter parameters.ini in D
D = TOOLS.getINI('parameters.ini')

def size(u):
    '''Give size of the file in path upload (see parameters.ini)'''
    p = D['path']  + "\\"
    res = ''
    try:
        res = int(os.path.getsize(p + u))
    except WindowsError:
        print "\nVerify file name or path of: " + p + u
        pass
    return res


disp = 1 # Enable menu display
run_thread = False # Binary file monitoring disabled
start = 1 # Enable start

while 1:
    if start == 1:
        ser, ser_debug = TOOLS.open_ser_list(D['registry_path'])  
    start = 0
    # Monitor the binary file on the debug port
    if run_thread == True:
        fileDbg = Proc()
        fileDbg.start()
        run_thread = False

    if disp == 1:
        if ser != '':
            print '\n      ', ser.port, 'connected'
        print """      Welcome to Esterm !
    --------------------------------------------------------
    | 1-AT commands sample                                 |
    | 2-Upload                                             |
    | 3-Compile all & Delete all & Upload all scripts      |
    | Ctrl+C start Esterm again                            |
    |------------------------------------------------------|
    | 'Menu' to display it                                 |
    --------------------------------------------------------
    """
        disp = 0
    try:
        cmd = raw_input(">")
        cmd = int(cmd)
    # CTRL + C is recognized as a keyboard interupt
    except KeyboardInterrupt:
        print "Starting Esterm again ..."
        ser.close()
        start = 1
        disp = 1
    except ValueError:
        # Interpret string as AT command
        if cmd.lower() != 'menu':
            TOOLS.atcmd(cmd, ser)
        else:
            disp = 1
    else:          
        if cmd == 1:
            while 1:
                disp = 1
                print """
    ---------------------------
    0-Delete all script
    1-Signal quality
    2-Enable script & Execute
    3-Execute
    --------------------------
    4-Readscript
    5-List files
    6-Delete files
    --------------------------
    7-File enabled ?
    8-Watchdog ?
    9-Disable Watchdog
    --------------------------
    10-Shutdown
    11-Reboot
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
                    if case == 0:
                        sure = raw_input("Delete all script, are you sure Guy ? o/n\n")
                        if 'o' in sure.lower():
                            res = TOOLS.atcmd('AT#LSCRIPT', ser, False)
                            # List the script find in AT#LSCRIPT and delete them one by one
                            script = TOOLS.lscript(res)
                            for s in script:
                                TOOLS.atcmd('AT#DSCRIPT=\"'+ s + '\"', ser)
                        else:
                            disp = 1
                            break
                    elif case == 1:
                        TOOLS.atcmd('AT+CSQ', ser)
                    elif  case == 2:
                        try:
                            res = TOOLS.atcmd('AT#LSCRIPT', ser, False)
                            print TOOLS.lscript(res)
                            script = str(raw_input("Which script:\n >>  "))
                            TOOLS.atcmd('AT#ESCRIPT="'+script+ '\"', ser)
                            TOOLS.atcmd('AT#EXECSCR', ser)
                        except KeyboardInterrupt:
                            break
                    elif  case == 3:
                        try:
                            TOOLS.atcmd('AT#EXECSCR', ser)
                        except KeyboardInterrupt:
                            break
                    elif  case == 4:
                        while 1:
                            try:
                                res = TOOLS.atcmd('AT#LSCRIPT', ser, False)
                                print TOOLS.lscript(res)
                                script = str(raw_input("Which script:\n >>  "))
                                TOOLS.atcmd('AT#RSCRIPT=\"'+ script +'\"', ser)
                            except KeyboardInterrupt:
                                break
                    elif  case == 5:
                        TOOLS.atcmd('AT#LSCRIPT', ser)
                    elif  case == 6:
                        while 1:
                            try:
                                script = str(raw_input("Separate script by space:\n >>  "))
                                script = script.split(' ')
                                for s in script:
                                    TOOLS.atcmd('AT#DSCRIPT=\"'+ s + '\"', ser)
                                disp = 1
                                pass
                            except KeyboardInterrupt:
                                disp = 1
                                break
                    elif  case == 7:
                        TOOLS.atcmd('AT#ESCRIPT?', ser)
                    elif  case == 8:
                        TOOLS.atcmd('AT#ENHRST?', ser)
                    elif  case == 9:
                        TOOLS.atcmd('AT#ENHRST=0', ser)
                    elif  case == 10:
                        TOOLS.atcmd('AT#SHDN', ser)
                        print "Telit is off, bye !"
                    elif  case == 11:
                        TOOLS.atcmd('AT#REBOOT', ser)
                        print "Telit is rebooting ..."
                    else:
                        print "Please ...\r\n"
        elif cmd == 2:
            while 1:
                try:
                    # "" for the command for space in name folders
                    os.system("python -m compileall " + "\"" + D['path'] + "\"" )
                except ValueError:
                    print 'Wrong path for', D['path'] + D['compile_all']
                    pass
                try:
                    print "\nFile from "+ D['path'] + '\\'
                    print TOOLS.file_dir(D['path'])
                    s = raw_input("Script ?")
                    TOOLS.atcmd('AT#WSCRIPT=\"'+ s + '\",' +str(size(s)), ser)
                    disp = 1
                    break
                except KeyboardInterrupt:
                    disp = 1
                    break
        elif cmd == 3:
            while 1:
                try:
                    # "" for the command for space in name folders
                    os.system("python -m compileall " + "\"" + D['path'] + "\"" )
                except ValueError:
                    print 'Wrong path for', D['path'] + D['compile_all']
                    pass
                try:
                    print "\nFile from "+ D['path'] + '\\'
                    print TOOLS.file_dir(D['path'])
                    sure = raw_input("Delete all (in Telit) and add all (from specified path) scripts, are you sure ? o/n\n")
                    if 'o' in sure.lower():
                        res = TOOLS.atcmd('AT#LSCRIPT', ser, False)
                        # List the script find in AT#LSCRIPT and delete them one by one
                        dscript = TOOLS.lscript(res)
                        for s in dscript:
                            TOOLS.atcmd('AT#DSCRIPT=\"'+ s + '\"', ser)
                        upscript = TOOLS.file_dir(D['path'])
                        for s in upscript:
                            TOOLS.atcmd('AT#WSCRIPT=\"'+ s + '\",' +str(size(s)), ser)
                        disp = 1
                        break
                    else:
                        disp = 1
                        break
                except KeyboardInterrupt:
                    disp = 1
                    break
        elif cmd == 4:
            while 1:
                try:
                    # "" for the command for space in name folders
                    os.system("python -m compileall " + "\"" + D['path'] + "\"" )
                except ValueError:
                    print 'Wrong path for', D['path'] + D['compile_all']
                    pass
                try:
                    print "\nFile from "+ D['path'] + '\\'
                    print TOOLS.file_dir(D['path'])
                    script = str(raw_input("Separate script by space:\n >>  "))
                    script = script.split(' ')
                    for s in script:
                        TOOLS.atcmd('AT#WSCRIPT=\"'+ s + '\",' +str(size(s)), ser, True)
                    disp = 1
                    break
                except KeyboardInterrupt:
                    disp = 1
                    break
        else:
            print "Please ...\r\n"

# close port
ser.close()
