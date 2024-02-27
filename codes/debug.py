from codes.construction_bases import *
from codes.fonctions_auxiliaires import *
from codes.classes import *
from codes.calculs import *
from codes.affichages import *

from codes.config import *
from codes.export import *

def debug_vent(data,conf, decli=0):
    """
    Entrée : Liste des observations, declinaison magnétique
    Sortie : Dictionnaire des listes des vitesses de vent
    """
    res={}
    cnt=0
    for d in data:
        direct = d.direction_vent
        sp = d.vitesse_vent
        if (not ('direction_vent' in d.a_donnees_manquantes())) and (not (direct == '')) and (not ('vitesse_vent' in d.a_donnees_manquantes())) and (not (sp == '')):
            wr = round_wind(direct-decli) % 36
            
            # [170;220]
            if wr>=17 and wr<=22 and sp>3 and d.date.month in [6,7,8]:  # Reglage dans le if
                # print('vent du {dir} pour {vitesse}kt le {date}'.format(dir=wr*10,vitesse=round(sp,0),date=d.date))
                incr_dico(res,d.date.hour,1)
                cnt+=1
    X=[]
    Y=[]
    for key in res.keys():
        X.append(str(key)+'h')
        Y.append(100*res[key]/cnt)
    
    plt.bar(X, Y, color=color_template().orange)
    # addlabels(X, Y, 'j')
    plt.title("Vent entre 170 et 220° en fonction de l'heure")
    plt.ylabel('Fréquence (%)')
    plt.xlabel('Heure (h)')
    plt.savefig(
        'Figures_raw/'+conf.chemin_observations[-9:-5]+'/vent_Sud.svg', format='svg')
    if config.SHOW:
        plt.show()
    plt.close('all')
    
def debug_visi(data,conf, decli=0):
    """
    Entrée : Liste des observations, declinaison magnétique
    Sortie : Dictionnaire des listes des vitesses de vent
    """
    res={}
    cnt=0
    for d in data:
        visi = d.visi
        if (not ('visi' in d.a_donnees_manquantes())) and (not (visi == '')):
            
            # [170;220]
            if visi<1000:  # Reglage dans le if
                # print('vent du {dir} pour {vitesse}kt le {date}'.format(dir=wr*10,vitesse=round(sp,0),date=d.date))
                incr_dico(res,d.date.hour,1)
                cnt+=1
    X=[]
    Y=[]
    for key in res.keys():
        X.append(key)
        Y.append(100*res[key]/cnt)
        
    plt.bar(X, Y, color=color_template().orange)
    # addlabels(X, Y, 'j')
    plt.title("Fréquence de visibilité < 1000m")
    plt.ylabel('Fréquence (%)')
    plt.xlabel('Heure (h)')
    
    plt.savefig(
        'Figures_raw/'+conf.chemin_observations[-9:-5]+'/visi<5000.svg', format='svg')
    if config.SHOW:
        plt.show()
    plt.close('all')
        