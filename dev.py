from codes.construction_bases import *
from codes.fonctions_auxiliaires import *
from codes.classes import *
from codes.fonctions_auxiliaires_mto import *
from codes.calculs import *
from codes.affichages import *

from config import *


data = charge_fichier(chemin_observations)
metars = build_dict_metar(chemin_Metars)


# print(count_weather_date(metars,'RA'))
# trace_phenomene(metars,'FG')
# plot_weather(metars,seuil=0.05)
# print(count_weather_date(metars,'-RA'))

    
# pourcentage_temps_present(data,'code_temps_present.csv',affichage=True)
# rose_des_vents(data,[30,12])
# plot_temp(data)




    



        