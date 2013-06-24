#-*- coding:utf-8 -*-
import UTILS

D = UTILS.getINI('parameters.ini')

UTILS.open_ser_list(D['registry_path'])
    
    
while 1:
    print """
    \t 1-AT 
    \t 2-Pinit
    \t 3-Signal quality 
    \t 4-Upload script & List files 
    \t 5-Enable script & Execute
    \t 6-Shutdown
    \t 7-Exit
    """
    try:
        case = int(raw_input("What do you want to:\n >>  "))
    except ValueError:
        case = 0
        
    if case == 0:
        print 'Please enter an integer ...'
    elif case == 1:
        UTILS.atcmd('AT\r')
    elif case == 2:
        UTILS.atcmd('AT+CPIN=\"'+D['pin']+'\"\r')
    elif case == 3:
        UTILS.atcmd('AT+CSQ\r')
    elif case == 4:
        UTILS.atcmd('AT#WSCRIPT=\"'+D['upload']+ ',' +UTILS.size() + ', 0\"\r')
    elif  case == 5:
        UTILS.atcmd('AT#ESCRIPT="'+D['exe']+ ',' +UTILS.size() + ', 0\"\r')
    elif  case == 6:
        UTILS.atcmd('AT#SHDN\r')
        print "Telit is off, bye !"
    elif  case == 7:
        print "Bye !\r\n"
        exit(0)
    else:
        print "Please ...\r\n"

ser.close()             # close port

