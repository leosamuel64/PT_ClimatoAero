def round_wind(wind_deg):
    '''
    Entrée : Direction du vent en °
    Sortie : Vent correspondant à la piste
    '''
    res=round(wind_deg/10)
    return res

        
def assoc_temps_present(path):
    '''
    Entrée : Chemin vers fichier code temps present
    Sortie : Dictionnaire code -> Description
    '''
    file=open(path,'r')
    res = {}
    for ligne in file:
        code,descr = ligne.strip().split(';')
        res[int(code)]=descr
    return res
