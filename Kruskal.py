from UnionFind import UnionFind

class Kruskal:
  def __init__(self,hexgrid):
    self.hexgrid=hexgrid

  def kruskal(self):
    uf = UnionFind()
    for i in self.hexgrid.get_nodes():
      uf.makeSet(i)

    #arêtes de l'arpm
    chemin = []
    tri=sorted(self.hexgrid.get_all_edges(), key=lambda li: li[2])
    
    #on ajoute les arêtes de l'arpm
    for i in tri:
      a,b,poids=i
      if uf.find(a)!=uf.find(b):
        chemin.append(i)
        uf.union(a,b)

    return chemin
  
