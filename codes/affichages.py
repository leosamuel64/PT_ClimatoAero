from PIL import Image
import matplotlib.pyplot as plt
import math
import datetime
from codes.calculs import *
from codes.config import *


def rose_des_vents(data,runways):
    '''
    Entrée : Liste des observations, liste des numéros de pistes
    Sortie : Graphique Rose des vents
    '''
    vd = vents_dominants_p(data)
    ax = plt.subplot(111, polar=True)
    ax.set_theta_zero_location("N")
    ax.set_theta_direction(-1)
    for d in vd: 
        if d in runways:
            plt.bar(x=(d*10)*math.pi/180, height=vd[d], width=math.pi*10/180, bottom=0,color="green")
        elif (d+1)%36 in runways or (d-1)%36 in runways:
            plt.bar(x=(d*10)*math.pi/180, height=vd[d], width=math.pi*10/180, bottom=0,color="yellow")
        elif (d+2)%36 in runways or (d-2)%36 in runways:
            plt.bar(x=(d*10)*math.pi/180, height=vd[d], width=math.pi*10/180, bottom=0,color="orange")
        else:
            plt.bar(x=(d*10)*math.pi/180, height=vd[d], width=math.pi*10/180, bottom=0,color="red")
    ax.set_title("Rose des vents ("+data[0].nom+")")
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
        if d.qnh!=0:
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
        pourcentage=100*x/long
        if pourcentage>seuil:
            X.append(pourcentage)
            Y.append(y)
        
    plt.bar(Y,X,color=color_template().orange)
    # plt.title('Météo ')
    plt.savefig('fig.svg',format='svg')
    plt.show()
    
    
def trace_phenomene(metars,code,show=True):
    '''
    Entrée : Liste des metars, code du phénomene (TS,-RA...), flag pour l'affichage ou les valeurs
    Sortie : Graphique des températures en fonction de la date
    '''
    res=count_weather_date(metars,code)
    X=['Jan','Fev','Mars','Avr','Mai', 'Juin', 'Juil','Aout','Sept','Oct','Nov','Dec']
    Y=[0 for _ in range (1,13)]
    for key_date in res.keys():
        mois = key_date.month
        value=res[key_date]
        Y[mois-1]+=value
    plt.bar(X,Y,color=color_template().orange)
    if show:
        plt.savefig('fig.svg',format='svg')
        plt.show()
    else:
        return X,Y
    
def trace_tableau(column_labels,line_label,data_temp):
    '''
    Entrée : Liste des labels, liste de liste des données
    Sortie : Tableau
    '''
    data_temp_2=[]
    for t in data_temp:
        tableau = format_temp_date(t,'°C')
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
    plt.savefig('fig.svg',format='svg')
    
    plt.show()

def trace_tableau_temp(data):
    t_max = tableau_climato(data, max)
    t_min = tableau_climato(data, min)
    t_moy = tableau_moyenne(data)

    trace_tableau(  ['-','Jan','Fev','Mars','Avr','Mai', 'Juin', 'Juil','Aout','Sept','Oct','Nov','Dec'],
                    ['Max','Min', 'Moy'],
                    [t_max,t_min,t_moy])
    
def trace_limitations(data,aeronef,ad,piste):
    """
    Entrée : Observation, avion, Numéro de la piste, aerodrome
    Sortie : Graphique des pourcentages de non-accessibilité de l'aérodrome par l'aéronef en fonction des mois
    """
    res=limitations(data,aeronef,piste,ad)
    X=['Jan','Fev','Mars','Avr','Mai', 'Juin', 'Juil','Aout','Sept','Oct','Nov','Dec']
    
    plt.bar(X,res,color=color_template().orange)
    addlabels(X, res,'%')
    
    plt.savefig('fig.svg',format='svg')
    plt.show()