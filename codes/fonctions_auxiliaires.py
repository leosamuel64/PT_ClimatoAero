import datetime
import matplotlib.pyplot as plt


def incr_dico(dico,key,value):
    '''
    Entrée : Dictionnaire, Clé, Valeur
    Procedure : Augmente Dictionnaire[Clé] de Valeur
    '''
    if key in dico.keys():
        dico[key]+=value
    else:
        dico[key]=value

def convert_date(mot):
        annee=int(mot[0]+mot[1]+mot[2]+mot[3])
        mois=int(mot[4])*10+int(mot[5])
        jour=int(mot[6])*10+int(mot[7])
        heure=int(mot[8])*10+int(mot[9])
        return datetime.datetime(annee,mois,jour,heure)
    
def convert_heure(mot,d):
    if len(mot)==3:
        heures=int(mot[0])
        minutes=int(mot[1])*10+int(mot[2])
    elif len(mot)==4:
        heures=int(mot[0])*10+int(mot[1])
        minutes = int(mot[2])*10+int(mot[3])
    elif len(mot)==2:
        heures=0
        minutes = int(mot[0])*10+int(mot[1])
    elif len(mot)==1:
        heures=0
        minutes=int(mot[0])
    else:
        return None
    annee = d.year
    mois = d.month
    jour = d.day
    if heures==23:
        return datetime.datetime(annee,mois,jour,heures,minutes)-datetime.timedelta(1)
    else:
        return datetime.datetime(annee,mois,jour,heures,minutes)
        
def convert_float(valeur):
    if valeur=='':
        return 0.0
    else:
        return float(valeur.replace(',','.'))

def convert_int(valeur):
    if valeur=='':
        return 0
    else:
        return int(valeur)

def ajoute_debut(t,val):
    temp = [-1 for _ in range(len(t)+1)]
    temp[0]=val
    for k in range (1,len(t)+1):
        temp[k]=t[k-1]
    return temp

def format_temp_date(t,suff):
    temp = []
    for x in t:
        match x:
            case (a,b):
                temp.append(str(a)+suff+'\n ('+str(b)+')')
            case a:
                temp.append(str(a)+suff)
    return temp

def sort_mois_temp(data,intervalle_heure=[]):
    '''
    Entrée : Liste des observations, Intervalle des heures à prendre en compte (pour exclure la nuit)
    Sortie : Dictionnaire des moyennes de température par mois
    '''
    res = {i:[] for i in range(1,13)}
    cnt = {i:0 for i in range(1,13)}
    for d in data:
        mois = d.date.month
        heure = d.date.hour
        temp = d.temperature
        
        if intervalle_heure != [] and heure>=intervalle_heure[0] and heure<=intervalle_heure[1]:
            res[mois].append((temp,d.date.year))
        elif intervalle_heure == []:
            res[mois].append((temp,d.date.year))
    return res

def tableau_climato(data, fonction):
    valeurs = sort_mois_temp(data)
    res=[]
    for i in range(1,13):
        res.append(fonction(valeurs[i]))
    return res
    
def moyenne(t):
    return sum(t)/len(t)

def tableau_moyenne(data):
    valeurs = sort_mois_temp(data)
    res=[]
    
    for i in range(1,13):
        somme=0
        for (temp,_) in valeurs[i]:
            somme+=temp
        res.append(round(somme/len(valeurs[i]),2))
        
    return res

def round_wind(wind_deg):
    '''
    Entrée : Direction du vent en °
    Sortie : Vent correspondant à la piste
    '''
    res=round(wind_deg/10)
    return res

        
def assoc_temps_present(path):
    '''
    Entrée : Chemin vers fichier code temps present
    Sortie : Dictionnaire code -> Description
    '''
    file=open(path,'r')
    res = {}
    for ligne in file:
        code,descr = ligne.strip().split(';')
        res[int(code)]=descr
    return res

def addlabels(x,y,suff):
    """
    Entrée : liste des abscices, liste des ordonnées, ajout d'un suffixe en haut de la barre
    Sortie : Ajoute la valeur en haut de la barre 
    """
    for i in range(len(x)):
        plt.text(i,y[i],str(round(y[i],1))+suff,ha = 'center')