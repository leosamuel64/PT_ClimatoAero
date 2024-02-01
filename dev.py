from codes.construction_bases import *
from codes.fonctions_auxiliaires import *
from codes.classes import *
from codes.calculs import *
from codes.affichages import *

from codes.config import *
from codes.export import *


# data = charge_fichier('data/LFBR.data')
# metars = build_dict_metar(chemin_Metars)

code_ad = 'LFBR'

conf=export(code_ad)

data = charge_fichier(conf.chemin_observations)
metars = build_dict_metar('data/metar/'+code_ad+'.txt')

ad=aerodrome(code_ad)


print('DEBUT CODE')

# --------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------
# --------------------------------------- CODE -----------------------------------------
# --------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------


# multi_exports(config.liste_ad,config.flotte,config.phenomenes)

            
    




    



        