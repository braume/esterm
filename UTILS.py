def getINI(fichier):
    # global D
    D = {}
    # fichier = '/sys/' + fichier
    # Ouverture du fichier
    f = open(fichier, 'r')
    # Lecture de la première ligne
    line = f.readline()
    # Tant qu'on est pas arrivé à la fin du fichier
    while (line != ''):
        # Si ce n'est pas la dernière ligne, on enlève le CRLF
        if (line.find('\r\n') != -1):
            line = line[0:line.find('\r\n')]
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