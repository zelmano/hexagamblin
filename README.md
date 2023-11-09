# hexagamblin

## Questions

### Questions : modélisation de base

- [ ] Q1: Proposez une implémentation d’un graphe, qui représente une grille hexagonale et qui possède toutes les propriétés d’un graphe.

- [ ] Q2: Proposez une extension de cette implémentation, permettant :
   - [ ] de labeliser les sommets par un type de terrain de votre choix (herbe, montagne, route, eau, etc...).
   - [ ] de labeliser les sommets par une altitude.

- [ ] Q3: Tester ce programme en ajoutant des types de terrain aléatoire et des altitudes aléatoires. Vous pouvez afficher le résultat grâce au programme hexgrid_viewer.py, en utilisant les couleurs pour signifier les terrains et la transparence pour signifier l’altitude.

### Questions : algorithmes de génération

- [ ] Q4: Quel algorithme utiliser pour générer une zone régulière qui s’étend sur la carte (i.e. toutes les cases à distance i d’une case) et comment l’adapter? Implémentez-le.

- [ ] Q5: 
   - [ ] créer une méthode permettant de trouver le sommet le plus haut de votre carte.
   - [ ] Quel algorithme permettrait de tracer des rivières à partir d’un point donné sur la carte, en ajoutant une contrainte d’altitude descendante en prenant le chemin le plus long possible?
   - [ ] Que pouvez-vous ajoutez pour créer des embranchements de rivières? Quelle est cette structure obtenue ?

- [ ] Q6: Proposez maintenant un algorithme, qui, s’inspirant des deux prédécedents, génère une carte aléatoirement, de sorte à ce que les altitudes soient "logiques" et que les types de terrains aient une cohérence, avec des rivières.

- [ ] Extension Bonus: l’eau peut ne pas être une rivière, par exemple, avec les lacs. Quelle contrainte cela ajoute au programme? Comment faire?

### Questions : exploitation des données

- [ ] Q7: Posez des villes aléatoirement sur votre carte. Quel algorithme utiliseriez-vous pour générer les routes entre ces villes de sorte à ce qu’elles soient le plus rapide à emprunter (sans les contraintes de terrain et d’altitude)? Implémentez votre solution. Quelle est la complexité de votre algorithme? Comparez les temps de calculs de cet algorithme en fonction de la taille de votre grille hexagonale et du nombre de villes souhaité, grâce à un graphique.

- [ ] Q8: Quelle modification apporter afin de pouvoir prendre en compte les différences de type et d’altitude de vos cases? Comment faire pour qu’il soit impossible de traverser de l’eau? Comparez les résultats avec et sans ces contraintes.

- [ ] Q9: Quel algorithme utiliser pour créer un réseau de routes le moins couteux possible entre x villes, pour qu’elles sont toutes accessibles les unes par rapport aux autres?

- [ ] Q10: Créer un algorithme, qui permet à un marchand de visiter toutes les villes en minimisant son parcours sur la route et de revenir à sa ville initiale.

- [ ] Extension Bonus: Admettons que nous disposons des moyens de transports autres que terrestres. Quelles modifications apporteriez-vous afin d’ajouter des bateaux ou des avions, par exemple? (Implémentation non demandée, juste des pistes de réflexion).

