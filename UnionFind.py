

class UnionFind():
  def __init__(self):
    self.parent={}

  def makeSet(self,x):
    self.parent[x]= None

  def find(self,x):
    if self.parent[x] is None:
      return x
    return self.find(self.parent[x])

  def union(self,x,y):
    #on trouve les racine
    xr, yr = self.find(x), self.find(y)
    #on les unis si elles sont différentes
    if xr!=yr:
      self.parent[xr]=yr