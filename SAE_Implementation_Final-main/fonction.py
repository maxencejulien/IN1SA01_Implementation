from random import *
from constante import *
from math import *

def affichage(fenetre, dictio, listObjetGraphique):

	"""
	La fonction parcourt un dictio et crée des rectangles ... pour les proies
	et des rectangles ... pour les prédateurs

	Paramètres :
		dictio -> dict
		fenetre -> objet
		listObjetGraphique -> list
	"""

	for e in dictio:
		if dictio[e][0] == 'Proie':
			c = fenetre.dessinerRectangle(e[0]+1, e[1]+1, DIMC-1, DIMC-1, 'yellow')
			#c = win.dessinerDisque(e[0], e[1], DIMC//2, 'red')
			#c = fenetre.afficherImage(e[0]+1, e[1]+1, 'pacman.png')
			listObjetGraphique.append(c)
		elif dictio[e][0] == 'Predateur':
			c = fenetre.dessinerRectangle(e[0]+1, e[1]+1, DIMC-1, DIMC-1, 'red')
			#c = fenetre.afficherImage(e[0], e[1], 'fantome.png')
			listObjetGraphique.append(c)


def naissance(dictio, nbNaissance, parmiLesCases, caseDisCarte, organisme):

	"""
	La fonction naissance permet de générer aléatoirement sur un ensemble de cases
	donné un certain nombre d'organismes

	Paramètres:
		dictio -> dict
		nbNaissance -> int
		parmiLesCases -> list
		caseDisCarte -> set
		organisme -> str
	"""

	indiceNais = 0
	newNaiss = []

	while len(parmiLesCases) > 0 and indiceNais < nbNaissance:

		posN = sample(parmiLesCases, 1)
		posN = posN[0]

		if organisme == 'Proie':
			dictio[posN] = [organisme, 0]
		elif organisme == 'Predateur':
			dictio[posN] = [organisme, EDEPPRE]
		newNaiss.append(posN)
		caseDisCarte.remove(posN)

		indiceNais += 1

	return newNaiss


def grandir(dictio):

	"""
	La fonction 'grandir' permet aux proies de veillir en gagnant de l'âge

	Paramètres:
		dictio -> dict 
	"""

	for e in dictio:
		if dictio[e][0] == 'Proie':
			dictio[e][1] += 1

def perteEnergie(dictio):

	"""
	La fonction 'perteEnergie' permet aux prédateurs de perdre de l'énergie

	Paramètre:
		dictio -> dict
	"""

	for e in dictio:
		if dictio[e][0] == 'Predateur':
			dictio[e][1] -= 1

def mourir(dictio, caseDisCarte, ageMort):

	"""
	La fonction 'mourir' permet de vérifier si des proies ont dépassé
	un certain âge, ou si les prédateurs n'ont plus d'énergie

	Paramètres:
		dictio -> dict
		caseDisCarte -> set
		ageMort -> int
	"""

	for e in dictio:
		if dictio[e][0] == 'Proie' and dictio[e][1] >= ageMort:
			dictio[e] = [None, None]
			caseDisCarte.add(e)
		elif dictio[e][0] == 'Predateur' and dictio[e][1] <= 0:
			dictio[e] = [None, None]
			caseDisCarte.add(e)
 
def caseAutour(pos, dimensionC, sansPos = False, rayon = 1):

	"""
	La fonction caseAutour permet de récupérer une liste comprenant toutes
	les cases voisines d'une case dont la case donnée. Il y a la possibilité de
	ne sélectionner uniquement les cases voisines avec le paramètre sansPos.

	Paramètres:
		pos -> tuple
		dimensionC -> int
		sansPos -> boolean
		rayon -> int 

	Retour:
		case -> list
	"""

	case = []

	for x in range(-rayon*dimensionC, rayon*dimensionC+1, dimensionC):
		for y in range(-rayon*dimensionC, rayon*dimensionC+1, dimensionC):
			if ( 0 <= pos[0]+x < LARGEUR-LARGEUR%DIMC) and  (0 <= pos[1]+y < HAUTEUR-LARGEUR%DIMC):
				case.append((pos[0]+x, pos[1]+y))

	if sansPos:
		case.remove(pos)

	return case

def caseAutourDispo(dictio, caseAutour):

	"""
	La fonction 'caseAutourDispo' permet de récupérer parmi une liste de cases
	données, les cases disponibles, les cases ne possédant pas de proies ou de
	prédateurs.

	Paramètres:
		dictio -> dict
		caseAutourDispo -> list

	Retour:
		case -> list
	"""

	case = []

	for c in caseAutour:
		if dictio[c][0] == None:
			case.append(c)

	return case

def reproduction(dictio, pos, caseAut, verif, caseDisCarte, organisme, enerReproPred=20):

	"""
	La fonction 'reproduction' permet de faire reporduire deux organismes autour d'eux.

	Paramètres:
		dictio -> dict
		pos -> tuple
		caseAut -> list
		verif -> list
		caseDisCarte -> set
		organisme -> str
		enerReproPred -> int
	"""

	for case in caseAut:
		if dictio[case][0] == 'Proie' and case not in verif:

			ca = caseAutour(case, DIMC, True)
			ca.remove(pos)

			caseAut.remove(case)
			caseAut.extend(ca)

			touteCaseAutour = caseAut

			touteCaseAutourDis = caseAutourDispo(dictio, touteCaseAutour)

			posN = naissance(dictio, 1, touteCaseAutourDis, caseDisCarte, organisme)

			if len(posN) > 0:
				#caseDisCarte.remove(posN[0])

				verif.add(pos)
				verif.add(case)
				verif.add(posN[0])

			break

		
		elif dictio[case][0] == 'Predateur' and dictio[case][1] >= enerReproPred and case not in verif:

			
			posN = naissance(dictio, 1, caseDisCarte, caseDisCarte, organisme)

			if len(posN) > 0:
				#caseDisCarte.remove(posN[0])

				verif.add(pos)
				verif.add(case)
				verif.add(posN[0])

			break
		

def bouger(dictio, pos, caseDisCarte, verif, direction):

	"""
	La fonction 'bouger' permet à un organisme de se déplacer dans une case voisine disponible
	dans le carte.

	Paramètres:
		dictio -> dict
		pos -> tuple
		caseDisCarte -> set
		verif -> list
		direction -> tuple
	"""

		

	dictio[(pos[0]+direction[0], pos[1]+direction[1])] = [dictio[pos][0], dictio[pos][1]]
	caseDisCarte.remove((pos[0]+direction[0], pos[1]+direction[1]))

	dictio[pos] = [None, None]
	caseDisCarte.add(pos)

	verif.add((pos[0]+direction[0], pos[1]+direction[1]))

def manger(dictio, pos, parmiLesCases, caseDisCarte):

	"""
	La fonction 'manger' permet aux prédateurs de manger une proie quand elle est dans
	une case voisine au prédateur.

	Paramètres:
		dictio -> dict
		pos -> tuple
		parmiLesCases -> list
		caseDisCarte -> set
	"""

	for case in parmiLesCases:
		if dictio[case][0] == 'Proie':
			dictio[case] = [None, None]
			dictio[pos][1] += MIAM
			caseDisCarte.add(case)

			break

def algoChasse(dictio, parmiLesCases, pos):

	"""
	La fonction 'algoChasse' permet de repérer la proie
	la plus proche d'un organisme

	Paramètre:
		dictio -> dict
		parmiLesCases -> list
		pos -> tuple

	Retour:
		casePlusProche -> tuple ou None
	"""
	
	caseProie = set()

	for case in parmiLesCases:
		if dictio[case][0] == 'Proie':
			caseProie.add(case)

	if len(caseProie) != 0:


		caseVoisine = caseAutour(pos, DIMC, True, 1)

		for case in caseVoisine:
			if case in caseProie:
				return None


		plusProche = float('inf') # float('inf') génère un nombre 'infini', très grand
		casePlusProche = (0, 0)

		for case in caseProie:
			if sqrt(((pos[0]-case[0])**2 + (pos[1]-case[1])**2)) < plusProche:
				plusProche = sqrt(((pos[0]-case[0])**2 + (pos[1]-case[1])**2)) 	# utilisation de la formule de la distance 
				casePlusProche = (case)											# entre deux points grâce à ses coordonnées

		return casePlusProche

	else:

		return None

	
def obtenir_direction(posDep, posArr, dimensionC):

	"""
	La fonction 'obtenir-direction' permet de déterminer
	une direction sous forme d'un tuple contenant
	la direction horizontale et verticale

	Paramètre:
		posDep -> tuple
		posArr -> tuple
		dimensionC -> int

	Retour:
		une direction -> tuple
	"""

	x, y = 0, 0
						
	if posArr[0] > posDep[0]:
		x = dimensionC
	elif posArr[0] < posDep[0]:
		x = -dimensionC
	
	if posArr[1] > posDep[1]:
		y = dimensionC
	elif posArr[1] < posDep[1]:
		y = -dimensionC

	return (x, y)

def creation_carte(dictio, largeur, hauteur, dimensionC, caseDisCarte):

	"""
	La fonction 'creation_carte' permet d'insérer dans un dictionnaire
	des 'cases' contenant des proies ou des prédateurs ou rien

	Paramètre:
		dictio -> dict
		largeur -> int
		hauteur -> int
		dimensionC -> int
		caseDisCarte -> set
	"""

	for x in range(0, largeur-(largeur%dimensionC), dimensionC):
		for y in range(0, hauteur-(hauteur%dimensionC), dimensionC):
			# LE DICTIONNAIRE CARTE PREND EN CLÉ LES POSITIONS DES CASES
			# ET EN VALEUR UN TABLEAU COMPRENANT CE QU'IL Y A DEDANS
			# ET L'ÂGE OU L'ÉNERGIE
			dictio[(x, y)] = [None, None]
			# L'ENSEMBLE DISPO PREND TOUTES LES POSITIONS
			caseDisCarte.add((x, y))

def creation_quadrillage(fenetre, largeur, hauteur, dimensionC):

	"""
	La fonction 'creation_quadrillage' permet de créer un quadrillage
	représentant notre carte

	Paramètre:
		fenetre -> objet
		largeur -> int
		hauteur -> int
		dimensionC -> int
	"""

	for x in range(0, largeur, dimensionC):
		fenetre.dessinerLigne(x, 0, x, hauteur, 'white')
	for y in range(0, hauteur, dimensionC):
		fenetre.dessinerLigne(0, y, largeur, y, 'white')


def compte_organisme(dictio, tabComptProie, tabComptPred):

	"""
	La fonction 'compte_organisme' permet de comptabiliser les proies
	et les prédateurs présent sur la carte

	Paramètre:
		dictio -> dict
		tabComptProie -> list
		tabComptPred -> list

	Retour:
		2 listes contenant le nombre de proies et de prédateurs
	"""

	compteurProie = 0
	compteurPred = 0
	for e in dictio:
		if dictio[e][0] == 'Proie':
			compteurProie += 1
		elif dictio[e][0] == 'Predateur':
			compteurPred += 1

	tabComptProie.append(compteurProie)
	tabComptPred.append(compteurPred)

	return (compteurProie, compteurPred)

def suppElementGraphique(tabElement, fenetre):

	"""
	La fonction 'suppElementGraphique' permet de supprimer d'une liste
	tous les éléments graphiques

	Paramètre:
		tabElement -> list
		fenetre -> list
	"""

	for x in tabElement:
		fenetre.supprimer(x)
	del tabElement[:]