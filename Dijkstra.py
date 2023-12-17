from Terrain import Terrain

class Dijkstra:
  def __init__(self, hexgrid):
    self.hexgrid = hexgrid

  def dijkstra(self,s0,contraintes):
    d = {}
    pred = {}
    for i in self.hexgrid.get_nodes():
        d[i] = float('inf')
        pred[i] = None

    d[s0] = 0
    s = s0
    E = []#liste des noeuds visités
    F = self.hexgrid.get_nodes()#liste des noeuds non visités

    #jusqu'à ce que tous les noeuds soient visités
    while F:
      #trouve le noeud non visité avec la dist minimale
      mini = float('inf')
      for cle,valeur in d.items():
        if cle not in E and valeur <= mini:
          mini = valeur
          s = cle

      #marque le noeud comme visité
      E.append(s)
      F.remove(s)

      #pour chaque voisin du noeud
      for i in self.hexgrid.get_neighbors(s):
        #avec contraintes
        if contraintes:
          if self.hexgrid.get_terrain(s) != Terrain.eau and self.hexgrid.get_terrain(i) != Terrain.eau:
            poid = 2.5 if self.hexgrid.get_terrain(i) == Terrain.neige else (1.5 if self.hexgrid.get_terrain(i) == Terrain.montagne else 1)
            montee = 1 if self.hexgrid.get_altitude(i) < self.hexgrid.get_altitude(s) else 1.5
            poid += ((((self.hexgrid.get_altitude(i) - self.hexgrid.get_altitude(s)) / 10) ** 2) * montee) / 200
            if d[i] > d[s] + poid:
              d[i] = d[s] + poid
              pred[i] = s
        #sans contraintes (poids=1)
        else:
          if d[i] > d[s] + 1:
            d[i] = d[s] + 1
            pred[i] = s

    return pred, d

  def pcc_ville_a_b(self,a,b,contraintes):
    pred,d = self.dijkstra(a,contraintes)
    tmp = b
    chemin = []
    poids = 0
    #tant que la ville actuelle n'est pas la ville de départ:
    while tmp != a:
      chemin.append(tmp)
      poids += d[tmp]
      tmp = pred[tmp]

    chemin.append(a)
    poids += d[a]
    return chemin, poids

  def pcc_villes(self, contraintes=True):
    #pour toutes les villes
    for i in self.hexgrid.get_villes():
      for j in self.hexgrid.get_villes():
        #on ne calcule pas le pcc d'une ville à elle-même
        if i != j:
          chemin, poids = self.pcc_ville_a_b(j, i, contraintes)
          self.hexgrid.villes[i][j] = {}
          self.hexgrid.villes[i][j]["chemin"] = chemin
          self.hexgrid.villes[i][j]["poids"] = poids
