from codes.fonctions_auxiliaires import *
import json

class metar:
    def __init__(self,ligne,date):
        annee=int(date[0:4])
        mois = int(date[5:7])
        jour = int(date[8:10])
        heure = int(date[11:13])
        minute = int(date[14:16])
        
        self.date = datetime.datetime(annee,mois,jour,heure,minute)
        self.message = ligne
        
class observation:
    def __init__(self, ligne):
        self.poste ,self.nom ,self.lon ,self.lat ,alt ,date ,hauteur_precipitation ,self.q_hauteur_precipitation ,duree_precipitation ,self.q_duree_precipitation ,temperature ,self.q_temperature ,dew_point ,self.q_dew_point ,temperature_mini ,self.q_temperature_mini ,heure_temperature_mini ,self.q_heure_temperature_mini ,temperature_maxi ,self.q_temperature_maxi ,heure_temperature_maxi ,self.q_heure_temperature_maxi ,duree_gel ,self.q_duree_gel ,qfe ,self.q_qfe ,qnh ,self.q_qnh ,self.geopotentiel ,self.q_geopotentiel ,self.qnh_mini ,self.q_qnh_mini ,self.vitesse_vent ,self.q_vitesse_vent ,self.direction_vent ,self.q_direction_vent ,self.vitesse_vent_instant_maxi ,self.q_vitesse_vent_instant_maxi ,self.direction_vent_instant_maxi ,self.q_direction_vent_instant_maxi ,self.heure_vent_instant_maxi ,self.q_heure_vent_instant_maxi ,self.humidite ,self.q_humidite ,self.humidite_mini ,self.q_humidite_mini ,self.heure_humidite_mini ,self.q_heure_humidite_mini ,self.humidite_maxi ,self.q_humidite_maxi ,self.heure_humidite_maxi ,self.q_heure_humidite_maxi ,self.nebulosite ,self.q_nebulosite ,self.nbas ,self.qnbas ,self.n1 ,self.qn1 ,self.c1 ,self.qc1 ,self.b1 ,self.qb1 ,self.n2 ,self.qn2 ,self.c2 ,self.qc2 ,self.b2 ,self.qb2 ,self.n3 ,self.qn3 ,self.b3 ,self.qb3 ,self.c3 ,self.qc3 ,self.n4 ,self.qn4 ,self.c4 ,self.qc4 ,self.b4 ,self.qb4 ,self.temps_present ,self.q_temps_present ,self.visi ,self.q_visi = ligne.split(';')
        
        self.date=convert_date(date)
        self.alt=int(alt)*3.281
        self.hauteur_precipitation=convert_float(hauteur_precipitation)
        self.duree_precipitation=convert_int(duree_precipitation)
        self.temperature = convert_float(temperature)
        self.dew_point = convert_float(dew_point)
        self.temperature_mini= convert_float(temperature_mini)
        self.temperature_maxi= convert_float(temperature_maxi)
        self.qfe=convert_float(qfe)
        self.qnh=convert_float(qnh)
        self.duree_gel=convert_int(duree_gel)
        self.heure_temperature_mini=convert_heure(heure_temperature_mini,self.date)
        self.heure_temperature_maxi=convert_heure(heure_temperature_maxi,self.date)
        self.qnh_mini=convert_float(self.qnh_mini)
        if not self.vitesse_vent=='':
            self.vitesse_vent=convert_float(self.vitesse_vent)*1.944
        self.direction_vent=convert_int(self.direction_vent)
        if not self.vitesse_vent_instant_maxi=='':
            self.vitesse_vent_instant_maxi=convert_float(self.vitesse_vent_instant_maxi)*1.944
        self.heure_vent_instant_maxi=convert_heure(self.heure_vent_instant_maxi,self.date)
        self.humidite=convert_float(self.humidite)
        self.humidite_mini =convert_float(self.humidite_mini)
        self.heure_humidite_mini  =convert_heure(self.heure_humidite_mini,self.date)
        self.humidite_maxi =convert_float(self.humidite_maxi)
        self.nebulosite=convert_int(self.nebulosite)
        self.visi=convert_int(self.visi)
        
    def __str__(self):
        txt="For only {price:.2f} dollars!"
        texte = """ ----- Observation du {date} à {nom} ({alti} ft) -----\n
        
        Temperature : {temp}°C (maxi : {tmaxi}°C | mini : {tmini}°C)
        Point de Rosée : {dp}°C | Humidité : {U}%
        Pression : QNH : {qnh} hPa | QFE : {qfe} hPa
        Vent : {vitesse_vent}kt / {direction_vent}°
        Nébulosité : {nebu}/8
        Visibilité : {visi} m
        
        """
        return texte.format(date=self.date, 
                            nom=self.nom,
                            alti=self.alt,
                            temp=self.temperature,
                            tmaxi=self.temperature_maxi,
                            tmini=self.temperature_mini,
                            qnh=self.qnh,
                            qfe=self.qfe,
                            dp=self.dew_point,
                            vitesse_vent=round(self.vitesse_vent,2),
                            direction_vent=self.direction_vent,
                            U=self.humidite,
                            nebu=self.nebulosite,
                            visi=self.visi
                            )

    def plafond(self):
        nuages=[(convert_int(self.n1),self.c1,self.b1),(convert_int(self.n2),self.c2,self.b2),(convert_int(self.n3),self.c3,self.b3),(convert_int(self.n4),self.c4,self.b4)]
        nebu_max=0
        couche_max = None
        for i in range(len(nuages)):
            if nuages[i][0]!='' and nuages[i][0]>nebu_max:
                nebu_max=nuages[i][0]
                couche_max=nuages[i]
        if nebu_max>4 and couche_max[2]!='':
            return couche_max
        else:
            return None

    def a_donnees_manquantes(self):
        tab = [self.q_hauteur_precipitation, self.q_duree_precipitation ,self.q_temperature ,self.q_dew_point ,self.q_temperature_mini ,self.q_heure_temperature_mini,self.q_temperature_maxi,self.q_heure_temperature_maxi ,self.q_duree_gel,self.q_qfe, self.q_qnh ,self.q_geopotentiel,self.q_qnh_mini,self.q_vitesse_vent,self.q_direction_vent,self.q_vitesse_vent_instant_maxi,self.q_direction_vent_instant_maxi ,self.q_heure_vent_instant_maxi ,self.q_humidite,self.q_humidite_mini,self.q_heure_humidite_mini,self.q_humidite_maxi, self.q_heure_humidite_maxi,self.q_nebulosite ,self.q_temps_present ,self.q_visi]
        labels = ["hauteur_precipitation", "duree_precipitation ","temperature ","dew_point ","temperature_mini ","heure_temperature_mini","temperature_maxi","heure_temperature_maxi ","duree_gel","qfe", "qnh ","geopotentiel","qnh_mini","vitesse_vent","direction_vent","vitesse_vent_instant_maxi","direction_vent_instant_maxi ","heure_vent_instant_maxi ","humidite","humidite_mini","heure_humidite_mini","humidite_maxi", "heure_humidite_maxi","nebulosite ","temps_present ","visi"]
        res = []
        
        for i in range(len(tab)):
            if tab[i] in ['n','m','d','r','']:
                res.append(labels[i])
                
        if self.temperature=='' and (not ('temperature' in res)):
            res.append('visi')
        if self.visi=='' and (not ('visi' in res)):
            res.append('visi')
                
        return res

    def altitude_pression(self):
        if self.qnh != '':
            return self.alt+(1013-self.qnh)*28
        else:
            return None

class avion:
    def __init__(self, code):
        
        
        file = open('data/avions.json','r')
        
        data = json.load(file)
        dico = data[code]
        
        self.code=code
        self.nom = dico['Nom_entier']
        self.max_cross_wind = dico["limit_cross_wind"]
        self.ifr = dico['IFR']
    
class aerodrome:
    def __init__(self, code):
        
        file = open('data/aerodromes.json','r')
        
        data = json.load(file)
        dico = data[code]
        
        self.code=code
        self.nom = dico['Nom']
        self.ifr_visi = dico["visi_ifr"]
        self.vfr_visi = dico["visi_vfr"]
        self.ifr_plafond = dico["plafond_ifr"]
        self.vfr_plafond = dico["plafond_vfr"]
        