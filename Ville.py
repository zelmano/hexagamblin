from random import *
from Terrain import Terrain

class Ville:
  def __init__(self,hexgrid):
    self.hexgrid=hexgrid
    self.villes={}

  def placer_ville(self,height,width):
    self.villes = {}
    nb_ville = 4#1 + (height * width) // 400
    i = 0
    while i < nb_ville:
      #coordonnées aléatoires dans la grille
      l,c = randint(0,height-1), randint(0,width-1)
      #si ça ne correspond pas à de l'eau ou à une ville
      if self.hexgrid.get_terrain((l,c)) != Terrain.eau and (l,c) not in self.villes:
        self.villes[(l,c)]={}
        i += 1

def get_villes(self):
    return list(self.villes.keys())
