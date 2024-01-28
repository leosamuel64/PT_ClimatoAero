from codes.construction_bases import *
from codes.fonctions_auxiliaires import *
from codes.classes import *
from codes.calculs import *
from codes.affichages import *

from codes.config import *


data = charge_fichier(chemin_observations)
# metars = build_dict_metar(chemin_Metars)
# 

print('DEBUT CODE')

# --------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------
# --------------------------------------- CODE -----------------------------------------
# --------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------


# x = avion('TRIN')
# ad = aerodrome('LFBO')
# trace_limitations(data,x,ad,30)

def vents_dominants_vitesse(data):
    """
    Entrée : Liste des observations
    Sortie : Dictionnaire des listes des vitesses de vent
    """
    res={i:[] for i in range(0,36)}
    for d in data:
        
        direct = d.direction_vent
        sp=d.vitesse_vent
        wr=round_wind(direct)%36
        res[wr].append(sp)
    return res


affiche_tc_visi_plafond(data)
                
    




    



        