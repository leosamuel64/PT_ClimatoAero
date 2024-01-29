from metar import Metar

from codes.classes import *


def build_dict_metar(path):
    def clean_metars(metars):
        res=[]
        for m in metars:
            try:
                _ = Metar.Metar(m)
                res.append(m)
            except:
                ()
        return res
    
    file=open(path, 'r')
    keys = ['station','valid','tmpf','dwpf','relh','drct','sknt','p01i','alti','mslp','vsby','gust','skyc1','skyc2','skyc3','skyc4','skyl1','skyl2','skyl3','skyl4','wxcodes','ice_accretion_1hr','ice_accretion_3hr','ice_accretion_6hr','peak_wind_gust','peak_wind_drct','peak_wind_time','feel','metar','snowdepth']
    res={}
    for key in keys:
        res[key]=[]
    
    for ligne in file:
        elements = ligne.split(',')
        for i in range(len(elements)):
            res[keys[i]].append(elements[i])

    messages = clean_metars(res['metar'])
    temps = res['valid']
    metars = []
    for k in range(len(messages)):
        m = metar(messages[k],temps[k])
        metars.append(m)
    
    return metars

    
def charge_fichier(path):
    res=[]
    file=open(path,'r')
    for ligne in file:
        obs = observation(ligne)
        res.append(obs)
    return res

def reecrit_fichier_MT(fichier,fichier_corr):
    file=open(fichier,'r')
    rajout='''MONTPELLIER;1�15'43"E;43�27'05"N;1;'''
    temp = []
    for ligne in file:
        debut=ligne[0:9]
        fin=ligne[9:len(ligne)]
        temp.append(debut+rajout+fin)
    file=open(fichier_corr,'w')
    for ligne in temp:
        file.write(ligne)
    file.close()
    

        
        
        
        
    