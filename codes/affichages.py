from PIL import Image
import matplotlib.pyplot as plt
import math
import datetime
from codes.calculs import *
from codes.config import *


def rose_des_vents(data, conf) -> None:
    '''
    Entrée : Liste des observations, liste des numéros de pistes
    Sortie : Graphique Rose des vents
    '''
    vd = vents_dominants_vitesse(data)
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
                    180, bottom=0, color="red", label='>15kt')
            legnd_R = False
        else:
            plt.bar(x=(d*10)*math.pi/180, height=s,
                    width=math.pi*10/180, bottom=0, color="red")
        if legnd_O:
            plt.bar(x=(d*10)*math.pi/180, height=m, width=math.pi*10/180,
                    bottom=0, color="orange", label='[10;15] kt')
            legnd_O = False
        else:
            plt.bar(x=(d*10)*math.pi/180, height=m,
                    width=math.pi*10/180, bottom=0, color="orange")
        if legnd_G:
            plt.bar(x=(d*10)*math.pi/180, height=i, width=math.pi*10 /
                    180, bottom=0, color="green", label='[3;10]kt')
            legnd_G = False
        else:
            plt.bar(x=(d*10)*math.pi/180, height=i,
                    width=math.pi*10/180, bottom=0, color="green")
    ax.set_title("Rose des vents")
    ax.set_rlabel_position(45)
    plt.xticks([x*math.pi/180 for x in range(10, 370, 10)])
    # ax.xaxis.set_major_locator(plt.MultipleLocator(10*math.pi/180))

    plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
    plt.savefig('Figures_raw/' +
                conf.chemin_observations[-9:-5]+'/RDV_.svg', format='svg')
    if config.SHOW:
        plt.show()
    plt.close('all')


def plot_temp(data):
    '''
    Entrée : Liste des observations
    Sortie : Graphique des températures en fonction de la date
    '''
    X = []
    Y = []
    maxi_calc, maxi_date = maxi_temp(data)
    mini_calc, mini_date = mini_temp(data)
    cnt = data[0].date
    for d in data:
        if not ('temperature' in d.a_donnees_manquantes()):
            X.append(d.temperature)
            Y.append(cnt)
            cnt += datetime.timedelta(0, 30*60)
    plt.plot_date(Y, X)
    plt.xlabel('Date')
    plt.ylabel('Température (°C)')
    plt.title('Température '+data[0].nom+'\n Température Maximum : '+str(maxi_calc)+'°C ('+str(
        maxi_date)+')\n Température Minimum : '+str(mini_calc)+'°C ('+str(mini_date)+')')
    if config.SHOW:
        plt.show()
    plt.close('all')


def plot_qnh(data):
    '''
    Entrée : Liste des observations
    Sortie : Graphique des températures en fonction de la date
    '''
    X = []
    Y = []
    maxi_calc, maxi_date = maxi_qnh(data)
    mini_calc, mini_date = mini_qnh(data)
    cnt = data[0].date
    for d in data:
        if not ('qnh' in d.a_donnees_manquantes()):
            X.append(d.qnh)
            Y.append(cnt)
        cnt += datetime.timedelta(0, 30*60)
    plt.plot(Y, X)
    plt.xlabel('Date')
    plt.ylabel('Température (°C)')
    plt.title('QNH '+data[0].nom+'\n QNH Maximum : '+str(maxi_calc)+'hPa ('+str(
        maxi_date)+')\n QNH Minimum : '+str(mini_calc)+'hPa ('+str(mini_date)+')')
    if config.SHOW:
        plt.show()
    plt.close('all')


def plot_weather(metars, conf, seuil=0):
    '''
    Entrée : Liste des metars, seuil pour ignorer les temps rares
    Sortie : Histogramme des pourcentages de chaque temps présent
    '''
    weather = count_weather(metars)
    X = []
    Y = []
    temp = []
    for key in weather.keys():
        temp.append([weather[key], key])
    temp.sort(reverse=True)
    long = len(metars)
    for (x, y) in temp:
        pourcentage = 2*365*x/long
        if pourcentage > seuil:
            X.append(pourcentage)
            Y.append(y)
    plt.bar(Y, X, color=color_template().orange)
    addlabels(Y, X, 'j/an')
    plt.title('Temps significatifs')
    plt.savefig('Figures_raw/' +
                conf.chemin_observations[-9:-5]+'/weather.svg', format='svg')
    if config.SHOW:
        plt.show()
    plt.close('all')


def trace_phenomene(metars, code, conf, show=True):
    '''
    Entrée : Liste des metars, code du phénomene (TS,-RA...), flag pour l'affichage ou les valeurs
    Sortie : Graphique du phénomène en fonction des mois
    '''
    res = count_weather_date(metars, code)
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
    plt.savefig(
        'Figures_raw/'+conf.chemin_observations[-9:-5]+'/Phenomene'+code+'.svg', format='svg')
    if config.SHOW:
        plt.show()
    plt.close('all')


def trace_tableau(column_labels, line_label, data_temp, nom, conf, ajout=''):
    '''
    Entrée : Liste des labels, liste de liste des données
    Sortie : Tableau
    '''
    data_temp_2 = []
    for t in data_temp:
        tableau = format_temp_date(t, ajout)
        data_temp_2.append(tableau)
    data = []
    for k in range(len(data_temp_2)):
        data.append(ajoute_debut(data_temp_2[k], line_label[k]))
    data_head = ajoute_debut(data, column_labels)
    colors = [[color_template().fond_table for _ in range(len(data_head[0]))]
              for _ in range(len(data_head))]
    for k in range(len(colors[0])):
        colors[0][k] = color_template().orange
    fig, ax = plt.subplots(1, 1)
    # ax.axis("tight")
    ax.axis("off")
    table = ax.table(cellText=data_head, cellColours=colors, loc="center")
    table.auto_set_font_size(True)
    # table.set_fontsize(5)
    plt.title(nom)
    plt.savefig(
        'Figures_raw/'+conf.chemin_observations[-9:-5]+'/Tableau'+nom+'.svg', format='svg')
    if config.SHOW:
        plt.show()
    plt.close('all')


def trace_tableau_temp(data, conf):
    """
    Entrée : Observation
    Sortie : Tableau des temperature max, min et moyenne avec les records par mois
    """
    valeurs = sort_mois_temp(data)
    t_max = tableau_climato_temp(valeurs, max)
    t_min = tableau_climato_temp(valeurs, min)
    t_moy = tableau_moyenne_temp(valeurs)
    trace_tableau(['-', 'Jan', 'Fev', 'Mars', 'Avr', 'Mai', 'Juin', 'Juil', 'Aout', 'Sept', 'Oct', 'Nov', 'Dec'],
                  ['Max', 'Min', 'Moy'],
                  [t_max, t_min, t_moy], 'température', conf, '°C')


def trace_tableau_qnh(data, conf):
    """
    Entrée : Observation
    Sortie : Tableau des temperature max, min et moyenne avec les records par mois
    """
    valeurs = sort_mois_qnh(data)
    t_max = tableau_climato_qnh(valeurs, max)
    t_min = tableau_climato_qnh(valeurs, min)
    t_moy = tableau_moyenne_qnh(valeurs)
    maxi = max(t_max)[0]
    mini = min(t_min)[0]
    moy = round(moyenne(t_moy), 0)
    trace_tableau(['-', 'Jan', 'Fev', 'Mars', 'Avr', 'Mai', 'Juin', 'Juil', 'Aout', 'Sept', 'Oct', 'Nov', 'Dec', 'Record'],
                  ['Max', 'Min', 'Moy'],
                  [t_max+[maxi], t_min+[mini], t_moy+[str(moy)]], 'QNH', conf, 'hPa')


def trace_limitations(data, aeronef, ad, conf):
    """
    Entrée : Observation, avion, Numéro de la piste, aerodrome
    Sortie : Graphique des pourcentages de non-accessibilité de l'aérodrome par l'aéronef en fonction des mois
    """
    res = limitations(data, aeronef, ad)
    X = ['Jan', 'Fev', 'Mars', 'Avr', 'Mai', 'Juin',
         'Juil', 'Aout', 'Sept', 'Oct', 'Nov', 'Dec']
    l_vent = []
    l_visi = []
    l_plaf = []
    l_precip = []
    legend_vent = False
    legend_visi = False
    legend_plaf = False
    legend_precip = False
    for (vent, visi, plaf, precip) in res:
        visi += vent
        plaf += visi
        precip += plaf
        l_vent.append(vent)
        l_visi.append(visi)
        l_plaf.append(plaf)
        l_precip.append(precip)

    if not legend_precip:
        plt.bar(X, l_precip, color='lightsteelblue',
                label='Limitations precipitations')
        legend_precip = True
    else:
        plt.bar(X, l_precip, color='lightsteelblue')

    if not legend_plaf:
        plt.bar(X, l_plaf, color='palegreen', label='Limitations plafond')
        legend_plaf = True
    else:
        plt.bar(X, l_plaf, color='palegreen')

    if not legend_visi:
        plt.bar(X, l_visi, color='darkgray', label='Limitations visibilité')
        legend_visi = True
    else:
        plt.bar(X, l_visi, color='darkgray')

    if not legend_vent:
        plt.bar(X, l_vent, color='peachpuff',
                label='Limitations vent traversier')
        legend_vent = True
    else:
        plt.bar(X, l_vent, color='peachpuff')

    addlabels(X, l_precip, 'j')

    plt.legend()
    plt.title('limitation '+aeronef.nom)
    plt.savefig(
        'Figures_raw/'+conf.chemin_observations[-9:-5]+'/limit_'+aeronef.code+'.svg', format='svg')
    if config.SHOW:
        plt.show()
    plt.close('all')


def trace_donnees_manquantes(data, conf):
    """
    Entrée : Observation
    Sortie : tableau des pourcentages des données manquantes par paramètres
    """
    calc = calcul_donnees_manquantes(data)
    res = []
    keys = []
    for key in calc.keys():
        res.append([round(calc[key], 2)])
        keys.append(key)
    trace_tableau(['Données', 'Données Manquantes (%)'],
                  keys,
                  res, 'Données Manquantes', conf)


def affiche_table_contingence(data, pas_abs, pas_ord, fonction_couple, texte, conf, ad):
    """
    Entrée : Observation, catégories en abscisse, catégories en ordonnée, fonction de création des couples, texte pour la case (0,0)
    Sortie : table de contingence du couple en fonction des catégories en image
    """
    table = calcul_table_contingence(
        data, pas_abs, pas_ord, fonction_couple, ad)
    trace_tableau([texte]+pas_abs+['>'],
                  pas_ord+['>'],
                  table, 'tc '+texte, conf, '')


def affiche_tc_visi_plafond(data, conf, ad):
    """
    Entrée : Observation,
    Sortie : table de contingence visi/plafond
    """
    pas_visi = [800, 1500, 5000, 10000]  # Visi
    pas_plafond = [200, 400, 1500, 5000]  # Plafond
    # TODO : Définir les seuils
    affiche_table_contingence(data, pas_visi, pas_plafond,
                              couple_contingence_visi_plafond, 'Visibilité\n Plafond          ', conf, ad)


def affiche_tc_venteff_altip(data, conf, ad, T, marge):
    """
    Entrée : Observation,
    Sortie : table de contingence visi/plafond
    """
    data2 = []
    for d in data:
        temp = d.temperature
        if (not ('temperature' in d.a_donnees_manquantes())) and (not (temp == '')):
            if (d.temperature <= T+marge) and (d.temperature >= T-marge):
                data2.append(d)

    pas_visi = [3, 10, 20]  # vent eff
    pas_plafond = [450, 620, 750]  # alti pression
    # TODO : Définir les seuils
    affiche_table_contingence(data2, pas_visi, pas_plafond,
                              couple_contingence_veff_altip, 'Vent effectif\n altitude pression         '+str(T)+'°C', conf, ad)


def trace_tableau_gel(data, conf):
    """
    Entrée : Observation,
    Sortie : tableau du nombre de jours moyen de gel par mois
    """
    tab = compte_gel_mois(data)
    trace_tableau(['-', 'Jan', 'Fev', 'Mars', 'Avr', 'Mai', 'Juin', 'Juil', 'Aout', 'Sept', 'Oct', 'Nov', 'Dec'],
                  ['jours/mois'],
                  [tab], 'gel', conf, 'j/m')


def trace_tableau_precipitation(data, conf):
    """
    Entrée : Observation
    Sortie : Tableau des precipitations max et moyenne avec les records par mois
    """
    t_max = max_precipitation_mois(data)
    t_moy = moyenne_precipitation_mois(data)
    maxi = max(t_max)[0]
    moy = round(moyenne(t_moy), 0)
    trace_tableau(['-', 'Jan', 'Fev', 'Mars', 'Avr', 'Mai', 'Juin', 'Juil', 'Aout', 'Sept', 'Oct', 'Nov', 'Dec', 'Record'],
                  ['Max (mm/jour)', 'Moy (mm)'],
                  [t_max+[str(maxi)], t_moy+[str(moy)]],
                  'precipitation', conf, '')


def trace_tableau_vent_travers(data, piste, conf):
    """
    Entrée : Observation
    Sortie : Tableau des vents traversiés max et moyen avec les records par mois
    """
    t_max = max_vent_t_mois(data, piste)
    t_moy = moyenne_vent_t_mois(data, piste)
    maxi = max(t_max)[0]
    moy = round(moyenne(t_moy), 0)
    trace_tableau(['-', 'Jan', 'Fev', 'Mars', 'Avr', 'Mai', 'Juin', 'Juil', 'Aout', 'Sept', 'Oct', 'Nov', 'Dec', 'Record'],
                  ['Max'],
                  [t_max+[str(maxi)]],
                  'Vent_travers', conf, 'kt')


def trace_tableau_vent_effectif(data, piste, conf):
    """
    Entrée : Observation
    Sortie : Tableau des vents traversiés max et moyen avec les records par mois
    """
    t_max = max_vent_e_mois(data, piste)
    t_moy = moyenne_vent_e_mois(data, piste)
    maxi = max(t_max)[0]
    moy = round(moyenne(t_moy), 0)
    trace_tableau(['-', 'Jan', 'Fev', 'Mars', 'Avr', 'Mai', 'Juin', 'Juil', 'Aout', 'Sept', 'Oct', 'Nov', 'Dec', 'Record'],
                  ['Max', 'Moy'],
                  [t_max+[str(maxi)], t_moy+[str(moy)]],
                  'Vent_effectif', conf, 'kt')


def affiche_coeff_pistes(data, ad, seuil_vent, conf):
    """
    Entrée : Observation, aerodrome, seuil de vent calme
    Sortie : Diagramme en barre de l'utilisation des pistes
    """
    coeff_p = coeff_pistes(data, ad, seuil_vent)
    X, Y = [], []
    for piste in coeff_p.keys():
        X.append(str(piste))
        Y.append(coeff_p[piste])
    plt.bar(X, Y, color=color_template().orange)
    addlabels(X, Y, '%')
    plt.savefig(
        'Figures_raw/'+conf.chemin_observations[-9:-5]+'/coeff_pistes.svg', format='svg')
    if config.SHOW:
        plt.show()
    plt.close('all')


def trace_duree_retour_qnh(data, conf, borne_inf=875, borne_sup=1045):
    """
    Entrée : Observation
    Sortie : Graphe de la durée de retour des valeurs de qnh
    """
    X = []
    Y = []
    for qnh in range(borne_inf, borne_sup+1):
        if qnh <= 1013:
            dr = duree_retour(data, recup_qnh, qnh, inferieur_a)
        else:
            dr = duree_retour(data, recup_qnh, qnh, superieur_a)
        if dr != None:
            X.append(dr)
            Y.append(qnh)
    plt.scatter(Y, X)
    plt.xlabel('QNH (hPa)')
    plt.ylabel('Nombre de mois')
    plt.title('Durée de retour QNH')
    plt.savefig(
        'Figures_raw/'+conf.chemin_observations[-9:-5]+'/duree_retour_qnh.svg', format='svg')
    if config.SHOW:
        plt.show()
    plt.close('all')


def trace_duree_retour_temp(data, conf, borne_inf=-20, borne_sup=45):
    """
    Entrée : Observation
    Sortie : Graphe de la durée de retour des valeurs de température
    """
    X = []
    Y = []
    for qnh in range(borne_inf, borne_sup+1):
        if qnh > 15:
            dr = duree_retour(data, recup_temp, qnh, superieur_a)
        else:
            dr = duree_retour(data, recup_temp, qnh, inferieur_a)
        if dr != None:
            X.append(dr)
            Y.append(qnh)
    plt.scatter(Y, X)
    plt.xlabel('Température (°C)')
    plt.ylabel('Nombre de mois')
    plt.title('Durée de retour Température')
    plt.savefig(
        'Figures_raw/'+conf.chemin_observations[-9:-5]+'/duree_retour_temp.svg', format='svg')
    if config.SHOW:
        plt.show()
    plt.close('all')


def trace_duree_retour_precip(data, conf, borne_inf=0, borne_sup=60):
    """
    Entrée : Observation
    Sortie : Graphe de la durée de retour des valeurs de precipitation
    """
    X = []
    Y = []
    for qnh in range(borne_inf, borne_sup+1):
        dr = duree_retour(data, recup_precip, qnh, superieur_a)
        if dr != None:
            X.append(dr)
            Y.append(qnh)
    plt.scatter(Y, X)
    plt.xlabel('Precipitation (mm/jour)')
    plt.ylabel('Nombre de mois')
    plt.title('Durée de retour Precipitation')
    plt.savefig(
        'Figures_raw/'+conf.chemin_observations[-9:-5]+'/duree_retour_precip.svg', format='svg')
    if config.SHOW:
        plt.show()
    plt.close('all')


def trace_proba_retour_qnh(data, conf, qnh, nb_periode=10*12, seuil=10**(-3)):
    """
    Entrée : Observation, valeur cible, nb de periode
    Sortie : Graphe de la probabilité d'avoir une valeur de QNH des occurence sur la periode 
    """
    X = []
    Y = []
    if qnh <= 1013:
        dr = duree_retour(data, recup_qnh, qnh, inferieur_a)
    else:
        dr = duree_retour(data, recup_qnh, qnh, superieur_a)
    occ = 0
    p = 1
    while p > seuil:
        p = proba_retour_au_moins(nb_periode, occ, dr)
        X.append(occ)
        Y.append(p)
        occ += 1
    plt.scatter(X, Y, label='Probabilité')
    plt.plot([0, occ], [0.95, 0.95], color='red', label='Seuil à 95%')
    plt.legend()
    plt.xlabel("Nombre d'occurences")
    plt.ylabel('Probabilité')
    if qnh <= 1013:
        plt.title("Probabilité du nombre d'occurences de \n QNH<"+str(qnh) +
                  'hPa sur une periode de ' + str(int(nb_periode/12))+' ans')
    else:
        plt.title("Probabilité du nombre d'occurences de \n QNH>"+str(qnh) +
                  'hPa sur une periode de ' + str(int(nb_periode/12))+' ans')
    plt.savefig(
        'Figures_raw/'+conf.chemin_observations[-9:-5]+'/proba_retour_qnh.svg', format='svg')
    if config.SHOW:
        plt.show()
    plt.close('all')


def trace_proba_retour_temp(data, conf, qnh, nb_periode=10*12, seuil=10**(-3)):
    """
    Entrée : Observation, valeur cible, nb de periode
    Sortie : Graphe de la probabilité d'avoir une valeur de température des occurence sur la periode 
    """
    X = []
    Y = []
    if qnh > 15:
        dr = duree_retour(data, recup_temp, qnh, superieur_a)
    else:
        dr = duree_retour(data, recup_temp, qnh, inferieur_a)
    occ = 0
    p = 1
    while p > seuil:
        p = proba_retour_au_moins(nb_periode, occ, dr)
        X.append(occ)
        Y.append(p)
        occ += 1
    plt.scatter(X, Y, label='Probabilité')
    plt.plot([0, occ], [0.95, 0.95], color='red', label='Seuil à 95%')
    plt.legend()
    plt.xlabel("Nombre d'occurences")
    plt.ylabel('Probabilité')
    if qnh > 15:
        plt.title("Probabilité du nombre d'occurence de \n T<"+str(qnh) +
                  '°C sur une periode de ' + str(int(nb_periode/12))+' ans')
    else:
        plt.title("Probabilité du nombre d'occurence de \n T>"+str(qnh) +
                  '°C sur une periode de ' + str(int(nb_periode/12))+' ans')
    plt.savefig(
        'Figures_raw/'+conf.chemin_observations[-9:-5]+'/proba_retour_temp.svg', format='svg')
    if config.SHOW:
        plt.show()
    plt.close('all')


def trace_proba_retour_precip(data, conf, qnh, nb_periode=10*12, seuil=10**(-3)):
    """
    Entrée : Observation, valeur cible, nb de periode
    Sortie : Graphe de la probabilité d'avoir une valeur de precipitations des occurence sur la periode 
    """
    X = []
    Y = []
    dr = duree_retour(data, recup_precip, qnh, superieur_a)
    occ = 0
    p = 1
    while p > seuil:
        p = proba_retour_au_moins(nb_periode, occ, dr)
        X.append(occ)
        Y.append(p)
        occ += 1
    plt.scatter(X, Y, label='Probabilité')
    plt.plot([0, occ], [0.95, 0.95], color='red', label='Seuil à 95%')
    plt.legend()
    plt.xlabel("Nombre d'occurences")
    plt.ylabel('Probabilité')
    plt.title("Probabilité du nombre d'occurence de plus de \n "+str(qnh) +
              'mm/jour de precipitation sur une periode de ' + str(int(nb_periode/12))+' ans')
    plt.savefig(
        'Figures_raw/'+conf.chemin_observations[-9:-5]+'/proba_retour_precip.svg', format='svg')
    if config.SHOW:
        plt.show()
    plt.close('all')
