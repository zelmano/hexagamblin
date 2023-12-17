from random import *
from Terrain import Terrain

class Riviere:
    def __init__(self, hexgrid):
        self.hexgrid = hexgrid
        self.proba_embranch = 0.01

    def dfs_riviere(self,n,proba_embranch=None, embranche=False):
        if proba_embranch==None:
            proba_embranch=self.proba_embranch

        visited = []  # creation de la pile des noeuds visités (gris)
        visited.append(n)
        result = []
        pred = {}
        pred[n]="/"

        branches=[]
        embr=False
        while visited:
            tmp = visited.pop()
            result.append(tmp)
            fils = self.hexgrid.get_neighbors(tmp)
            #print(visited)
            for i in fils:
                #if i not in visited and i not in result and self.nodes[i]["altitude"]<=self.nodes[tmp]["altitude"]:
                if i not in visited and i not in result and self.hexgrid.get_altitude(i)<=self.hexgrid.get_altitude(tmp):
                    pred[i] = tmp
                    visited.append(i)
                    """
                    if random() < proba_embranch and not embranche and not embr:
                        if self.dfs_riviere(i, proba_embranch, embranche=True) == "oui":
                            embr = True
                            print("ouiiiiiiiiiii", i)
                    else:
                        proba_embranch*=3
                    """

        #print("Prédécesseurs : ", pred)

        #embranchements

        #rivière principale
        liste=[]
        #print("result",result)
        for i in result:
            liste_tmp = []
            while pred[i]!="/":
                liste_tmp.append(i)
                i=pred[i]
            liste_tmp.append(i)
            if len(liste_tmp)>len(liste):
                liste=liste_tmp
                #print(liste)
        #print(liste)

        if len(liste) > 4:
            for i in liste:
                self.hexgrid.set_terrain(i, Terrain.eau)
            tmp=None
            while tmp is None or tmp in liste:
                tmp=result[randint(6,len(result)-1)]

            print("tmp", tmp)
            liste_tmp = []
            while pred[tmp] != "/":
                liste_tmp.append(tmp)
                tmp = pred[tmp]
            liste_tmp.append(tmp)
            for i in liste_tmp:
                self.hexgrid.set_terrain(i, Terrain.eau)

            return True

        """
        if len(liste)>1 and embranche:
            for i in liste:
                self.hexgrid.set_terrain(i, Terrain.eau)
        """
        return False


    def placer_riviere(self,height, width):
        nb_riviere = 1+int(height * width / 100)
        #print("nb riviere",nb_riviere)

        nb_rivieres_placees=0
        while nb_rivieres_placees < nb_riviere:
            point = (randint(0, height - 1), randint(0, width - 1))
            if self.dfs_riviere(point):
                nb_rivieres_placees += 1#on compte que les succes de plaçage de rivière
                print(point)