D={}
# file = '/sys/' + file (while file in Telit)
f = open("parameters.ini")
for line in f:
    if (line.find('=') != -1):
        line = line.rstrip('\r\n')
        parts = line.split('=')
        D[parts[0]] = parts[1]
        print D[parts[0]]
f.close()