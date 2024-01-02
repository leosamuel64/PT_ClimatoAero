from metar import Metar
from codes.fonctions_auxiliaires import *
import math

def vents_dominants_p(data):
    """
    Entrée : Liste des observations
    Sortie : Dictionnaire des pourcentages des vents
    TODO : Revoir la pondération des vents en fonction de la vitesse
    """
    res={i:0 for i in range(0,36)}
    cnt=0
    for d in data:
        
        direct = d.direction_vent
        sp=d.vitesse_vent
        wr=round_wind(direct)%36
        res[wr]+=1*sp
        cnt+=1*sp
        
    for key in res:
        res[key]=round(100*res[key]/cnt)
    return res


def maxi_temp(data):
    '''
    Entrée : Liste des observations
    Sortie : Couple (Température Maximum, Date)
    '''
    res=data[0].temperature_maxi
    date = data[0].date
    for d in data:
        if d.temperature_maxi>res:
            res = d.temperature_maxi
            date = d.date
    return res,date

def mini_temp(data):
    '''
    Entrée : Liste des observations
    Sortie : Couple (Température Minimum, Date)
    '''
    res=data[0].temperature_mini
    for d in data:
        if d.temperature_mini<res:
            res = d.temperature_mini
            date = d.date
    return res,date

def maxi_qnh(data):
    '''
    Entrée : Liste des observations
    Sortie : Couple (QNH Maximum, Date)
    '''
    res=data[0].qnh
    date = data[0].date
    for d in data:
        if d.qnh>res:
            res = d.qnh
            date = d.date
    return res,date

def mini_qnh(data):
    '''
    Entrée : Liste des observations
    Sortie : Couple (QNH Minimum, Date)
    '''
    res=data[0].qnh
    for d in data:
        if d.qnh<res and d.qnh!=0:
            res = d.qnh
            date = d.date
    return res,date

def moyenne_mois(data,intervalle_heure=[]):
    '''
    Entrée : Liste des observations, Intervalle des heures à prendre en compte (pour exclure la nuit)
    Sortie : Dictionnaire des moyennes de température par mois
    '''
    res = {i:0 for i in range(1,13)}
    cnt = {i:0 for i in range(1,13)}
    for d in data:
        mois = d.date.month
        heure = d.date.hour
        temp = d.temperature
        
        if intervalle_heure != [] and heure>=intervalle_heure[0] and heure<=intervalle_heure[1]:
            res[mois]+=temp
            cnt[mois]+=1
        elif intervalle_heure == []:
            res[mois]+=temp
            cnt[mois]+=1
    for mois in res.keys():
        res[mois]=res[mois]/cnt[mois]
    return res

def compte_temps_present(data):
    '''
    Entrée : Liste des observations
    Sortie : Renvoie le dictionnaire code -> occurences des phenomènes
    '''
    res={}
    for d in data:
        incr_dico(res,d.temps_present,1)
    return res


def pourcentage_temps_present(data,path,affichage=False):
    '''
    Entrée : Liste des observations, chemin vers code météo, Affichage debug
    Sortie : Renvoie le dictionnaire code -> occurences des phenomènes
    '''
    assoc_code = assoc_temps_present(path)
    temps_present = compte_temps_present(data)
    liste = []
    somme=0
    for k in temps_present.keys():
        if k!='':
            liste.append((temps_present[k],int(k)))
            somme+=temps_present[k]
    liste.sort(reverse=True)
    if affichage:
        for (nombre,code) in liste:
            valeur = round(100*nombre/somme)
            if valeur >0:
                print(str(round(100*nombre/somme,2))+'% : '+assoc_code[code])
                print('ok')
    else:
        res=[]
        for (nombre,code) in liste:
            res.append((assoc_code[code],100*nombre/somme))

def count_weather(metars):
    '''
    Entrée : Liste des metars
    Sortie : Dictionnaire Code_Phenomene -> Nombre 
    '''
    res={}
    for m in metars:
        obs = Metar.Metar(m.message)
        weather = obs.weather
        for groupe in weather:
            temp=''
            for k in groupe:
                if k!=None and not('/' in k):
                    temp+=k
            if temp in res.keys():
                res[temp]+=1
            else:
                if temp!='':
                    res[temp]=1
    return res

def count_weather_date(metars,code):
    '''
    Entrée : Liste des metars, code du phénomène
    Sortie : Dictionnaire Date -> Nombre d'heure du phenomene pour ce jour 
    '''
    res={}
    date=metars[0].date
    for m in metars:
        obs = Metar.Metar(m.message)
        weather = obs.weather
        for groupe in weather:
            temp=''
            for k in groupe:
                if k!=None and not('/' in k):
                    temp+=k
                    
            key_date=datetime.datetime(m.date.year,m.date.month,m.date.day)

            if temp==code:
                if key_date in res.keys():
                    res[key_date]+=0.5
                else:
                    res[key_date]=0.5
            elif not key_date in res.keys():
                    res[key_date]=0
                        
    return res

def calcul_crossWind(cap,direction,vitesse):
    """
    Entrée : Cap de l'avion, Direction du vent, vitesse du vent
    Sortie : Vent Traversier subit par l'avion
    """
    angle_au_vent=(cap-direction) % 360
    
    if angle_au_vent>180:
        angle_au_vent=abs(angle_au_vent-360)
    rad = angle_au_vent*math.pi/180
    
    return math.sin(rad)*vitesse

def limite_vent(d,aeronef,piste):
    """
    Entrée : Observation, avion, numéro de la piste
    Sortie : Indique si le vent est limitant
    """
    direct = d.direction_vent
    sp=d.vitesse_vent
    vent_t = calcul_crossWind(piste*10,direct,sp)
    if aeronef.max_cross_wind < vent_t:
        return True
    else:
        return False
    
def limite_visi(d,aeronef,ad):
    """
    Entrée : Observation, avion, aerodrome
    Sortie : Indique si la visibilité est limitant
    """
    visi = d.visi
    res = False
    if visi > 0 and aeronef.ifr and visi<ad.ifr_visi :
        res=True
    elif visi > 0 and not aeronef.ifr and visi < ad.vfr_visi:
        res=True
    return res
        
def limite_plafond(d,aeronef,ad):
    """
    Entrée : Observation, avion, aerodrome
    Sortie : Indique si le plafond est limitant
    """
    plafond = d.plafond()
    if plafond!=None:
        plafond = int(d.plafond()[2])
    res = False
    if plafond!=None and aeronef.ifr and plafond<ad.ifr_plafond :
        res=True
    elif plafond!=None and not aeronef.ifr and plafond < ad.vfr_plafond:
        res=True
    return res

def limitations(data,aeronef,piste,ad):
    """
    Entrée : Observation, avion, Numéro de la piste, aerodrome
    Sortie : Tableau des pourcentages de non-accessibilité de l'aérodrome par l'aéronef en fonction des mois
    """
    res={i:(0,0) for i in range(0,12)}
    cnt=0
    for d in data:
        mois=d.date.month
        
        last_lim, last_tot = res[mois-1]
        
        if limite_vent(d,aeronef,piste) or limite_visi(d,aeronef,ad) or limite_plafond(d,aeronef,ad):        
            res[mois-1]=(last_lim+1,last_tot+1)
        else:
            res[mois-1]=(last_lim,last_tot+1)
    fin=[]
    for key in res:
        last_lim, last_tot = res[key]
        fin.append(round(100*last_lim/last_tot,1))
    return fin