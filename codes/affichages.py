
import matplotlib.pyplot as plt
from codes.fonctions_auxiliaires_mto import *
import math
import datetime
from codes.calculs import *


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
        
    plt.bar(Y,X)
    plt.title('Météo ')
    plt.show()
    
    
def trace_phenomene(metars,code,show=True):
    '''
    Entrée : Liste des metars, code du phénomene (TS,-RA...), flag pour l'affichage ou les valeurs
    Sortie : Graphique des températures en fonction de la date
    '''
    res=count_weather_date(metars,code)
    X=[]
    Y=[]
    for key_date in res.keys():
        X.append(key_date)
        value=res[key_date]
        Y.append(value)
    plt.bar(X,Y)
    plt.title('Répartition de '+code)
    if show:
        plt.show()
    else:
        return X,Y

