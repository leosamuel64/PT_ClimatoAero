from codes.construction_bases import *
from codes.fonctions_auxiliaires import *
from codes.classes import *
from codes.calculs import *
from codes.affichages import *
from codes.debug import *

from codes.config import *
from codes.export import *


code_ad = 'LFBR'

conf = export(code_ad)

data = charge_fichier(conf.chemin_observations)
# metars = build_dict_metar('data/metar/'+code_ad+'.txt')
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
# trace_phenomene(metars,'BR',conf)

# mois = [i for i in range(1,13)]

# arr_IFR = [27037,
# 24114,
# 25213,
# 23990,
# 25318,
# 26852,
# 25590,
# 23480,
# 28788,
# 28827,
# 25037,
# 24842
# ]

# delay = [9459,
# 1352,
# 3785,
# 2770,
# 2503,
# 2757,
# 3005,
# 251,
# 10723,
# 11554,
# 5633,
# 12131,
# ]

# wx_delay = [7504,
# 978,
# 173,
# 542,
# 76,
# 517,
# 0,
# 0,
# 448,
# 8245,
# 4415,
# 11670,
# ]

# somme_arr = 0
# somme_delay=0
# somme_wx = 0

# for i in range(12):
#     print('{i} : IFR_ARR={arr} \t|\t DELAY={delay}% \t dont \t WX_DELAY={mto}% \tsoit au total\t WX_DELAY={mto_tot}%'.format(
#         i=i+1,
#         arr=int(arr_IFR[i]),
#         delay=int(100*delay[i]/arr_IFR[i]),
#         mto=int(100*wx_delay[i]/delay[i]),
#         mto_tot=int(100*wx_delay[i]/arr_IFR[i])))
#     somme_arr+=arr_IFR[i]
#     somme_delay+= delay[i]
#     somme_wx+= wx_delay[i]
    
# print('IFR_ARR={arr} \t|\t DELAY={delay}% \t dont \t WX_DELAY={mto}% \tsoit au total\t WX_DELAY={mto_tot}%'.format(
#         arr=int(somme_arr),
#         delay=int(100*somme_delay/somme_arr),
#         mto=int(100*somme_wx/somme_delay),
#         mto_tot=int(100*somme_wx/somme_arr)))

    
class annulation_DFPV:
    def __init__(self,ligne) -> None:
        Evt_Key,Evt_Label,Evt_Type,Evt_Category,Evt_CreatedAt,Evt_UpdatedAt,Dat_DayFree,Dat_DayOfWeek,Dat_Day,Dat_Month,Dat_Year,Dat_Week,Dat_StartDate,Dat_StartHour,Dat_EndDate,Dat_EndHour,Dat_Hours,Dat_DayHours,Res_RegistrationNumber,Cus_Label,Cus_Company =ligne.strip().split(';')
        self.avion = Evt_Label
        self.category = Evt_Category
        jour,mois, annee = Dat_StartDate.strip().split('/')
        heure,minute = Dat_StartHour.strip().split(':')
        self.date = datetime.datetime(int(annee),int(mois),int(jour),int(heure),int(minute))
        if Cus_Label!='':
            centre = Cus_Label[0:3]
        else:
            centre = 'XXX'
        assoc = {'MUR' : 'LFBR',
                 'CAR' : 'LFMK',
                 'GRE' : 'LFLS',
                 'YAN' : 'LFLN',
                 'BIS' : 'LFBS',
                 'MPL' : 'LFMT',
                 'MEL' : 'LFPM',
                 'XXX' : 'LFxx'}
        try:
            self.centre = assoc[centre]
        except:
            self.centre = Cus_Label
        
def charge_base_DFPV(chemin):
    res=[]
    file = open(chemin)
    for ligne in file:
        annulation = annulation_DFPV(ligne)
        res.append(annulation)
    return res

# print(len(charge_base_DFPV('data/DFPV.csv')))

def calcul_annulation_terrain(base,code_terrain,avions):
    X = ['Jan', 'Fev', 'Mars', 'Avr', 'Mai', 'Juin',
         'Juil', 'Aout', 'Sept', 'Oct', 'Nov', 'Dec']
    Y = {i:0 for i in range(1,13)}
    cnt = 0
    for ann in base:
        # print(ann.category)
        if (ann.centre == code_terrain) and (ann.avion in avions) and (ann.category == 'Annulation cause m�t�o'):
            mois = ann.date.month
            incr_dico(Y,mois,1)
        cnt+=1
    res=[]
    for i in range(1,13):
        res.append(1000*Y[i]/cnt)
    return X, res


dfpv = charge_base_DFPV('data/DFPV.csv')
# calcul_annulation_terrain(dfpv,'LFBR')

def affiche_annulation_terrain(base,code_terrain,avions):
    X,Y = calcul_annulation_terrain(base,code_terrain,avions)
    
    plt.bar(X, Y, color=color_template().orange)
    addlabels(X, Y, '‰')
    plt.title("Nombre d'annulations météo parmis les annulations à {}".format(code_terrain))
    plt.ylabel('Nombre de vols concernés pour 1000 vols')
    plt.savefig(
        'Figures_raw/'+conf.chemin_observations[-9:-5]+'/Annulation'+code_terrain+'.svg', format='svg')
    if config.SHOW:
        plt.show()
    plt.close('all')
    
# affiche_annulation_terrain(dfpv,'LFBR',['A-TB10','A-DA40','A-CAP10','A-Vélis'])

# affiche_annulation_terrain(dfpv,'LFBR',['A-TB20','A-DA42','A-BE58_TXi'])

def vents_dominants_vitesse_metar(metar, decli=0):
    """
    Entrée : Liste des observations, declinaison magnétique
    Sortie : Dictionnaire des listes des vitesses de vent
    """
    res = {i: [0, 0, 0] for i in range(0, 36)}
    somme = 0
    for m in metar:
        obs = Metar.Metar(m.message)
        if obs.wind_dir!=None and obs.wind_speed!=None:
            direct = obs.wind_dir.value()
            sp = obs.wind_speed.value()
            wr = round_wind(direct-decli) % 36
            if sp > 2.92:
                if sp < 8.75:
                    res[wr][0] += 1
                    somme += 1
                elif sp < 15.55:
                    somme += 1
                    res[wr][1] += 1
                else:
                    somme += 1
                    res[wr][2] += 1
        norm = {}
        for key in res.keys():
            a, b, c = res[key]
            if somme != 0:
                norm[key] = [100*a/somme, 100*b/somme, 100*c/somme]
            else:
                norm[key] = [0, 0, 0]
    return norm

        
def rose_des_vents_metar(metars, conf) -> None:
    '''
    Entrée : Liste des observations, liste des numéros de pistes\r
    Sortie : Graphique Rose des vents
    '''
    vd = vents_dominants_vitesse_metar(metars)
    ax = plt.subplot(111, polar=True)
    ax.set_theta_zero_location("N")
    ax.set_theta_direction(-1)
    ax.get_yaxis().set_visible(True)
    legnd_R = True
    legnd_O = True
    legnd_G = True
    for d in vd:
        i, m, s = vd[d]
        s += i+m
        m += i
        if legnd_R:
            plt.bar(x=(d*10)*math.pi/180, height=s, width=math.pi*10 /
                    180, bottom=0, color="red", label='>8m/s')
            legnd_R = False
        else:
            plt.bar(x=(d*10)*math.pi/180, height=s,
                    width=math.pi*10/180, bottom=0, color="red")
        if legnd_O:
            plt.bar(x=(d*10)*math.pi/180, height=m, width=math.pi*10/180,
                    bottom=0, color="orange", label='[4.5;8] m/s')
            legnd_O = False
        else:
            plt.bar(x=(d*10)*math.pi/180, height=m,
                    width=math.pi*10/180, bottom=0, color="orange")
        if legnd_G:
            plt.bar(x=(d*10)*math.pi/180, height=i, width=math.pi*10 /
                    180, bottom=0, color="green", label='[1.5;4.5] m/s')
            legnd_G = False
        else:
            plt.bar(x=(d*10)*math.pi/180, height=i,
                    width=math.pi*10/180, bottom=0, color="green")
    ax.set_title("Rose des vents")
    ax.set_rlabel_position(45)
    plt.xticks([x*math.pi/180 for x in range(10, 370, 10)])

    plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
    plt.savefig('Figures_raw/' +
                conf.chemin_observations[-9:-5]+'/RDV_metar.svg', format='svg')
    if config.SHOW:
        plt.show()
    plt.close('all')


# rose_des_vents_metar(metars,conf)

debug_visi(data,conf)