from codes.construction_bases import *
from codes.fonctions_auxiliaires import *
from codes.classes import *
from codes.calculs import *
from codes.affichages import *

import os
import time


def genere_export_ad(code_ad, flotte, phenomenes):
    conf = export(code_ad)
    data = charge_fichier(conf.chemin_observations)
    metars = build_dict_metar('data/metar/'+code_ad+'.txt')
    ad = aerodrome(code_ad)
    res = 0
    # Debut calculs images
    rose_des_vents(data, conf)
    res += 1
    plot_weather(metars, conf, seuil=2)
    res += 1
    for phenomene in phenomenes:
        trace_phenomene(metars, phenomene, conf)
        res += 1
    trace_tableau_temp(data, conf)
    res += 1
    trace_tableau_gel(data, conf)
    res += 1
    trace_tableau_qnh(data, conf)
    res += 1
    trace_tableau_precipitation(data, conf)
    res += 1
    trace_tableau_vent_travers(data, ad.pistes[0], conf)
    res += 1
    trace_tableau_vent_effectif(data, ad.pistes[0], conf)
    res += 1
    for ac in flotte:
        acft = avion(ac)
        trace_limitations(data, acft, ad, conf)
        res += 1
    trace_donnees_manquantes(data, conf)
    res += 1
    affiche_tc_visi_plafond(data, conf)
    res += 1
    affiche_coeff_pistes(data, ad, config.SEUIL_VENT_CALME, conf)
    res += 1
    return res


def multi_exports(liste_ad, flotte, phenomenes):

    for code in liste_ad:
        print('---------------------')

        print('---------'+code+'--------')
        deb = time.time()
        res = genere_export_ad(code, flotte, phenomenes)
        tps = round(time.time()-deb, 0)
        print("Temps d'execution : "+str(tps)+' s')
        print("Nombre de figures : "+str(res)+' figures')
        print("Temps par figure : "+str(round(tps/res, 1))+' s/figures')
        
def export_all():
    multi_exports(config.liste_ad, config.flotte, config.phenomenes)