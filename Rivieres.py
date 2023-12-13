from random import *
from Terrain import Terrain

class Riviere:
    def __init__(self, hexgrid):
        self.hexgrid = hexgrid
        self.proba_embranch = 0.01

    def dfs_riviere(self,n,proba_embranch=None):
        if proba_embranch==None:
            proba_embranch=self.proba_embranch
        branches=[]

        visited = []  # creation de la pile des noeuds visités (gris)
        visited.append(n)
        result = []
        pred = {}
        pred[n]="/"

        while visited:
            tmp = visited.pop()
            result.append(tmp)
            #fils = self.get_neighbors(tmp)
            fils = self.hexgrid.get_neighbors(tmp)
            #print(visited)
            for i in fils:
                if i not in visited and i not in result and self.nodes[i]["altitude"]<=self.nodes[tmp]["altitude"]:
                    pred[i] = tmp
                    visited.append(i)

                    if random() < proba_embranch:
                        branches.append(i)

        #print("Prédécesseurs : ", pred)

        #embranchements
        for i in branches:
            if random()<proba_embranch and len(visited)>0:
                self.dfs_riviere(i)

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
        if len(liste)<=2:
            return False

        for i in liste:
            self.nodes[i]["terrain"]=Terrain.eau
        return True

    def placer_riviere(self,height, width):
        nb_riviere = 1+int(height * width / 50)
        #print("nb riviere",nb_riviere)

        """
        for i in range(nb_riviere):
            point = (randint(0, height - 1), randint(0, width - 1))
            riviere=self.dfs_riviere(point)
            if riviere==False:
                i-=1
        """

        nb_rivieres_placees=0
        while nb_rivieres_placees < nb_riviere:
            point = (randint(0, height - 1), randint(0, width - 1))
            if self.dfs_riviere(point):
                nb_rivieres_placees += 1#on compte que les succes de plaçage de rivière