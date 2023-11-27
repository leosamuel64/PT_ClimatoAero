from codes.construction_bases import *
from codes.fonctions_auxiliaires import *
from codes.classes import *
from codes.fonctions_auxiliaires_mto import *
from codes.calculs import *
from codes.affichages import *

from config import *


data = charge_fichier(chemin_observations)
# metars = build_dict_metar(chemin_Metars)


# --------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------
# --------------------------------------- CODE -----------------------------------------
# --------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------

import matplotlib.pyplot as plt
import numpy as np


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
        res.append(somme/len(valeurs[i]))
        
    return res
    
def calcul_tableau_temp(data):
    ()

# print(sort_mois_temp(data))
# print(tableau_climato(data, max,1))
print(tableau_climato(data, min))
# print(tableau_climato(data, moyenne,1))

# print(tableau_moyenne(data))

# calcul_tableau_temp(data)



        