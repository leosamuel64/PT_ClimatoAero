from codes.construction_bases import *
from codes.fonctions_auxiliaires import *
from codes.classes import *
from codes.calculs import *
from codes.affichages import *

from codes.config import *
from codes.export import *

def debug_vent(data, decli=0):
    """
    Entrée : Liste des observations, declinaison magnétique
    Sortie : Dictionnaire des listes des vitesses de vent
    """
    res={}
    for d in data:
        direct = d.direction_vent
        sp = d.vitesse_vent
        if (not ('direction_vent' in d.a_donnees_manquantes())) and (not (direct == '')) and (not ('vitesse_vent' in d.a_donnees_manquantes())) and (not (sp == '')):
            wr = round_wind(direct-decli) % 36
            
            # [170;220]
            if wr>=17 and wr<=22 and sp>3 and d.date.month in [6,7,8]:  # Reglage dans le if
                # print('vent du {dir} pour {vitesse}kt le {date}'.format(dir=wr*10,vitesse=round(sp,0),date=d.date))
                incr_dico(res,d.date.hour,1)
    affiche_dico(res)