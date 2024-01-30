from PIL import Image
import matplotlib.pyplot as plt
import math
import datetime
from codes.calculs import *
from codes.config import *


def rose_des_vents(data):
    '''
    Entrée : Liste des observations, liste des numéros de pistes
    Sortie : Graphique Rose des vents
    '''
    vd = vents_dominants_vitesse(data)
    
    ax = plt.subplot(111, polar=True)
    ax.set_theta_zero_location("N")
    ax.set_theta_direction(-1)
    ax.get_yaxis().set_visible(False)
    
    
    for d in vd: 
        i,m,s=vd[d]
        s+=i+m
        m+=i
        
        plt.bar(x=(d*10)*math.pi/180, height=s, width=math.pi*10/180, bottom=0,color="red")
        plt.bar(x=(d*10)*math.pi/180, height=m, width=math.pi*10/180, bottom=0,color="orange")
        plt.bar(x=(d*10)*math.pi/180, height=i, width=math.pi*10/180, bottom=0,color="green")
        
    # ax.set_title("Rose des vents ("+data[0].nom+")")
    plt.savefig('exports_raw/RDV_.svg',format='svg')
    
    plt.show()

    

def plot_temp(data):
    '''
    Entrée : Liste des observations
    Sortie : Graphique des températures en fonction de la date
    '''
    X=[]
    Y=[]
    maxi_calc, maxi_date=maxi_temp(data)
    mini_calc, mini_date=mini_temp(data)
    cnt=data[0].date
    for d in data:
        if not ('temperature' in d.a_donnees_manquantes()):
            X.append(d.temperature)
            Y.append(cnt)
                
            cnt+=datetime.timedelta(0,30*60)
        
    plt.plot_date(Y,X)
    plt.xlabel('Date')
    plt.ylabel('Température (°C)')
    plt.title('Température '+data[0].nom+'\n Température Maximum : '+str(maxi_calc)+'°C ('+str(maxi_date)+')\n Température Minimum : '+str(mini_calc)+'°C ('+str(mini_date)+')')
    plt.show()


def plot_qnh(data):
    '''
    Entrée : Liste des observations
    Sortie : Graphique des températures en fonction de la date
    '''
    X=[]
    Y=[]
    maxi_calc, maxi_date=maxi_qnh(data)
    mini_calc, mini_date=mini_qnh(data)
    cnt=data[0].date
    for d in data:
        if not ('qnh' in d.a_donnees_manquantes()):
    
            X.append(d.qnh)
            Y.append(cnt)
            
        cnt+=datetime.timedelta(0,30*60)
    plt.plot(Y,X)
    plt.xlabel('Date')
    plt.ylabel('Température (°C)')
    plt.title('QNH '+data[0].nom+'\n QNH Maximum : '+str(maxi_calc)+'hPa ('+str(maxi_date)+')\n QNH Minimum : '+str(mini_calc)+'hPa ('+str(mini_date)+')')
    plt.show()
    

def plot_weather(metars,seuil=0):
    '''
    Entrée : Liste des metars, seuil pour ignorer les temps rares
    Sortie : Histogramme des pourcentages de chaque temps présent
    '''
    weather = count_weather(metars)
    X=[]
    Y=[]
    temp=[]
    for key in weather.keys():
        temp.append([weather[key],key])
        
    temp.sort(reverse=True)
    long = len(metars)
    for (x,y) in temp:
        pourcentage=2*365*x/long
        if pourcentage>seuil:
            X.append(pourcentage)
            Y.append(y)
        
    plt.bar(Y,X,color=color_template().orange)
    addlabels(Y, X,'j/an')
    
    # plt.title('Météo ')
    plt.savefig('exports_raw/weather.svg',format='svg')
    plt.show()
    
    
def trace_phenomene(metars,code,show=True):
    '''
    Entrée : Liste des metars, code du phénomene (TS,-RA...), flag pour l'affichage ou les valeurs
    Sortie : Graphique du phénomène en fonction des mois
    '''
    res=count_weather_date(metars,code)
    X=['Jan','Fev','Mars','Avr','Mai', 'Juin', 'Juil','Aout','Sept','Oct','Nov','Dec']
    Y=[0 for _ in range (1,13)]
    cnt=[0 for _ in range (1,13)]
    deja_jour=[]
    for key_date in res.keys():
        mois = key_date.month
        jour = key_date.day
        year = key_date.year
        if code!='TS':
            value=res[key_date]
            Y[mois-1]+=value
            cnt[mois-1]+=24
        else:
            if not(datetime.datetime(year,mois,jour) in deja_jour):
                deja_jour.append(datetime.datetime(year,mois,jour))
                value=res[key_date]
                Y[mois-1]+=value
                cnt[mois-1]+=24
            
    if code!='TS':
        for k in range(len(Y)):
            Y[k]=30*Y[k]/cnt[k]
    else:
        for k in range(len(Y)):
            Y[k]=30*(Y[k]*24)/cnt[k]
    
    plt.bar(X,Y,color=color_template().orange)
    addlabels(X, Y,'j')
    
    if show:
        plt.savefig('exports_raw/Phenomene'+code+'.svg',format='svg')
        plt.show()
    else:
        return X,Y
    
def trace_tableau(column_labels,line_label,data_temp,nom,ajout=''):
    '''
    Entrée : Liste des labels, liste de liste des données
    Sortie : Tableau
    '''
    data_temp_2=[]
    for t in data_temp:
        tableau = format_temp_date(t,ajout)
        data_temp_2.append(tableau)
    
    data = []
    for k in range(len(data_temp_2)):
        data.append(ajoute_debut(data_temp_2[k],line_label[k]))
        
    data_head = ajoute_debut(data,column_labels)
    colors = [[color_template().fond_table for _ in range(len(data_head[0])) ] for _ in range(len(data_head))]
    for k in range(len(colors[0])):
        colors[0][k]=color_template().orange
    fig, ax = plt.subplots(1, 1)
    # ax.axis("tight")
    ax.axis("off")
    table = ax.table(cellText=data_head, cellColours=colors, loc="center")
    table.auto_set_font_size(False)
    table.set_fontsize(5)
    plt.savefig('exports_raw/Tableau'+nom+'.svg',format='svg')
    
    plt.show()

def trace_tableau_temp(data):
    """
    Entrée : Observation
    Sortie : Tableau des temperature max, min et moyenne avec les records par mois
    """
    
    t_max = tableau_climato_temp(data, max)
    t_min = tableau_climato_temp(data, min)
    t_moy = tableau_moyenne_temp(data)

    trace_tableau(  ['-','Jan','Fev','Mars','Avr','Mai', 'Juin', 'Juil','Aout','Sept','Oct','Nov','Dec'],
                    ['Max','Min', 'Moy'],
                    [t_max,t_min,t_moy],'température','°C')
    
def trace_tableau_qnh(data):
    """
    Entrée : Observation
    Sortie : Tableau des temperature max, min et moyenne avec les records par mois
    """
    
    t_max = tableau_climato_qnh(data, max)
    t_min = tableau_climato_qnh(data, min)
    t_moy = tableau_moyenne_qnh(data)
    
    maxi = max(t_max)[0]
    mini = min(t_min)[0]
    moy= round(moyenne(t_moy),0)
    

    trace_tableau(  ['-','Jan','Fev','Mars','Avr','Mai', 'Juin', 'Juil','Aout','Sept','Oct','Nov','Dec','Record'],
                    ['Max','Min', 'Moy'],
                    [t_max+[maxi],t_min+[mini],t_moy+[str(moy)]],'QNH','hPa')
    
def trace_limitations(data,aeronef,ad,piste):
    """
    Entrée : Observation, avion, Numéro de la piste, aerodrome
    Sortie : Graphique des pourcentages de non-accessibilité de l'aérodrome par l'aéronef en fonction des mois
    """
    res=limitations(data,aeronef,piste,ad)
    X=['Jan','Fev','Mars','Avr','Mai', 'Juin', 'Juil','Aout','Sept','Oct','Nov','Dec']
    
    plt.bar(X,res,color=color_template().orange)
    addlabels(X, res,'j')
    
    plt.savefig('exports_raw/limit_'+aeronef.code+'.svg',format='svg')
    plt.show()
    
def trace_donnees_manquantes(data):
    """
    Entrée : Observation
    Sortie : tableau des pourcentages des données manquantes par paramètres
    """
    calc = calcul_donnees_manquantes(data)
    res=[]
    keys=[]
    for key in calc.keys():
        res.append([round(calc[key],2)])
        keys.append(key)
        
    trace_tableau(['Données','Données Manquantes (%)'],
                keys,
                res,'Miss_Data')

    

def affiche_table_contingence(data,pas_abs,pas_ord,fonction_couple,texte):
    """
    Entrée : Observation, catégories en abscisse, catégories en ordonnée, fonction de création des couples, texte pour la case (0,0)
    Sortie : table de contingence du couple en fonction des catégories en image
    """
    table = calcul_table_contingence(data,pas_abs,pas_ord,fonction_couple)
    trace_tableau(  [texte]+pas_abs+['>'],
                    pas_ord+['>'],
                    table,'tc'+fonction_couple.__name__,'')
    

def affiche_tc_visi_plafond(data):
    """
    Entrée : Observation,
    Sortie : table de contingence visi/plafond
    """
    pas_visi = [800,1500,5000,10000] # Visi
    pas_plafond = [50,100,200,400,1500,5000] # Plafond
    affiche_table_contingence(data,pas_visi,pas_plafond,couple_contingence_visi_plafond, 'Visibilité\n Plafond          ')

def trace_tableau_gel(data):
    """
    Entrée : Observation,
    Sortie : tableau du nombre de jour moyen de gel par mois
    """
    tab = compte_gel_mois(data)
    
    trace_tableau(  ['-','Jan','Fev','Mars','Avr','Mai', 'Juin', 'Juil','Aout','Sept','Oct','Nov','Dec'],
                    ['jours/mois'],
                    [tab],'gel','j/m')
    

def trace_tableau_precipitation(data):
    """
    Entrée : Observation
    Sortie : Tableau des precipitations max et moyenne avec les records par mois
    """
    
    t_max = max_precipitation_mois(data)
    t_moy = moyenne_precipitation_mois(data)
    
    maxi = max(t_max)[0]
    moy= round(moyenne(t_moy),0)
    

    trace_tableau(  ['mm/jour','Jan','Fev','Mars','Avr','Mai', 'Juin', 'Juil','Aout','Sept','Oct','Nov','Dec','Record'],
                    ['Max', 'Moy'],
                    [t_max+[str(maxi)],t_moy+[str(moy)]],
                    'precipitation','')
    
def trace_tableau_vent_travers(data,piste):
    """
    Entrée : Observation
    Sortie : Tableau des vents traversiés max et moyen avec les records par mois
    """
    
    t_max = max_vent_t_mois(data,piste)
    t_moy = moyenne_vent_t_mois(data,piste)
    
    maxi = max(t_max)[0]
    moy= round(moyenne(t_moy),0)
    

    trace_tableau(  ['-','Jan','Fev','Mars','Avr','Mai', 'Juin', 'Juil','Aout','Sept','Oct','Nov','Dec','Record'],
                    ['Max', 'Moy'],
                    [t_max+[str(maxi)],t_moy+[str(moy)]],
                    'Vent_travers','kt')
    
def trace_tableau_vent_effectif(data,piste):
    """
    Entrée : Observation
    Sortie : Tableau des vents traversiés max et moyen avec les records par mois
    """
    
    t_max = max_vent_e_mois(data,piste)
    t_moy = moyenne_vent_e_mois(data,piste)
    
    maxi = max(t_max)[0]
    moy= round(moyenne(t_moy),0)
    

    trace_tableau(  ['-','Jan','Fev','Mars','Avr','Mai', 'Juin', 'Juil','Aout','Sept','Oct','Nov','Dec','Record'],
                    ['Max', 'Moy'],
                    [t_max+[str(maxi)],t_moy+[str(moy)]],
                    'Vent_effectif','kt')
    
def affiche_coeff_pistes(data,ad,seuil_vent):
    coeff_p=coeff_pistes(data,ad,seuil_vent)
    X,Y=[],[]
    for piste in coeff_p.keys():
        X.append(str(piste))
        Y.append(coeff_p[piste])
        
    plt.bar(X,Y,color=color_template().orange)
        
    addlabels(X, Y,'%')
    
    plt.savefig('exports_raw/coeff_pistes.svg',format='svg')
    plt.show()