from codes.construction_bases import *
from codes.fonctions_auxiliaires import *
from codes.classes import *
from codes.calculs import *
from codes.affichages import *

from codes.config import *
from codes.export import *


code_ad = 'LFBR'

conf = export(code_ad)

data = charge_fichier(conf.chemin_observations)
# metars = build_dict_metar('data/metar/'+code_ad+'.txt')

ad = aerodrome(code_ad)


print('DEBUT CODE')

# --------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------
# --------------------------------------- CODE -----------------------------------------
# --------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------

ac = avion('PIVI')

# trace_limitations(data,ac,ad,conf)

# affiche_tc_venteff_altip(data,conf,ad)
# affiche_tc_visi_plafond(data,conf,ad)

# export_all()