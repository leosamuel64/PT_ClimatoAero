from metar import Metar
from codes.fonctions_auxiliaires import *
import math
from codes.config import *


def vents_dominants_vitesse(data,decli=0):
    """
    Entrée : Liste des observations, declinaison magnétique
    Sortie : Dictionnaire des listes des vitesses de vent
    """
    res = {i: [0, 0, 0] for i in range(0, 36)}
    somme=0
    for d in data:
        direct = d.direction_vent
        sp = d.vitesse_vent
        if (not ('direction_vent' in d.a_donnees_manquantes())) and (not (direct == '')) and (not ('vitesse_vent' in d.a_donnees_manquantes())) and (not (sp == '')):
            wr = round_wind(direct+decli) % 36
            if sp > 3:
                if sp < 10:
                    res[wr][0] += 1
                    somme+=1
                elif sp < 15:
                    somme+=1
                    res[wr][1] += 1
                else:
                    somme+=1
                    res[wr][2] += 1
        norm = {}
        for key in res.keys():
            a,b,c=res[key]
            norm[key]=[100*a/somme,100*b/somme,100*c/somme]
    return norm


def maxi_temp(data):
    '''
    Entrée : Liste des observations
    Sortie : Couple (Température Maximum, Date)
    '''
    res = data[0].temperature_maxi
    date = data[0].date
    for d in data:
        if not ('temperature_maxi' in d.a_donnees_manquantes()):
            if d.temperature_maxi > res:
                res = d.temperature_maxi
                date = d.date
    return res, date


def mini_temp(data):
    '''
    Entrée : Liste des observations
    Sortie : Couple (Température Minimum, Date)
    '''
    res = data[0].temperature_mini
    for d in data:
        if not ('temperature_mini' in d.a_donnees_manquantes()):
            if d.temperature_mini < res:
                res = d.temperature_mini
                date = d.date
    return res, date


def maxi_qnh(data):
    '''
    Entrée : Liste des observations
    Sortie : Couple (QNH Maximum, Date)
    '''
    res = data[0].qnh
    date = data[0].date
    for d in data:
        if not ('qnh' in d.a_donnees_manquantes()):
            if d.qnh > res:
                res = d.qnh
                date = d.date
    return res, date


def mini_qnh(data):
    '''
    Entrée : Liste des observations
    Sortie : Couple (QNH Minimum, Date)
    '''
    res = data[0].qnh
    for d in data:
        if not ('qnh' in d.a_donnees_manquantes()):
            if d.qnh < res and d.qnh != 0:
                res = d.qnh
                date = d.date
    return res, date


def moyenne_mois(data, intervalle_heure=[]):
    '''
    Entrée : Liste des observations, Intervalle des heures à prendre en compte (pour exclure la nuit)
    Sortie : Dictionnaire des moyennes de température par mois
    '''
    res = {i: 0 for i in range(1, 13)}
    cnt = {i: 0 for i in range(1, 13)}
    for d in data:
        mois = d.date.month
        heure = d.date.hour
        temp = d.temperature

        if intervalle_heure != [] and heure >= intervalle_heure[0] and heure <= intervalle_heure[1]:
            res[mois] += temp
            cnt[mois] += 1
        elif intervalle_heure == []:
            res[mois] += temp
            cnt[mois] += 1
    for mois in res.keys():
        res[mois] = res[mois]/cnt[mois]
    return res


def compte_temps_present(data):
    '''
    Entrée : Liste des observations
    Sortie : Renvoie le dictionnaire code -> occurences des phenomènes
    '''
    res = {}
    for d in data:
        if not ('temps_present' in d.a_donnees_manquantes()):
            incr_dico(res, d.temps_present, 1)
    return res


def pourcentage_temps_present(data, path, affichage=False):
    '''
    Entrée : Liste des observations, chemin vers code météo, Affichage debug
    Sortie : Renvoie le dictionnaire code -> occurences des phenomènes
    '''
    assoc_code = assoc_temps_present(path)
    temps_present = compte_temps_present(data)
    liste = []
    somme = 0
    for k in temps_present.keys():
        if k != '':
            liste.append((temps_present[k], int(k)))
            somme += temps_present[k]
    liste.sort(reverse=True)
    if affichage:
        for (nombre, code) in liste:
            valeur = round(100*nombre/somme)
            if valeur > 0:
                print(str(round(100*nombre/somme, 2))+'% : '+assoc_code[code])
                print('ok')
    else:
        res = []
        for (nombre, code) in liste:
            res.append((assoc_code[code], 100*nombre/somme))


def count_weather(metars):
    '''
    Entrée : Liste des metars
    Sortie : Dictionnaire Code_Phenomene -> Nombre 
    '''
    res = {}
    for m in metars:
        obs = Metar.Metar(m.message)
        weather = obs.weather
        for groupe in weather:
            temp = ''
            for k in groupe:
                if k != None and not ('/' in k):
                    temp += k
            if temp in config.PHENOMENE_PONDERATION.keys():
                valeur = config.PHENOMENE_PONDERATION[temp]
            else:
                valeur = 1
            if temp in res.keys():
                res[temp] += valeur
            else:
                if temp != '':
                    res[temp] = valeur
    return res


def count_weather_date(metars, code):
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
            if temp == code:
                if key_date in res.keys():
                    res[key_date] += 0.5
                else:
                    res[key_date] = 0.5
        key_date = datetime.datetime(m.date.year, m.date.month, m.date.day)
        if not (key_date in res.keys()):
            res[key_date] = 0

    return res


def calcul_crossWind(cap, direction, vitesse):
    """
    Entrée : Cap de l'avion, Direction du vent, vitesse du vent
    Sortie : Vent Traversier subit par l'avion
    """
    angle_au_vent = (cap-direction) % 360
    if angle_au_vent > 180:
        angle_au_vent = abs(angle_au_vent-360)
    rad = angle_au_vent*math.pi/180
    return math.sin(rad)*vitesse


def calcul_vent_eff(cap, direction, vitesse):
    """
    Entrée : Cap de l'avion, Direction du vent, vitesse du vent
    Sortie : Vent Traversier subit par l'avion
    """
    angle_au_vent = (cap-direction) % 360
    if angle_au_vent > 180:
        angle_au_vent = abs(angle_au_vent-360)
    rad = angle_au_vent*math.pi/180

    return math.cos(rad)*vitesse


def limite_vent(d, aeronef, ad):
    """
    Entrée : Observation, avion, numéro de la piste
    Sortie : Indique si le vent est limitant
    """
    if not ('direction_vent' in d.a_donnees_manquantes()) and not ('vitesse_vent' in d.a_donnees_manquantes()) and d.direction_vent != '' and d.vitesse_vent != '':
        direct = d.direction_vent
        sp = d.vitesse_vent
        vent_t = calcul_crossWind(ad.pistes[0]*10, direct, sp)
        if (aeronef.max_cross_wind < vent_t) or ((aeronef.limite_vent != None) and (aeronef.limite_vent < sp)):
            return True
        else:
            return False
    else:
        return False


def limite_precip(d, aeronef):
    """
    Entrée : Observation, avion, numéro de la piste
    Sortie : Indique si le vent est limitant
    """
    if (not ('hauteur_precipitation' in d.a_donnees_manquantes())) and d.hauteur_precipitation != '':
        if d.hauteur_precipitation > 0 and aeronef.limite_pluie:
            return True
        else:
            return False
    else:
        return False


def limite_visi(d, aeronef, ad):
    """
    Entrée : Observation, avion, aerodrome
    Sortie : Indique si la visibilité est limitant
    """
    visi = d.visi
    res = False
    if (not ('visi' in d.a_donnees_manquantes())) and visi != '':
        if visi > 0 and aeronef.ifr and visi < ad.ifr_visi:
            res = True
        elif visi > 0 and not aeronef.ifr and visi < ad.vfr_visi:
            res = True
    return res


def limite_plafond(d, aeronef, ad):
    """
    Entrée : Observation, avion, aerodrome
    Sortie : Indique si le plafond est limitant
    """
    plafond = d.plafond()
    if plafond != None:
        plafond = int(d.plafond()[2])
    res = False
    if plafond != None and aeronef.ifr and plafond < ad.ifr_plafond:
        res = True
    elif plafond != None and not aeronef.ifr and plafond < ad.vfr_plafond:
        res = True
    return res


def limitations(data, aeronef, ad):
    """
    Entrée : Observation, avion, Numéro de la piste, aerodrome
    Sortie : Tableau des pourcentages de non-accessibilité de l'aérodrome par l'aéronef en fonction des mois
    """
    res = {i: ([0,0,0,0], 0) for i in range(0, 12)}
    cnt = 0
    for d in data:
        mois = d.date.month
        last_lim, last_tot = res[mois-1]
        vect_limit = [limite_vent(d, aeronef, ad),limite_visi(d, aeronef, ad),limite_plafond(d, aeronef, ad),limite_precip(d, aeronef)]
        if True in vect_limit:
            res[mois-1] = (ajoute_vecteurs(last_lim,vect_limit), last_tot+1)
        else:
            res[mois-1] = (last_lim, last_tot+1)
    fin = []
    for key in res:
        last_lim, last_tot = res[key]
        temp=[]
        for x in last_lim:
            temp.append(round((x/last_tot)*30, 1))
        fin.append(temp)
    return fin


def calcul_donnees_manquantes(data):
    """
    Entrée : Observation
    Sortie : Liste des pourcentages des parametres manquants
    """
    labels = ["hauteur_precipitation", "duree_precipitation ", "temperature ", "dew_point ", "temperature_mini ", "heure_temperature_mini", "temperature_maxi", "heure_temperature_maxi ", "duree_gel", "qfe", "qnh ", "geopotentiel", "qnh_mini", "vitesse_vent",
              "direction_vent", "vitesse_vent_instant_maxi", "direction_vent_instant_maxi ", "heure_vent_instant_maxi ", "humidite", "humidite_mini", "heure_humidite_mini", "humidite_maxi", "heure_humidite_maxi", "nebulosite ", "temps_present ", "visi"]
    res = {i: 0 for i in labels}
    total = len(data)
    for d in data:
        manquantes = d.a_donnees_manquantes()
        for i in manquantes:
            res[i] += 1
    cnt = len(data)
    for key in res.keys():
        res[key] = 100*res[key]/cnt
    return res


def couple_contingence_visi_plafond(data,ad):
    """
    Entrée : Observation
    Sortie : liste des couples (visi,plafond)
    """
    res = []
    for d in data:
        if (not 'visi' in d.a_donnees_manquantes()) and d.visi != '':
            plafond = d.plafond()
            if plafond != None:
                res.append((d.visi, int(plafond[2])))
            else:
                res.append((d.visi, 20000))
    return res



def couple_contingence_veff_altip(data,ad):
    """
    Entrée : Observation
    Sortie : liste des couples (veff,altipression)
    """
    res = []
    for d in data:
        if (not 'direction_vent' in d.a_donnees_manquantes()) and d.direction_vent != '' and (not 'qnh' in d.a_donnees_manquantes()) and d.qnh != '':
            direction = d.direction_vent
            vitesse = d.vitesse_vent
            alti_p = d.alt + (1013-d.qnh)*28
            
            res.append((calcul_vent_eff(ad.pistes[0],direction,vitesse),alti_p))
    return res


def place_table_contingence(grandeurs, pas1, pas2):
    """
    Entrée : liste des couples, catégories en abscisse, catégories en ordonnée
    Sortie : matrice des valeurs en fonction des catégories
    """
    res = [[0 for _ in range(len(pas1)+1)] for _ in range(len(pas2)+1)]
    for (x, y) in grandeurs:
        i, j = 0, 0
        while (x > pas1[i] and i != len(pas1)-1):
            i += 1
        while (y > pas2[j] and j != len(pas2)-1):
            j += 1
        if x > pas1[len(pas1)-1]:
            i += 1
        if y > pas2[len(pas2)-1]:
            j += 1
        res[j][i] += 1
    return res


def calcul_table_contingence(data, pas_abs, pas_ord, fonction_couple,ad):
    """
    Entrée : Observation, catégories en abscisse, catégories en ordonnée, fonction de création des couples
    Sortie : table de contingence du couple en fonction des catégories (en pourcent)
    """
    couple = fonction_couple(data,ad)
    table_place = place_table_contingence(couple, pas_abs, pas_ord)
    normalise_matrice(table_place)
    return table_place


def compte_gel_mois(data):
    """
    Entrée : Observation,
    Sortie : liste du nombre de jour moyen par mois
    """
    cnt = [0 for i in range(0, 12)]
    total = [0 for i in range(0, 12)]
    for d in data:
        if not ('duree_gel' in d.a_donnees_manquantes()) and d.duree_gel != '':
            mois = d.date.month
            total[mois-1] += 60
            cnt[mois-1] += d.duree_gel
    res = []
    for k in range(len(cnt)):
        res.append((round(4*30*cnt[k]/total[k], 2)))
    return res


def precipitation_par_jour(data):
    """
    Entrée : Observation
    Sortie : Dico des precipitations par jour
    """
    res = {}

    for d in data:
        hp = d.hauteur_precipitation
        if (not ('hauteur_precipitation' in d.a_donnees_manquantes())) and (not (hp == '')):
            jour = d.date.day
            mois = d.date.month
            annee = d.date.year
            date = datetime.datetime(annee, mois, jour)
            incr_dico(res, date, hp)
    return res


def precipitation_par_mois(data):
    """
    Entrée : Observation
    Sortie : liste des precipitations par mois
    """
    precip_jour = precipitation_par_jour(data)
    annee = [[] for _ in range(12)]
    for date in precip_jour.keys():
        mois = date.month
        annee[mois-1].append((round(precip_jour[date], 0), date.year))
    return annee


def max_precipitation_mois(data):
    """
    Entrée : Observation
    Sortie : liste des maxi par mois
    """
    precip_mois = precipitation_par_mois(data)
    res = []
    for k in range(12):
        record = max(precip_mois[k])
        res.append(record)
    return res


def moyenne_precipitation_mois(data):
    """
    Entrée : Observation
    Sortie : liste des moyennes par mois
    """
    precip_mois = precipitation_par_mois(data)
    res = []
    for k in range(12):
        mois = precip_mois[k]
        somme = 0
        for (v, annee) in mois:
            somme += v
        moy = 30*(somme/len(mois))
        res.append(round(moy, 1))
    return res


def vent_t_par_mois(data, piste):
    """
    Entrée : Observation
    Sortie : liste des vents traverisés par mois
    """
    res = {i: [] for i in range(1, 13)}
    for d in data:
        vent_dir = d.direction_vent
        vent_sp = d.vitesse_vent
        if (not ('direction_vent' in d.a_donnees_manquantes())) and (not (vent_dir == '')) and (not ('vitesse_vent' in d.a_donnees_manquantes())) and (not (vent_sp == '')):
            mois = d.date.month
            annee = d.date.year
            vt = calcul_crossWind(piste*10, vent_dir, vent_sp)
            res[mois].append((round(vt, 0), str(annee)+' \n' +
                             str(int(vent_dir))+'°/'+str(int(vent_sp))+'kt'))
    return res


def max_vent_t_mois(data, piste):
    """
    Entrée : Observation
    Sortie : liste des maxis par mois
    """
    vt_mois = vent_t_par_mois(data, piste)
    res = []
    for mois in vt_mois.keys():
        m = max(vt_mois[mois])
        res.append(m)
    return res


def moyenne_vent_t_mois(data, piste):
    """
    Entrée : Observation
    Sortie : liste des moyennes par mois
    """
    vt_mois = vent_t_par_mois(data, piste)
    res = []
    for mois in vt_mois.keys():
        somme = 0
        cnt = 0
        for (v, a) in vt_mois[mois]:
            cnt += 1
            somme += v
        res.append(round(somme/cnt, 2))
    return res


def vent_e_par_mois(data, piste):
    """
    Entrée : Observation
    Sortie : liste des vents traverisés par mois
    """
    res = {i: [] for i in range(1, 13)}
    for d in data:
        vent_dir = d.direction_vent
        vent_sp = d.vitesse_vent
        if (not ('direction_vent' in d.a_donnees_manquantes())) and (not (vent_dir == '')) and (not ('vitesse_vent' in d.a_donnees_manquantes())) and (not (vent_sp == '')):
            mois = d.date.month
            annee = d.date.year
            vt = abs(calcul_vent_eff(piste*10, vent_dir, vent_sp))
            res[mois].append((round(vt, 0), str(annee)+' \n' +
                             str(int(vent_dir))+'°/'+str(int(vent_sp))+'kt'))
    return res


def max_vent_e_mois(data, piste):
    """
    Entrée : Observation
    Sortie : liste des maxis par mois
    """
    vt_mois = vent_e_par_mois(data, piste)
    res = []
    for mois in vt_mois.keys():
        m = max(vt_mois[mois])
        res.append(m)
    return res


def moyenne_vent_e_mois(data, piste):
    """
    Entrée : Observation
    Sortie : liste des moyennes par mois
    """
    vt_mois = vent_e_par_mois(data, piste)
    res = []
    for mois in vt_mois.keys():
        somme = 0
        cnt = 0
        for (v, a) in vt_mois[mois]:
            cnt += 1
            somme += v
        res.append(round(somme/cnt, 2))
    return res


def coeff_pistes(data, ad, seuil_vent):
    pistes = ad.pistes
    piste_pref = ad.piste_pref
    res = {n: 0 for n in pistes}
    cnt = 0
    for d in data:
        vent_dir = d.direction_vent
        vent_sp = d.vitesse_vent
        if (not ('direction_vent' in d.a_donnees_manquantes())) and (not (vent_dir == '')) and (not ('vitesse_vent' in d.a_donnees_manquantes())) and (not (vent_sp == '')):
            v_eff_max = 0
            p = piste_pref
            for hdg in pistes:
                v_eff = calcul_vent_eff(hdg*10, vent_dir, vent_sp)
                if v_eff > v_eff_max:
                    v_eff_max = v_eff
                    p = hdg
            if v_eff_max >= seuil_vent:
                res[p] += 1
            else:
                res[piste_pref] += 1
            cnt += 1
    for hdg in pistes:
        res[hdg] = round(100*res[hdg]/cnt, 1)
    return res


def sort_mois_temp(data, intervalle_heure=[]):
    '''
    Entrée : Liste des observations, Intervalle des heures à prendre en compte (pour exclure la nuit)
    Sortie : Dictionnaire des moyennes de température par mois
    '''
    res = {i: [] for i in range(1, 13)}
    cnt = {i: 0 for i in range(1, 13)}
    for d in data:
        mois = d.date.month
        heure = d.date.hour
        temp = d.temperature
        if (not ('temperature' in d.a_donnees_manquantes())) and (not (temp == '')):
            if intervalle_heure != [] and heure >= intervalle_heure[0] and heure <= intervalle_heure[1]:
                res[mois].append((temp, d.date.year))
            elif intervalle_heure == []:
                res[mois].append((temp, d.date.year))
    return res


def sort_mois_qnh(data, intervalle_heure=[]):
    '''
    Entrée : Liste des observations, Intervalle des heures à prendre en compte (pour exclure la nuit)
    Sortie : Dictionnaire des moyennes des qnh par mois
    '''
    res = {i: [] for i in range(1, 13)}
    cnt = {i: 0 for i in range(1, 13)}
    for d in data:
        mois = d.date.month
        heure = d.date.hour
        temp = d.qnh
        if (not ('qnh' in d.a_donnees_manquantes())) and (not (temp == '')):
            if intervalle_heure != [] and heure >= intervalle_heure[0] and heure <= intervalle_heure[1]:
                res[mois].append((int(temp), d.date.year))
            elif intervalle_heure == []:
                res[mois].append((int(temp), d.date.year))
    return res


def recup_qnh(data):
    '''
    Entrée : Liste des observations
    Sortie : liste des couples (QNH, date)
    '''
    res = []
    for d in data:
        if (not ('qnh' in d.a_donnees_manquantes())) and (not (d.qnh == '')):
            res.append((d.qnh, d.date))
    return res


def recup_temp(data):
    '''
    Entrée : Liste des observations
    Sortie : liste des couples (temperature, date)
    '''
    res = []
    for d in data:
        if (not ('temperature' in d.a_donnees_manquantes())) and (not (d.temperature == '')):
            res.append((d.temperature, d.date))
    return res


def recup_precip(data):
    '''
    Entrée : Liste des observations
    Sortie : liste des couples (precipitation, date)
    '''
    dico = precipitation_par_jour(data)
    res = []
    for key in dico.keys():
        res.append((dico[key], key))
    return res


def liste_occurences(data, fonction, seuil, operation):
    '''
    Entrée : Liste des observations, fonction d'extraction,seuil de comparaison, operation de comparaison
    Sortie : liste des couples (valeur, date) où la valeur est 'operation' au seuil 
    '''
    valeurs = fonction(data)
    res = [(val, datetime.datetime(date.year, date.month, date.day))
           for (val, date) in valeurs if operation(val, seuil)]
    return enleve_doublon(res)


def temps_entre_occurence(occurences, seuil=3):
    '''
    Entrée : liste des occurences [(valeur,date)...]
    Sortie : liste des temps entre deux occurences
    '''
    res = []
    for k in range(len(occurences)-1):
        Δt = occurences[k+1][1] - occurences[k][1]
        if Δt > datetime.timedelta(seuil):
            res.append(Δt.days)
    return res


def duree_retour(data, fonction, seuil, operation):
    '''
    Entrée : Liste des observations, fonction d'extraction, seuil du phenomène, operation de comparaison
    Sortie : durée de retour en mois
    '''
    occurences = liste_occurences(data, fonction, seuil, operation)
    tps_entre = temps_entre_occurence(occurences)
    if tps_entre == []:
        return None
    else:
        return round(moyenne(tps_entre)/31, 1)


def proba_retour(nb_periodes, nb_occurences, d_retour):
    """
    Entrée : nombre de periode, nombre d'occurence, durée de retour
    Sortie : Probabilité d'avoir nb_occurences sur le nb_periode
    """
    return ((nb_periodes/d_retour)**nb_occurences/(facto(nb_occurences)))*math.exp(-nb_periodes/d_retour)


def proba_retour_au_moins(nb_periodes, nb_occurences, d_retour):
    """
    Entrée : nombre de periode, nombre d'occurence, durée de retour
    Sortie : Probabilité d'avoir au moins nb_occurences sur le nb_periode
    """
    somme = 0
    for i in range(0, nb_occurences):
        somme += proba_retour(nb_periodes, i, d_retour)
    return 1 - somme
