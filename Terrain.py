from enum import Enum

class Terrain(Enum):
    """
    Liste des terrains possibles et la couleur associée
    """
    eau = 'blue'
    herbe = 'darkgreen'
    montagne = '#2B2B2A'
    neige = 'whitesmoke'
    chemin = 'sienna'