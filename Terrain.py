from enum import Enum

class Terrain(Enum):
    """
    Liste des terrains possibles et la couleur associée
    """
    eau = 'blue'
    herbe = 'green'
    montagne = 'grey'
    neige = 'white'
    chemin = 'sienna'