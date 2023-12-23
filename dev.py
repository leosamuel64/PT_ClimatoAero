from codes.construction_bases import *
from codes.fonctions_auxiliaires import *
from codes.classes import *
from codes.fonctions_auxiliaires_mto import *
from codes.calculs import *
from codes.affichages import *

from codes.config import *


data = charge_fichier(chemin_observations)
# metars = build_dict_metar(chemin_Metars)
# 

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
        res.append(round(somme/len(valeurs[i]),2))
        
    return res
    
def calcul_tableau_temp(data):
    ()


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
                
            


def trace_tableau(column_labels,line_label,data_temp):
    '''
    Entrée : Liste des labels, liste de liste des données
    Sortie : Tableau
    '''
    data_temp_2=[]
    for t in data_temp:
        tableau = format_temp_date(t,'°C')
        data_temp_2.append(tableau)
    
    data = []
    for k in range(len(data_temp_2)):
        data.append(ajoute_debut(data_temp_2[k],line_label[k]))
        

        
    data_head = ajoute_debut(data,column_labels)
    colors = [[color_template().fond_table for _ in range(len(data_head[0])) ] for _ in range(len(data_head))]
    for k in range(len(colors[0])):
        colors[0][k]=color_template().orange
    fig, ax = plt.subplots(1, 1)
    # ax.axis("tight")
    ax.axis("off")
    table = ax.table(cellText=data_head, cellColours=colors, loc="center")
    table.auto_set_font_size(False)
    table.set_fontsize(5)
    plt.savefig('fig.svg',format='svg')
    
    plt.show()
# print(sort_mois_temp(data))

t_max = tableau_climato(data, max)
t_min = tableau_climato(data, min)
t_moy = tableau_moyenne(data)


trace_tableau(['-','Jan','Fev','Mars','Avr','Mai', 'Juin', 'Juil','Aout','Sept','Oct','Nov','Dec'],
              ['Max','Min', 'Moy'],
              [t_max,t_min,t_moy])



# calcul_tableau_temp(data)

# plot_weather(metars,0.2)
# trace_phenomene(metars,'-RA')


        