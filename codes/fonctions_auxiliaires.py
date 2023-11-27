import datetime


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
