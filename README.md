# IN1SA01_Implementation

####################################### TRAVAIL ACCOMPLI #######################################

Nous avons réussi à effectué toute les étapes. C'est-à-dire, la naissance de proies, leur veillissement, leur déplacement et leur reproduction et leur mort. De plus, les prédateurs se déplacent, se nourrissent se reproduisent et meurent. A la fin de notre programme, un graphique affiche le nombre d'individus par organisme en fonction du temps.

####################################### PROBLÈMES RENCONTRÉS #######################################

ETAPE 1 : AU PARADIS DES PROIES

Tout d'abord nous avons rencotré des problèmes d'affichage lors de la naissance des proies. Cependant, nous avons réussi à régler ce problème. En effet, la fonction naissance() n'était pas appelé au bon moment.

Le deuxième problème que nous avons eu, est que nos proies se déplacer plusieurs fois par tour. Lorsqu'on appele la fonction bouger(), une boucle parcourt toute les cases et vérifie si une proie est dedans. Si c'est le cas, elle la déplace. Après ce changement de case, la boucle continue, est peut si la proie a été déplacé dans une case en dessous par exemple, repassé sur une proie déjà déplacé lors du tour. Pour palier ce problème, nous avons mis en place une vérification des cases qui ont reçu une proie lors du tour.

ETAPE 2 : PLETHORE DE PROIES

Lors de cette étape, le principal problème rencontré était de trouver les case voisines et disponibles afin de ne pas faire naître une proie sur une case où se situait un parent. Nous avons réitéré la méthode de vérification, pour éviter que deux proies ou qu'une proie issue d'une reproduction, puisse se reporduire une deuxième fois lors du tour ou qu'une jeune proie se reproduise lors du tour de sa naissance.

####################################### IDÉE ORIGINALE #######################################

Nous avons décidé de modifier le fichier 'tkiteasy.py' afin de pouvoir nommer notre fenêtre.

A la fin du programme, une deuxième fenêtre s'ouvre affichant un graphique représentant le temps par boucle.

Lorsqu'il n'y a plus de prédateurs sur la carte, une surprise apparaît.
