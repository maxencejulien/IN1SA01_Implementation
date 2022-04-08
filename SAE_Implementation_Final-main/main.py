#coding: utf-8
from tkinter.constants import FLAT
from tkiteasy import *
from random import *
import matplotlib.pyplot as plt
import time
from constante import *
from fonction import *


# PRECISER TKEASY

# TABLE DESTINEES AUX GRAPHES
nbProie = []
nbPredateur = []
temps = []

# ouverture de fenÃªtre
win = ouvrirFenetre(LARGEUR, HAUTEUR, 'Simulation d\'une évolution d\'une biocénose')

# CARTE REPRÉSENTE L'ENSEMBLE DE NOS CASES
carte = {}
# DISO REPRÉSENTE L'ENSEMBLE DES CASES LIBRES
dispo = set()
# CARREAU REPRÉSENTE LES CARRÉS GRAPHIQUES REPRÉSENTANT NOS PROIES ET PRÉDATEURS
carreau = []

# CREATION CARTE
creation_carte(carte, LARGEUR, HAUTEUR, DIMC, dispo)

# CREATION QUADRILLAGE
creation_quadrillage(win , LARGEUR, HAUTEUR, DIMC)


naissance(carte, 60, dispo, dispo, 'Proie')
naissance(carte, 5, dispo, dispo, 'Predateur')

affichage(win, carte, carreau)

while win.recupererClic() == None:

	debut = time.time()

	grandir(carte)
	perteEnergie(carte)
	mourir(carte, dispo, DPRO)
	naissance(carte, FPRO, dispo, dispo, 'Proie')

	############# PARTIE MANGER #############
	for e in carte:
		if carte[e][0] == 'Predateur':
			ca = caseAutour(e, DIMC, True)
			manger(carte, e, ca, dispo)


	############# PARTIE BOUGER #############
	dejaBouge = set()
	if len(dispo) > 0:
		for e in carte:
			if e not in dejaBouge:
				
				if carte[e][0] == 'Proie':

					ca = caseAutour(e, DIMC)
					cad = caseAutourDispo(carte, ca)

					if len(cad) > 0:

						newpos = choice(cad)
						
						direct = obtenir_direction(e, newpos, DIMC)

						bouger(carte, e, dispo, dejaBouge, direct)
				
				elif carte[e][0] == 'Predateur':
					
					ca = caseAutour(e, DIMC, True, FLAIR)
					cad = caseAutourDispo(carte, ca)

					if len(cad) > 0:

						proieProche = algoChasse(carte, ca, e)

						if proieProche != None:

							direct = obtenir_direction(e, proieProche, DIMC)

							if (e[0]+direct[0], e[1]+direct[1]) in dispo:

								bouger(carte, e, dispo, dejaBouge, direct)

						else:

							newpos = choice(cad)

							direct = obtenir_direction(e, newpos, DIMC)

							if (e[0]+direct[0], e[1]+direct[1]) in dispo:

								bouger(carte, e, dispo, dejaBouge, direct)


	############# PARTIE REPRODUCTION #############
	dejaRepro = set()
	if len(dispo) > 0:
		for e in carte:
			if e not in dejaRepro:
				
				if carte[e][0] == 'Proie':
					ca = caseAutour(e, DIMC, True)
					reproduction(carte, e, ca, dejaRepro, dispo, 'Proie')
				
				elif carte[e][0] == 'Predateur':
					ca = caseAutour(e, DIMC, True)
					reproduction(carte, e, ca, dejaRepro, dispo, 'Predateur', NRJREPROPRED)
	
	
	# SUPPRESSION DE TOUS LES ELEMENTS GRAPHIQUES
	suppElementGraphique(carreau, win)

	# AFFICHAGE DES ELEMENTS GRAPHIQUES
	affichage(win, carte, carreau)

	# COMPTE LE NOMBRE D'ORGANISME PRESENT SUR LA CARTE
	compte = compte_organisme(carte, nbProie, nbPredateur)

	if compte[1] == 0:

		win.afficherImage(LARGEUR//2, HAUTEUR//2, 'game_over.png', 'center')


	temps.append(time.time()-debut)

	win.pause(.05)


# fermeture fenêtre
win.fermerFenetre()


# CREATION D'UN GRAPHIQUE REPRESENTANT LE NOMBRE D'INDIVIDUS PAR ORGANISMES
# EN FONCTION DU NOMBRE DE TOURS
plt.plot(range(len(nbProie)), nbProie, color='green', label='nombre de proie')
plt.plot(range(len(nbPredateur)), nbPredateur, color='red', label='nombre de prédateur')
plt.title("Simulation d'une évolution d'une biocénose")
plt.xlabel("Nombre de tours")
plt.ylabel("Nombre d'individus")
plt.legend()
plt.show()

# CREATION D'UN GRAPHIQUE REPRESENTANT LE TEMPS REQUIS
# EN FONCTION DU NOMBRE DE TOURS
plt.plot(range(len(temps)), temps, color='green', label='temps')
plt.title("Temps par boucle")
plt.xlabel("Nombre de tours")
plt.ylabel("Temps en secondes")
plt.legend()
plt.show()
