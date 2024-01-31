from codes.construction_bases import *
from codes.fonctions_auxiliaires import *
from codes.classes import *
from codes.calculs import *
from codes.affichages import *

from codes.config import *


data = charge_fichier('data/LFBR.data')
# metars = build_dict_metar(chemin_Metars)
# 

print('DEBUT CODE')

# --------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------
# --------------------------------------- CODE -----------------------------------------
# --------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------


# trace_tableau_qnh(data)

ad= aerodrome('LFBO')
ac = avion('PIVI')
trace_limitations(data,ac,ad)
            
            
            
            

        
            


            
    




    



        