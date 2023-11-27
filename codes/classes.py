from codes.fonctions_auxiliaires import *

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
        self.poste ,self.nom ,self.lon ,self.lat ,alt ,date ,hauteur_precipitation ,self.qrr1 ,duree_precipitation ,self.qdrr1 ,temperature ,self.qt ,dew_point ,self.qtd ,temperature_mini ,self.qtn ,heure_temperature_mini ,self.qhtn ,temperature_maxi ,self.qtx ,heure_temperature_maxi ,self.qhtx ,duree_gel ,self.qdg ,qfe ,self.qpstat ,qnh ,self.qpmer ,self.geopotentiel ,self.qgeop ,self.qnh_mini ,self.qpmermin ,self.vitesse_vent ,self.qff ,self.direction_vent ,self.qdd ,self.vitesse_vent_instant_maxi ,self.qfxi ,self.direction_vent_instant_maxi ,self.qdxi ,self.heure_vent_instant_maxi ,self.qhxi ,self.humidite ,self.qu ,self.humidite_mini ,self.qun ,self.heure_humidite_mini ,self.qhun ,self.humidite_maxi ,self.qux ,self.heure_humidite_mini ,self.qhux ,self.nebulosite ,self.qn ,self.nbas ,self.qnbas ,self.n1 ,self.qn1 ,self.c1 ,self.qc1 ,self.b1 ,self.qb1 ,self.n2 ,self.qn2 ,self.c2 ,self.qc2 ,self.b2 ,self.qb2 ,self.n3 ,self.qn3 ,self.b3 ,self.qb3 ,self.c3 ,self.qc3 ,self.n4 ,self.qn4 ,self.c4 ,self.qc4 ,self.b4 ,self.qb4 ,self.temps_present ,self.qww ,self.visi ,self.qvv = ligne.split(';')
        
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
        self.vitesse_vent=convert_float(self.vitesse_vent)*1.944
        self.direction_vent=convert_int(self.direction_vent)
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
            if nuages[i][0]>nebu_max:
                nebu_max=nuages[i][0]
                couche_max=nuages[i]
        if nebu_max>4:
            return couche_max
