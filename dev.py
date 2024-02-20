from codes.construction_bases import *
from codes.fonctions_auxiliaires import *
from codes.classes import *
from codes.calculs import *
from codes.affichages import *

from codes.config import *
from codes.export import *


code_ad = 'LFBR'

conf = export(code_ad)

# data = charge_fichier(conf.chemin_observations)
metars = build_dict_metar('data/metar/'+code_ad+'.txt')
# om = obs_metar(data,metars)

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

# trace_limitations(data,om,ac,ad,conf)

# cnt=0
# bug=0
# total=0
# for key in om.keys():
#     d,m = om[key]
#     if m!=[]:
#         obs = Metar.Metar(m.message)
#         obj = obs.wind_speed
#         data_val = d.vitesse_vent
#         if obj != None and data_val!='':
#             if abs(obj.value()-(data_val))>10:
#                 print(round(obj.value(),0),round(data_val,0),d.date)
#                 cnt+=1
#         else:
#             if obj==None:
#                 bug+=1
#     else:
#         bug+=1
#     total+=1
        
# print(100*cnt/(total),100*bug/(total*2),total)

# trace_phenomene(metars,'TS',conf)

def count_weather_date_liste(metars, l_code):
    '''
    Entrée : Liste des metars, code du phénomène
    Sortie : Dictionnaire Date -> Nombre d'heure du phenomene pour ce jour 
    '''
    res = {}
    date = metars[0].date
    for m in metars:
        obs = Metar.Metar(m.message)
        weather = obs.weather
        for groupe in weather:
            temp = ''
            for k in groupe:
                if k != None and not ('/' in k):
                    temp += k
            key_date = datetime.datetime(m.date.year, m.date.month, m.date.day)
            if temp in l_code:
                if key_date in res.keys():
                    if temp in config.PHENOMENE_PONDERATION.keys():
                        res[key_date] += 0.5
                    else:
                        res[key_date] += 0.5
                else:
                    if temp in config.PHENOMENE_PONDERATION.keys():
                        res[key_date] = 0.5
                    else:
                        res[key_date] = 0.5
        key_date = datetime.datetime(m.date.year, m.date.month, m.date.day)
        if not (key_date in res.keys()):
            res[key_date] = 0

    return res

def trace_phenomene_liste(metars, code,texte_code, conf, show=True) -> None:
    '''
    Entrée : Liste des metars, code du phénomene (TS,-RA...), flag pour l'affichage ou les valeurs
    Sortie : Graphique du phénomène en fonction des mois
    '''
    res = count_weather_date_liste(metars, code)
    code=texte_code
    X = ['Jan', 'Fev', 'Mars', 'Avr', 'Mai', 'Juin',
         'Juil', 'Aout', 'Sept', 'Oct', 'Nov', 'Dec']
    Y = [0 for _ in range(1, 13)]
    cnt = [0 for _ in range(1, 13)]
    deja_jour = []
    for key_date in res.keys():
        mois = key_date.month
        jour = key_date.day
        year = key_date.year
        if not code in config.PHENOMENE_PONDERATION.keys():
            value = res[key_date]
            Y[mois-1] += value
            cnt[mois-1] += 24

        else:
            if not (datetime.datetime(year, mois, jour) in deja_jour):
                deja_jour.append(datetime.datetime(year, mois, jour))
                value = res[key_date]
                Y[mois-1] += value
                cnt[mois-1] += 24
    if not code in config.PHENOMENE_PONDERATION.keys():
        for k in range(len(Y)):
            Y[k] = 30*Y[k]/cnt[k]
    else:
        for k in range(len(Y)):
            Y[k] = 30*(Y[k]*config.PHENOMENE_PONDERATION[code])/cnt[k]
    plt.bar(X, Y, color=color_template().orange)
    addlabels(X, Y, 'j')
    plt.title('Moyenne des jours de '+code+' par mois')
    plt.ylabel('Nombre de jours par mois')
    plt.savefig(
        'Figures_raw/'+conf.chemin_observations[-9:-5]+'/Phenomene'+code+'.svg', format='svg')
    if config.SHOW:
        plt.show()
    plt.close('all')


# trace_phenomene_liste(metars,['TS','TSRA','-TSRA','RETS','VCTS'],'TS',conf)
# trace_phenomene_liste(metars,['-RA','RA'],'RA',conf)
trace_phenomene(metars,'BR',conf)