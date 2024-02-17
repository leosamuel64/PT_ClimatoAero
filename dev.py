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
metars = build_dict_metar('data/metar/'+code_ad+'.txt')
om = obs_metar(data,metars)

ad = aerodrome(code_ad)


print('DEBUT CODE')

# --------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------
# --------------------------------------- CODE -----------------------------------------
# --------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------

ac = avion('TB20')

# trace_limitations(data,ac,ad,conf)

# affiche_tc_venteff_altip(data,conf,ad,15,5)
# affiche_tc_visi_plafond(data,conf,ad)

# export_all()

# affiche_tc_venteff_altip(data,conf,ad,15,5)

# rose_des_vents(data,conf)
# trace_limitations(data,ac,ad,conf)
    
# couple_contingence_visi_plafond_metar(metars,ad)
# affiche_tc_visi_plafond(metars,conf,ad)
# trace_limitations(data,ac,ad,conf)

# multi_exports(['LFBR'],config.flotte, config.phenomenes)

# print(obs_metars)

trace_limitations(data,om,ac,ad,conf)