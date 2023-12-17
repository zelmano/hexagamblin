"""
Programme basique en python3.8 permettant via matplolib de visualiser une grille hexagonale.

Elle propose simplement:
 - l'affichage des hexagones, avec des couleurs et une opacité
 - l'ajout de formes colorées sur les hexagones
 - l'ajout de liens colorés entre les hexagones

Contact: sebastien.gamblin@isen-ouest.yncrea.fr
"""

from __future__ import annotations

from abc import abstractmethod
from collections import defaultdict

from random import *
from typing import Dict, Tuple, List

import matplotlib.colors as mcolors
from matplotlib.patches import RegularPolygon
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.colors import LinearSegmentedColormap
import numpy as np

from Terrain import Terrain
from Rivieres import Riviere

Coords = Tuple[int, int]  # un simple alias de typage python


# il y a mieux en python :
# - 3.11: Coords: AliasType = Tuple[int, int]
# - 3.12: type Coords = Tuple[int, int]


class Forme:
    """Superclasse abstraite qui sauvegarde une couleur et impose une méthode 'get' qui retourne un Patch."""

    def __init__(self, color: str = "black", edgecolor: str = None):
        assert color in mcolors.CSS4_COLORS
        if edgecolor is not None:
            assert edgecolor in mcolors.CSS4_COLORS
        self._color = color
        self._edgecolor = edgecolor

    @abstractmethod
    def get(self, x: float, y: float, h: int) -> Patch:
        pass


class Rect(Forme):
    """Redéfinition d'une Forme pour un rectangle."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get(self, x: float, y: float, h: int) -> plt.Rectangle:
        return plt.Rectangle((x - h / 2, y - h / 2), h, h, facecolor=self._color, edgecolor=self._edgecolor)


class Circle(Forme):
    """Redéfinition d'une Forme pour un cercle."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get(self, x: float, y: float, h: int) -> plt.Circle:
        return plt.Circle((x, y), h / 2, facecolor=self._color, edgecolor=self._edgecolor)


class HexGridViewer:
    """
    Classe permettant d'afficher une grille hexagonale. Elle se crée via son constructeur avec deux arguments:
    la largeur et la hauteur.
    Deux attributs gèrent l'apparence des hexagones: colors et alpha, pour respectivement représenter la
    couleur et la transparence des hexagones.
    Chaque hexagone est représenté par une tuple : (x, y) spécifique dans la grille. Ces tuples sont les clés
    des dictionnaires colors et alpha, que vous pouvez modifier via les méthodes add_color et add_alpha.

    Il est aussi possible d'ajouter des symboles Rectangle ou Circle au milieu des hexagones, ainsi que des liens
    entre les centres des hexagones.

    Pour s'informer sur les HexGrid:
    Voir : https://www.redblobgames.com/grids/hexagons/#coordinates-offset pour plus d'informations.
    """

    def __init__(self, width: int, height: int):

        self.__width = width  # largueur de la grille hexagonale, i.e. ici "nb_colonnes"
        self.__height = height  # hauteur de la grille hexagonale, i.e. ici "nb_lignes"

        # modifié par défaut par matplolib, la modification ne sert à rien
        # mais est nécessaire pour calculer les points
        self.__hexsize = 10

        # couleur des hexagones : par défaut, blanc
        self.__colors: Dict[Coords, str] = defaultdict(lambda: "white")
        # transparence des hexagones : par défaut, 1
        self.__alpha: Dict[Coords, float] = defaultdict(lambda: 1)
        # symboles sur les hexagones, par défaut, aucun symbole sur une case.
        # Limitation : un seul symbole par case !
        self.__symbols: Dict[Coords, Forme | None] = defaultdict(lambda: None)
        # liste de liens à affichager entre les cases.
        self.__links: List[Tuple[Coords, Coords, str, int]] = []

    def get_width(self) -> int:
        return self.__width

    def get_height(self) -> int:
        return self.__height

    def add_color(self, x: int, y: int, color: str) -> None:
        assert self.__colors[(x, y)] in mcolors.CSS4_COLORS, \
            f"self.__colors type must be in matplotlib colors. What is {self.__colors[(x, y)]} ?"
        self.__colors[(x, y)] = color

    def add_alpha(self, x: int, y: int, alpha: float) -> None:
        assert 0 <= self.__alpha[
            (x, y)] <= 1, f"alpha value must be between 0 and 1. What is {self.__alpha[(x, y)]} ?"
        self.__alpha[(x, y)] = alpha


    def add_symbol(self, x: int, y: int, symbol: Forme) -> None:
        self.__symbols[(x, y)] = symbol

    def add_link(self, coord1: Coords, coord2: Coords, color: str = None, thick=2) -> None:
        self.__links.append((coord1, coord2, color if color is not None else "black", thick))

    def get_color(self, x: int, y: int) -> str:
        return self.__colors[(x, y)]

    def get_alpha(self, x: int, y: int) -> float:
        return self.__alpha[(x, y)]

    def get_neighbours(self, x: int, y: int) -> List[Coords]:
        """
        Retourne la liste des coordonnées des hexagones voisins de l'hexagone en coordonnées (x,y).
        """
        if y % 2 == 0:
            res = [(x + dx, y + dy) for dx, dy in ((1, 0), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1))]
        else:
            res = [(x + dx, y + dy) for dx, dy in ((1, 0), (1, 1), (0, 1), (-1, 0), (0, -1), (1, -1))]
        return [(dx, dy) for dx, dy in res if 0 <= dx < self.__height and 0 <= dy < self.__width]

    def show(self, hexgraph: HexGraphe=None, alias: Dict[str, str] = None, debug_coords: bool = False, show_altitude: bool = False) -> None:
        """
        Permet d'afficher via matplotlib la grille hexagonale. :param alias: dictionnaire qui permet de modifier le
        label d'une couleur. Ex: {"white": "snow"} :param debug_coords: booléen pour afficher les coordonnées des
        cases. Attention, le texte est succeptible de plus ou moins bien s'afficher en fonction de la taille de la
        fenêtre matplotlib et des dimensions de la grille.
        """

        if alias is None:
            alias = {}

        fig, ax = plt.subplots(figsize=(8, 8))
        ax.set_aspect('equal')

        h = self.__hexsize
        coords = {}
        for row in range(self.__height):
            for col in range(self.__width):
                x = col * 1.5 * h
                y = row * np.sqrt(3) * h
                if col % 2 == 1:
                    y += np.sqrt(3) * h / 2
                coords[(row, col)] = (x, y)

                center = (x, y)
                hexagon = RegularPolygon(center, numVertices=6, radius=h, orientation=np.pi / 6, edgecolor="none")
                hexagon.set_facecolor(self.__colors[(row, col)])
                hexagon.set_alpha(self.__alpha[(row, col)])

                # Ajoute du texte à l'hexagone
                if debug_coords:
                    text = f"({row}, {col})"  # Le texte que vous voulez afficher
                    ax.annotate(text, xy=center, ha='center', va='center', fontsize=8, color='black')
                if show_altitude:
                    text = f"({hexgraph.nodes[row,col]['altitude']})"  # Le texte que vous voulez afficher
                    ax.annotate(text, xy=center, ha='center', va='center', fontsize=8, color='black')

                # ajoute l'hexagone
                ax.add_patch(hexagon)

                # gestion des Formes additionnelles
                forme = self.__symbols[(row, col)]
                if forme is not None:
                    ax.add_patch(forme.get(x, y, h))

        for coord1, coord2, color, thick in self.__links:
            if coord1 not in coords or coord2 not in coords:
                continue
            x1, y1 = coords[coord1]
            x2, y2 = coords[coord2]
            plt.gca().add_line(plt.Line2D([x1, x2], [y1, y2], color=color, linewidth=thick))

        ax.set_xlim(-h, self.__width * 1.5 * h + h)
        ax.set_ylim(-h, self.__height * np.sqrt(3) * h + h)
        ax.axis('off')

        ks, vs = [], []
        for color in set(self.__colors.values()):
            if color in alias:
                ks.append(alias[color])
            else:
                ks.append(color)
            vs.append(color)

        gradient_cmaps = [
            LinearSegmentedColormap.from_list('custom_cmap', ['white', vs[i]]) for i in range(len(vs))]
        # Créez une liste de patch à partir des polygones
        legend_patches = [
            Patch(label=ks[i], edgecolor="black", linewidth=1, facecolor=gradient_cmaps[i](0.5), )
            for i in range(len(ks))]
        # Ajoutez la légende à la figure
        ax.legend(handles=legend_patches, loc='center left', bbox_to_anchor=(1, 0.5))
        plt.show()

def genererGrille(height, width, terrain=None):
    """
    Genere une grille de hauteur height et de largeur width, avec une hauteur aleatoire pour chaque case
    Si un terrain est spécifié, toute la grille est constituée de celui-ci
    Sinon la génération est aléatoire
    """
    nodes={}
    for i in range(height):
        for j in range(width):
            nodes[(i,j)]={}
            if terrain:
                nodes[(i, j)]["terrain"]=terrain
                nodes[(i, j)]["altitude"] = randint(0, 500)
            else:
                nodes[(i,j)]["terrain"]=(choices(list(Terrain), [0.1, 0.3, 0.2, 0.2, 0.2])[0])
                nodes[(i,j)]["altitude"] = randint(0,1000)
    return nodes


class HexGraphe:
    def __init__(self, nodes, height, width):
        self.nodes: Dict[Coords: Dict[str:int, str:int, str:List]] = nodes
        """
        Coords = Tuple(int, int) 
        dictionnaire de noeuds :
        -ayant comme clé un tuple des coordonnées d'un noeud, 
        -ayant en valeur un dictionnaire d'information sur le noeud
            -de clés : 
                -"terrain", valeur : Terrain (son type) : un des terrains parmis l'enum Terrain
                -"altitude", valeur : int alitude allant de 0 à 1000
                -"neighboors", valeur : liste des voisins
        
        {(x,y) : { "terrain":"xxx", "altitude":xxx, "neighboors":[(x,y),(x,y),(x,y)] }, pareil pour autre noeud }
        """
        self.height = height
        self.width = width
        for node in self.get_nodes():
            nodes[node]["neighbors"] = self.get_neighbours(node[0],node[1])
        self.villes=None


    def get_neighbours(self, x: int, y: int) -> List[Coords]:
        if y % 2 == 0:
            res = [(x + dx, y + dy) for dx, dy in ((1, 0), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1))]
        else:
            res = [(x + dx, y + dy) for dx, dy in ((1, 0), (1, 1), (0, 1), (-1, 0), (0, -1), (1, -1))]
        return [(dx, dy) for dx, dy in res if 0 <= dx < self.height and 0 <= dy < self.width]

    def get_nodes(self):
        return list(self.nodes.keys())

    def get_node(self,n):
        return self.nodes[n]

    def get_terrain(self,n):
        x, y = n
        return self.nodes[(x,y)]["terrain"]
    def get_altitude(self,n):
        x, y = n
        return self.nodes[(x,y)]["altitude"]

    def get_neighbors(self,n):
        x,y = n
        return self.nodes[(x, y)]["neighbors"]

    def get_max_altitude(self):
        """
        retourne le sommet le plus haut du graphe
        """
        max_altitude=0
        highest_node=None
        for node in self.get_nodes():
            if self.nodes[node]["altitude"]>max_altitude:
                highest_node=node
                max_altitude = self.nodes[node]["altitude"]
        return highest_node

    def get_villes(self):
        return list(self.villes.keys())

    def get_pcc(self):
        return [self.villes[i][j]["chemin"] for i in self.get_villes() for j in self.get_villes() if i!=j]
    def set_terrain(self,n,terrain):
        x,y=n
        self.nodes[(x,y)]["terrain"] = terrain

    def set_altitude(self,n,altitude):
        x, y = n
        self.nodes[(x,y)]["altitude"] = altitude

    def __repr__(self):
        for cle, valeur in self.nodes.items():
            print(f"{cle}: {valeur}")
        if self.villes:
            print(self.villes)
        return ""

    def bfs_propagation(self, centre,long):
        """
        Renvoie une liste de tuples (sommets,distance par rapport au centre)
        """
        visited = []  # creation de la file des noeuds visités (gris)
        visited.append(centre)
        result = []
        propa=[]
        compt=0
        neighbors_tmp = []
        while compt<=long:
            if not visited:
                compt += 1
                if compt>long:
                    return propa
                for i in neighbors_tmp:
                    visited.append(i)
                neighbors_tmp=[]
            tmp = visited.pop(0)
            propa.append((tmp, compt))
            result.append(tmp)
            fils = self.get_neighbors(tmp)

            for i in fils:
                if i not in visited and i not in result and i not in neighbors_tmp:
                    neighbors_tmp.append((i))

        return propa

    def propagation_terrain(self,centre,long,terrain):
        """Recupère une liste de tuples (sommets, distance par rapport au centre)
        Leur applique le terrain du centre et réduit leur altitude en fonction de leur distance par rapport au centre
        """
        propa = self.bfs_propagation(centre, long)
        #print(propa)
        hauteur_max = self.get_altitude(centre)
        #print(hauteur_max)
        montee = 1
        altitude = hauteur_max
        for coords, long in propa:


            #baisse la hauteur de 200 par unité de distance puis rajoute une valeur aléatoire entre -100 et 100
            # met la hauteur ou 0 si hauteur negative

            if terrain==Terrain.montagne:
                altitude = min(max(hauteur_max - montee * long * 150 + randint(-100, 100), 0), 1000)
                #print(altitude)
                if altitude>800:
                    self.set_altitude(coords, altitude)
                    self.set_terrain(coords, Terrain.neige)
                elif altitude>500:
                    self.set_altitude(coords, altitude)
                    self.set_terrain(coords, Terrain.montagne)


                else:
                    self.set_altitude(coords, altitude)
                    self.set_terrain(coords, Terrain.herbe)

            """
            #GENERER HERBE EN PROPAGATION MONTANTE ET DESCENDANTE CA MARCHE PAS
            #faudrait avoir constante hauteur à laquelle on fait + ou - X en fonction de montee, à chaque fois que long change
            if terrain==Terrain.herbe:
                altitude = min(max(altitude + montee * randint(-100, 100), 0), 500)
                print(altitude)
                self.set_terrain(coords,Terrain.herbe)
                self.set_altitude(coords, altitude)
                if altitude>500:
                    montee=-1
                    print(montee)

                if altitude==0:
                    montee=1
                    print(montee)
            """
            #print("hauteur", self.get_altitude(coords))

    def placer_montagnes(self,height,width):
        nb_montagne = 1+int(height*width/80)
        #print(nb_montagne)
        for i in range(nb_montagne):
            point=(randint(0,height-1),randint(0,width-1))
            self.nodes[point]["altitude"]=randint(700,1000)
            self.propagation_terrain(point,randint(2,4),Terrain.montagne)

    def placer_herbe(self,height, width):
        point=(height / 2, width / 2)
        self.nodes[point]["altitude"]=randint(0,300)
        self.propagation_terrain(point,max(height / 2, width / 2), Terrain.herbe)

    def placer_ville(self,height,width):
        self.villes = {}
        nb_ville = 4 #+ (height * width) // 400
        i = 0  # Initialisation de la variable i en dehors de la boucle while
        while i < nb_ville:
            a, b = randint(0, height - 1), randint(0, width - 1)
            if self.nodes[(a, b)]["terrain"] != Terrain.eau and (a, b) not in self.villes:
                self.villes[(a, b)]={}
                i += 1

        print('villes : ', self.get_villes())
        print(len(self.villes))

    def djikstra(self,s0,contraintes):
        d={}
        pred={}
        for i in self.get_nodes():
            d[i]=float('inf')
            pred[i]=None

        d[s0] = 0
        s=s0
        E=[]
        F=self.get_nodes()
        while F:
            mini=float('inf')
            for cle,valeur in d.items():
                if cle not in E and valeur<=mini:
                    mini=valeur
                    s=cle

            E.append(s)
            F.remove(s)
            for i in self.get_neighbors(s):
                if contraintes:
                    """
                    1.5 * plus dure de monter que de descendre
                    descendre ou monter 2 fois de 150 est plus simple que descendre d'un coup de 300
                    
                    """
                    if self.nodes[s]["terrain"]!=Terrain.eau and self.nodes[i]!=Terrain.eau:
                        poid = 2.5 if self.nodes[i]["terrain"]==Terrain.neige else (1.5 if self.nodes[i]["terrain"]==Terrain.montagne else 1)
                        montee= 1 if self.nodes[i]["altitude"]<self.nodes[s]["altitude"] else 1.5
                        poid+= ((((self.nodes[i]["altitude"] - self.nodes[s]["altitude"])/10)**2)*montee)/200
                        #print("difference = ",self.nodes[i]["altitude"] - self.nodes[s]["altitude"],", terrain = ",self.nodes[i]["terrain"],":",poid)
                        if d[i] > d[s] + poid:
                            d[i] = d[s] + poid
                            pred[i] = s
                else:
                    if d[i] > d[s] + 1:
                        d[i] = d[s] + 1
                        pred[i] = s

        return pred,d

    def pcc_ville_a_b(self,a,b,contraintes):
        """
        Va de b à a
        """
        pred, d = self.djikstra(a,contraintes)
        print(pred,d)
        tmp=b
        l=[]
        poid=0
        while tmp!=a:

            l.append(tmp)
            poid+=d[tmp] #faire un return l,d et adapter le reste du code
            tmp=pred[tmp]

        l.append(a)
        poid+=d[a]
        return l,poid

    def pcc_villes(self, contraintes=True):
        for i in self.get_villes():
            for j in self.get_villes():
                if i!=j:
                    chemin,poid = self.pcc_ville_a_b(j,i,contraintes)
                    self.villes[i][j]={}
                    self.villes[i][j]["chemin"] = chemin
                    self.villes[i][j]["poid"] = poid

        print(self.villes)


    def kruskalbien(self):
        temp = HexGraphe(self.nodes, self.height, self.width)
        temp.villes={}
        for i in self.get_villes():
            temp.villes[i]={}
        #temp.print()

        uf = UnionFind()
        l=[]
        chemin=[]
        for i in self.get_villes():
            uf.makeSet(i)

        #LAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        print("aaa")
        liste_villes=self.get_villes()
        for i in range(len(self.villes)):

            for j in range(i):

                print(self.villes[liste_villes[i]][liste_villes[j]])
                if self.villes[liste_villes[i]][liste_villes[j]]["poid"] != 0:
                    l.append((liste_villes[j], liste_villes[i], self.villes[liste_villes[i]][liste_villes[j]]["poid"],self.villes[liste_villes[i]][liste_villes[j]]["chemin"]))
        tri = sorted(l, key=lambda li: li[2])
        #print(tri)


        for i in tri:
            if uf.find(i[0])!=uf.find(i[1]):
                temp.villes[i[0]][i[1]]={}
                temp.villes[i[0]][i[1]]["poid"]=i[2]
                temp.villes[i[0]][i[1]]["chemin"]=i[3]
                uf.union(i[0],i[1])
                chemin.append(i)

        return chemin


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
        xr, yr = self.find(x), self.find(y)
        if xr!=yr:
            self.parent[xr]=yr

def question123():
    height = 10
    width = 10
    alpha_spread = 0.5
    grille = genererGrille(height, width)
    graphe = HexGraphe(grille, height, width)

    hex_grid = HexGridViewer(width, height)

    # affichage de la grille :
    for x, y in graphe.get_nodes():
        hex_grid.add_color(x, y, graphe.get_terrain((x, y)).value)
        # coefficient alpha entre alpha_spread et 1 pour une altitude entre 0 et 1000
        hex_grid.add_alpha(x, y, (graphe.get_altitude((x, y)) * alpha_spread) / 1000 + alpha_spread)

    # dictionnaire d'alias couleur nom de terrain pour la légende
    alias_terrains = {terrain.value: terrain.name for terrain in Terrain}
    hex_grid.show(alias=alias_terrains)

def question4_propagation():
    height = 10
    width = 10
    grille = genererGrille(height, width, terrain=Terrain.herbe)
    a = HexGraphe(grille, height, width)

    hex_grid = HexGridViewer(width, height)

    propa = a.bfs_propagation((4, 4), 3)
    # print(propa)
    for coords, long in propa:
        x, y = coords
        hex_grid.add_color(x, y, 'red')
        hex_grid.add_alpha(x, y, 1 - long * 0.2)
    hex_grid.show(debug_coords=True)

def question4_adaptation_montagne():
    # adaptation de la propagation avec des montagnes :
    height = 20
    width = 20
    grille = genererGrille(height, width, terrain=Terrain.neige)
    graphe = HexGraphe(grille, height, width)
    print(graphe)

    hex_grid = HexGridViewer(width, height)

    graphe.propagation_terrain((4, 4), 3, Terrain.montagne)

    graphe.propagation_terrain((15, 10), 2, Terrain.montagne)

    for x, y in graphe.get_nodes():
        hex_grid.add_color(x, y, graphe.get_terrain((x, y)).value)
        hex_grid.add_alpha(x, y, (graphe.get_altitude((x, y)) * (4 / 5)) / 1000 + 0.2)

    hex_grid.show(graphe, debug_coords=False, show_altitude=True)

def question5a():
    height = 10
    width = 10
    grille = genererGrille(height, width)
    graphe = HexGraphe(grille, height, width)
    print(graphe)
    print(graphe.get_max_altitude())
def question5b():
    height = 10
    width = 10
    grille = genererGrille(height, width, Terrain.neige)
    graphe = HexGraphe(grille, height, width)
    print(graphe)
    hex_grid = HexGridViewer(width, height)


    riviere = Riviere(graphe)
    riviere.placer_riviere(height, width)

    graphe.placer_ville(height, width)
    graphe.pcc_villes(contraintes=False)

    for x, y in graphe.get_nodes():
        hex_grid.add_color(x, y, graphe.get_terrain((x, y)).value)
        hex_grid.add_alpha(x, y, (graphe.get_altitude((x, y)) * (3 / 5)) / 1000 + 2 / 5)

    alias_terrains = {terrain.value: terrain.name for terrain in Terrain}
    hex_grid.show(graphe, debug_coords=False, show_altitude=True, alias=alias_terrains)

def question6():
    """pour generer une map clean aléatoire :
    mettre herbe partout :
    creer x montagnes aléatoirements avec pic le plus haut entre 700 et 1000
    pour chaque sommet : -si altitude > 800 : mettre neige
                         -si altitude < 500 : mettre herbe
    ensuite on rajoute des rivieres aléatoirement"""
    height = 40
    width = 40
    # alpha_spread = 0.5
    grille = genererGrille(height, width, terrain=Terrain.herbe)
    graphe = HexGraphe(grille, height, width)

    hex_grid = HexGridViewer(width, height)

    # graphe.placer_herbe(height,width)
    graphe.placer_montagnes(height, width)
    riviere = Riviere(graphe)
    riviere.placer_riviere(height, width)

    for x, y in graphe.get_nodes():
        hex_grid.add_color(x, y, graphe.get_terrain((x, y)).value)
        hex_grid.add_alpha(x, y, (graphe.get_altitude((x, y)) * (3 / 5)) / 1000 + 2 / 5)

    alias_terrains = {terrain.value: terrain.name for terrain in Terrain}
    hex_grid.show(graphe, debug_coords=False, show_altitude=False, alias=alias_terrains)

def question7():
    height = 20
    width = 20
    grille = genererGrille(height, width, terrain=Terrain.herbe)
    graphe = HexGraphe(grille, height, width)

    hex_grid = HexGridViewer(width, height)

    # graphe.placer_herbe(height,width)
    graphe.placer_montagnes(height, width)
    riviere = Riviere(graphe)
    riviere.placer_riviere(height, width)

    graphe.placer_ville(height, width)
    graphe.pcc_villes(contraintes=False)

    for x, y in graphe.get_nodes():
        hex_grid.add_color(x, y, graphe.get_terrain((x, y)).value)
        hex_grid.add_alpha(x, y, (graphe.get_altitude((x, y)) * (3 / 5)) / 1000 + 2 / 5)

    for x, y in graphe.get_villes():
        hex_grid.add_symbol(x, y, Circle("darkred"))

    for chemin in graphe.get_pcc():
        for i in range(len(chemin) - 1):
            hex_grid.add_link(chemin[i], chemin[i + 1], "black", thick=2)

    hex_grid.show(graphe, debug_coords=False, show_altitude=False)

def question8():
    height = 10
    width = 10
    grille = genererGrille(height, width, terrain=Terrain.herbe)
    graphe = HexGraphe(grille, height, width)

    hex_grid = HexGridViewer(width, height)

    # graphe.placer_herbe(height,width)
    graphe.placer_montagnes(height, width)

    riviere = Riviere(graphe)
    riviere.placer_riviere(height, width)

    graphe.placer_ville(height, width)
    graphe.pcc_villes(contraintes=True)

    for x, y in graphe.get_nodes():
        hex_grid.add_color(x, y, graphe.get_terrain((x, y)).value)

        if graphe.nodes[(x, y)]["terrain"] == Terrain.herbe:
            alpha = (graphe.get_altitude((x, y)) * 1.75 * (3 / 5)) / 1000 + 2 / 5
        elif graphe.nodes[(x, y)]["terrain"] == Terrain.montagne:
            alpha = ((graphe.get_altitude((x, y)) - 300) * 2 * (3 / 5)) / 1000 + 2 / 5
        else:
            alpha = (graphe.get_altitude((x, y)) * (3 / 5)) / 1000 + 2 / 5
        hex_grid.add_alpha(x, y, alpha)

    for x, y in graphe.get_villes():
        hex_grid.add_symbol(x, y, Circle("darkred"))

    for chemin in graphe.get_pcc():
        color = (random(), random(), random())
        for i in range(len(chemin) - 1):
            hex_grid.add_link(chemin[i], chemin[i + 1], color, thick=2)

    # print(graphe)
    hex_grid.show(graphe, debug_coords=False, show_altitude=True)

def question9():
    height = 20
    width = 20
    grille = genererGrille(height, width, terrain=Terrain.herbe)
    graphe = HexGraphe(grille, height, width)

    hex_grid = HexGridViewer(width, height)

    # graphe.placer_herbe(height,width)
    graphe.placer_montagnes(height, width)
    riviere = Riviere(graphe)
    riviere.placer_riviere(height, width)

    graphe.placer_ville(height, width)
    graphe.pcc_villes(contraintes=True)

    for x, y in graphe.get_nodes():
        hex_grid.add_color(x, y, graphe.get_terrain((x, y)).value)

        if graphe.nodes[(x, y)]["terrain"] == Terrain.herbe:
            alpha = (graphe.get_altitude((x, y)) * 1.75 * (3 / 5)) / 1000 + 2 / 5
        elif graphe.nodes[(x, y)]["terrain"] == Terrain.montagne:
            alpha = ((graphe.get_altitude((x, y)) - 300) * 2 * (3 / 5)) / 1000 + 2 / 5
        else:
            alpha = (graphe.get_altitude((x, y)) * (3 / 5)) / 1000 + 2 / 5
        hex_grid.add_alpha(x, y, alpha)

    for x, y in graphe.get_villes():
        hex_grid.add_symbol(x, y, Circle("darkred"))

    for chemin in graphe.get_pcc():
        # color = (random(), random(), random())
        for i in range(len(chemin) - 1):
            hex_grid.add_link(chemin[i], chemin[i + 1], "black", thick=3)

    chemins = graphe.kruskalbien()
    for chemin in chemins:
        print(chemin)
        path = chemin[3]
        for i in range(len(path) - 1):
            hex_grid.add_link(path[i], path[i + 1], "red", thick=1)

    # print(graphe)
    alias_terrains = {terrain.value: terrain.name for terrain in Terrain}
    hex_grid.show(graphe, debug_coords=False, show_altitude=True, alias=alias_terrains)
def main():
    #question123()
    #question4_propagation()
    #question4_adaptation_montagne()
    #question5a()
    #question5b()
    #question6()
    #question7()
    #question8()
    question9()

    

if __name__ == "__main__":
    main()

# # Quel algorithme utiliser pour générer une zone régulière qui s'étend sur la carte (i.e. toutes les cases à
# distance $i$ d'une case)?

# # Quel algorithme permettrait de tracer des rivières à partir d'un point donné sur la carte, en ajoutant une
# contrainte d'altitude descendante en prenannt le chemin le plus long possible ?

# # Quel algorithme utiliser pour aller d'un point A à un point B ?

# # Quel algorithme utiliser pour créer un réseau de routes le moins couteux possible entre x villes, pour qu'elles
# sont toutes interconnectées ?

##
