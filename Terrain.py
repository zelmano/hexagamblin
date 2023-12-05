from enum import Enum

class Terrain(Enum):
    """
    Liste des terrains possibles et la couleur associée
    """
    eau = 'blue'
    herbe = 'darkgreen'
    montagne = 'dimgrey'
    neige = 'whitesmoke'
    chemin = 'sienna'