from codes.construction_bases import *
from codes.fonctions_auxiliaires import *
from codes.classes import *
from codes.calculs import *
from codes.affichages import *

from codes.config import *


data = charge_fichier('data/LFMT.data')
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



# reecrit_fichier_MT('data/backup_LFMT.data','data/LFMT.data')

            
            
# rose_des_vents(data)
            
for i in range(len(data)):
    if data[i].plafond()!=None and data[i].plafond()[2]=='':
        print(data[i].plafond())
            
            
            
            

        
            


            
    




    



        