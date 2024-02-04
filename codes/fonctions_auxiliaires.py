import datetime
import matplotlib.pyplot as plt


def incr_dico(dico, key, value):
    '''
    Entrée : Dictionnaire, Clé, Valeur
    Procedure : Augmente Dictionnaire[Clé] de Valeur
    '''
    if key in dico.keys():
        dico[key] += value
    else:
        dico[key] = value


def convert_date(mot):
    '''
    Entrée : date au format observation
    Procedure : Augmente Dictionnaire[Clé] de Valeur
    '''
    annee = int(mot[0]+mot[1]+mot[2]+mot[3])
    mois = int(mot[4])*10+int(mot[5])
    jour = int(mot[6])*10+int(mot[7])
    heure = int(mot[8])*10+int(mot[9])
    return datetime.datetime(annee, mois, jour, heure)


def convert_heure(mot, d):
    """
    Entrée : une str de la date, observation
    Sortie : Renvoie l'heure (str) en format datetime
    """
    if len(mot) == 3:
        heures = int(mot[0])
        minutes = int(mot[1])*10+int(mot[2])
    elif len(mot) == 4:
        heures = int(mot[0])*10+int(mot[1])
        minutes = int(mot[2])*10+int(mot[3])
    elif len(mot) == 2:
        heures = 0
        minutes = int(mot[0])*10+int(mot[1])
    elif len(mot) == 1:
        heures = 0
        minutes = int(mot[0])
    else:
        return None
    annee = d.year
    mois = d.month
    jour = d.day
    if heures == 23:
        return datetime.datetime(annee, mois, jour, heures, minutes)-datetime.timedelta(1)
    else:
        return datetime.datetime(annee, mois, jour, heures, minutes)


def convert_float(valeur):
    """
    Entrée : str du fichier .data
    Sortie : Renvoie valeur en str '' OU float
    """
    if valeur == '':
        return ''
    else:
        return float(valeur.replace(',', '.'))


def convert_int(valeur):
    """
    Entrée : str du fichier .data
    Sortie : Renvoie valeur en str:'' OU int
    """
    if valeur == '':
        return ''
    else:
        return int(valeur)


def ajoute_debut(t, val):
    """
    Entrée : liste, valeur
    Sortie : Renvoie liste avec valeur au début
    """
    temp = [-1 for _ in range(len(t)+1)]
    temp[0] = val
    for k in range(1, len(t)+1):
        temp[k] = t[k-1]
    return temp


def format_temp_date(t, suff):
    """
    Entrée : liste des couples (valeur, date), str
    Sortie : Renvoie la liste des couples (valeur+str, date)
    """
    temp = []
    for x in t:
        match x:
            case (a, b):
                temp.append(str(a)+suff+'\n ('+str(b)+')')
            case a:
                temp.append(str(a)+suff)
    return temp


def tableau_climato_temp(valeurs, fonction):
    """
    Entrée : Dictionnaire des température par mois (max, min), fonction de comparaison
    Sortie : Renvoie la liste des températures pliées selon fonction
    """
    res = []
    for i in range(1, 13):
        res.append(fonction(valeurs[i]))
    return res


def tableau_climato_qnh(valeurs, fonction):
    """
    Entrée : Dictionnaire des qnh par mois (max, min), fonction de comparaison
    Sortie : Renvoie la liste des températures pliées selon fonction
    """
    res = []
    for i in range(1, 13):
        res.append(fonction(valeurs[i]))
    return res


def moyenne(t):
    """
    Entrée : liste de float/int
    Sortie : moyenne de la liste
    """
    return sum(t)/len(t)


def tableau_moyenne_temp(valeurs):
    """
    Entrée : liste des températures
    Sortie : moyenne de la liste des valeurs
    """
    res = []
    for i in range(1, 13):
        somme = 0
        for (temp, _) in valeurs[i]:
            somme += temp
        res.append(round(somme/len(valeurs[i]), 2))
    return res


def tableau_moyenne_qnh(valeurs):
    """
    Entrée : liste des qnh
    Sortie : moyenne de la liste des valeurs
    """
    res = []
    for i in range(1, 13):
        somme = 0
        for (temp, _) in valeurs[i]:
            somme += temp
        res.append(round(somme/len(valeurs[i]), 0))
    return res


def round_wind(wind_deg):
    '''
    Entrée : Direction du vent en °
    Sortie : Vent correspondant à la piste
    '''
    res = round(wind_deg/10)
    return res


def assoc_temps_present(path):
    '''
    Entrée : Chemin vers fichier code temps present
    Sortie : Dictionnaire code -> Description
    '''
    file = open(path, 'r')
    res = {}
    for ligne in file:
        code, descr = ligne.strip().split(';')
        res[int(code)] = descr
    return res


def addlabels(x, y, suff):
    """
    Entrée : liste des abscices, liste des ordonnées, ajout d'un suffixe en haut de la barre
    Sortie : Ajoute la valeur en haut de la barre 
    """
    for i in range(len(x)):
        plt.text(i, y[i], str(round(y[i], 1))+suff, ha='center')


def normalise_matrice(m):
    """
    Entrée : Matrice à valeurs positives
    Sortie : Matrice avec des pourcentages pour valeurs 
    """
    somme = 0
    for i in range(len(m)):
        for j in range(len(m[0])):
            somme += m[i][j]

    for i in range(len(m)):
        for j in range(len(m[0])):
            m[i][j] = round(100*m[i][j]/somme, 2)


def enleve_doublon(liste):
    '''
    Entrée : Liste de couple
    Sortie : liste des couples sans doublon du deuxieme element (_,b) [b unique]
    '''
    res=[]
    double=[]
    for (a,b) in liste:
        if not(b in double):
            res.append((a,b))
            double.append(b)
    return res

def inferieur_a(a,b):
    '''
    Entrée : a,b entiers ou floats
    Sortie : bool a<b
    '''
    return a<b    

def superieur_a(a,b):
    '''
    Entrée : a,b entiers ou floats
    Sortie : bool a>b
    '''
    return a>b 

def facto(n):
    match n:
        case 0:
            return 1
        case 1:
            return 1
        case n:
            return n*facto(n-1)