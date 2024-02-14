
class color_template:
    def __init__(self):
        self.orange = (246/255, 137/255, 34/255)
        self.bleu = (0/255, 176/255, 231/255)
        self.gris = (75/255, 77/255, 81/255)
        self.fond_table = (1, 1, 1)


class config:
    PHENOMENE_PONDERATION = {'TS': 2*24,
                             'RA': 2*2,
                             'DZ': 2*2
                             }
    SEUIL_VENT_CALME = 2  # En kt
    SHOW = False
    flotte = ['TOBA',
              'TB20',
              'DA40',
              'DA42',
              'CP10',
              'B58',
              'PIVI']
    phenomenes = ['BR',
                  'RA',
                  'FG',
                  'TS']
    liste_ad = ['LFBR', 'LFLN', 'LFLS', 'LFMK', 'LFMT', 'LFPM']
    code_ciel_invisible = [0,10,43,45,47,49]