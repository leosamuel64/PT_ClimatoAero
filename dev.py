from codes.construction_bases import *
from codes.fonctions_auxiliaires import *
from codes.classes import *
from codes.calculs import *
from codes.affichages import *

from codes.config import *
from codes.export import *


# data = charge_fichier('data/LFBR.data')
# metars = build_dict_metar(chemin_Metars)
# 

# data = charge_fichier('data/obs/LFLN2.data')
# metars = build_dict_metar('data/metar/LFPM.txt')


# data = charge_fichier('data/obs/LFMK.data')
# data = charge_fichier('data/obs/LFMT.data')
# data = charge_fichier('data/obs/LFPM.data')



print('DEBUT CODE')

# --------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------
# --------------------------------------- CODE -----------------------------------------
# --------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------

flotte = ['TOBA',
          'TB20',
          'DA40',
          'DA42',
          'CP10',
          'B58',
          'PIVI'] 

phenomenes = ['BR',
              'RA',
              'FG',
              'TS']

liste_ad = ['LFBR','LFLN','LFLS','LFMK','LFMT','LFPM']

multi_exports(liste_ad,flotte,phenomenes)

            
    




    



        