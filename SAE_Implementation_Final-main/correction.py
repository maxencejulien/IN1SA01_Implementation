#coding: utf-8
from tkiteasy import *
import random
import matplotlib.pyplot as pyplt

#DEFINES ###################################################################
SIZECASE=5 # taille d'une case en pixels
NBCASES=90  # nb de cases
TOURS = 300
tout = set([(c,l) for c in range(NBCASES) for l in range(NBCASES)])

#PROIES
REPRO=True # est-ce que deux proies qui se touchent se reproduisent?
FBIRTHPROIE = 3 # fréquence d'apparition des proies  (nb tours)
LIFEPROIE = 40  # durée de vie max d'une proie
NBPROIES_START = 10 # nombre de proies introduites au lancement

#PREDATEURS
LIFEPRED = 60 # durée de vie max d'un prédateur
NRJPRED = 15  # énergie de départ d'un prédateur (-1 par tour)
NRJBIRTH = 20 # énergie requise pour se reproduire
NRJMIAM =  3  # énergie obtenue en mangeant
NRJMAX  =  60 # énergie max
NBPRED_START = 30 # nombre de prédateurs introduits au lancement
DISTFLAIR = 10 # distance à laquelle le prédateur sent la proie
nbpred = 0
"""Conditions générant de beaux cycles
#PROIES
REPRO=True # est-ce que deux proies qui se touchent se reproduisent?
FBIRTHPROIE = 1 # fréquence d'apparition des proies  (nb tours)
LIFEPROIE = 40  # durée de vie max d'une proie
NBPROIES_START = 40 # nombre de proies introduites au lancement

#PREDATEURS
LIFEPRED = 60 # durée de vie max d'un prédateur
NRJPRED = 15  # énergie de départ d'un prédateur (-1 par tour)
NRJBIRTH = 20 # énergie requise pour se reproduire
NRJMIAM =  6  # énergie obtenue en mangeant
NBPRED_START = 20 # nombre de prédateurs introduits au lancement
DISTFLAIR = 15 # distance à laquelle le prédateur sent la proie
"""

"""Conditions stables petite population proies sans pred et sans repro
REPRO=False
SIZECASE=20
NBCASES=30
FBIRTHPROIE = 5
LIFEPROIE = 40
NBPROIES_START = 10"""


################################################################################
# assOgfx
################################################################################
# def assOgfx(proies_age, proies_objgfx, pred_age, pred_objgfx, pred_nrj, carte,msg):
#     global dobj
#     assert(len(dobj)==len(proies_age)+len(pred_age)), print("SHIT1",msg)
#     assert(len(dobj)==len(proies_objgfx)+len(pred_objgfx)), print("SHIT2",msg)
#     assert(len(dobj)==len(carte)), print("SHIT3",msg)

################################################################################
# plusTuple
################################################################################
def plusTuple(t,u):
    return((t[0]+u[0],t[1]+u[1]))

################################################################################
# dessinerTerrain
################################################################################
def dessinerTerrain():
    for x in range(SIZECASE,SIZECASE*NBCASES,SIZECASE):
        g.dessinerLigne(x,0,x,SIZECASE*NBCASES,"#333333")

    for y in range(SIZECASE,SIZECASE*NBCASES,SIZECASE):
        g.dessinerLigne(0,y,SIZECASE*NBCASES,y,"#333333")

################################################################################
# dessiner
################################################################################
def dessiner(c,qui):
    global nbpred
    z = tab2grafx(c)
    if qui == "pred":
        color = "red"
        nbpred += 1
    else:
        color = "green"
    return g.dessinerDisque(z[0]+SIZECASE/2,z[1]+SIZECASE/2,SIZECASE/3,color)

################################################################################
# tab2grafx
################################################################################
def tab2grafx(c):
#     print (f"{c} => ({c[0]*SIZECASE},{c[1]*SIZECASE})")
    return (c[0]*SIZECASE,c[1]*SIZECASE)

################################################################################
# naissanceProie
################################################################################
def naissanceProie(nbp, proies_age, proies_objgfx, carte,npr):
    global dobj
    if type(nbp)==tuple:
        c,l = nbp[0],nbp[1]
        if (c,l) not in carte:
#             if (c,l) in npr or (c,l) in pred_objgfx or (c,l) in proies_age or (c,l) in proies_objgfx:
#                 print("FUCK 1: naissance forcée en",(c,l), (c,l) in npr , (c,l) in pred_objgfx , (c,l) in proies_age , (c,l) in proies_objgfx)
#                 g.actualiser()
#                 input()
            o = dessiner((c,l),"proie")
            dobj[o] = True
            proies_age[(c,l)]  = LIFEPROIE
            proies_objgfx[(c,l)]  = o
            carte[(c,l)] = o # à revoir?
        return

    oqp = set(carte.keys())
    dispos = list(tout-oqp)
    random.shuffle(dispos)
    nbn = min(nbp,len(dispos))
#     print(nbn,"naissances")
    for i in range(nbn):
        c,l = dispos.pop()
#         print(c,l)
        o = dessiner((c,l),"proie")
        dobj[o] = True
        proies_age[(c,l)]  = LIFEPROIE
        proies_objgfx[(c,l)]  = o
        carte[(c,l)] = o # à revoir?
#     input()
#         print(f"Proie {(c,l)} is born")

################################################################################
# naissancePred
################################################################################
def naissancePred(pred_age, pred_objgfx, pred_nrj, carte):
    global nbpred, dobj
    c = random.randint(0,NBCASES-1)
    l = random.randint(0,NBCASES-1)

    if (c,l) not in carte:
#         if (c,l) in pred_age or (c,l) in pred_objgfx or (c,l) in proies_age or (c,l) in proies_objgfx:
#             print("FUCK 2")
#             input()
        o = dessiner((c,l),"pred")
        dobj[o]=False
        pred_age[(c,l)] = LIFEPRED
        pred_nrj[(c,l)] = NRJPRED
        pred_objgfx[(c,l)]  = o
        carte[(c,l)] = o # à revoir?
#         print(f"Pred {(c,l)} is born")
    return (c,l)

def dansTerrain(c):
    return 0<=c[0]<NBCASES and 0<=c[1]<NBCASES

################################################################################
# voisinage
################################################################################
def voisinage(c,carte, proies_age,pred_age):
#     print("voisinage===================",c)
    vois = set([(-1,0),(1,0),(0,-1),(0,1)])
    if c[0]==0:
        vois.discard((-1,0))
    elif c[0]==NBCASES-1:
        vois.discard((1,0))

    if c[1]==0:
        vois.discard((0,-1))
    elif c[1]==NBCASES-1:
        vois.discard((0,1))

    vois2 = set()
    repro = False
#     print("vois possible",vois)
    for v in vois:
#         print(v,"?")
#         print("in carte",plusTuple(c,v) in carte, "in pred_age:",plusTuple(c,v) in pred_age,"and in pred_nrj",plusTuple(c,v) in pred_nrj,"and in predobjgfx",plusTuple(c,v) in pred_objgfx,"in proies_age",plusTuple(c,v) in proies_age,"in proies_obj",plusTuple(c,v) in proies_objgfx)
        if plusTuple(c,v) not in carte:
#             print("...not in carte, but in pred_age:",plusTuple(c,v) in pred_age,"and in pred_nrj",plusTuple(c,v) in pred_nrj,"and in predobjgfx",plusTuple(c,v) in pred_objgfx)
            vois2.add(v)
        elif plusTuple(c,v) in proies_age:
#             print("...fornik!")
            repro = True
#     print("vois2 possible",vois2,"repro",repro)
                    
    if not vois2:
        return None, None
    birth = None
    if REPRO and repro and len(vois2)>1:
        birth = random.choice(list(vois2))
#         print("birth sur",birth)
        vois2.discard(birth)
    move = random.choice(list(vois2))
#     print("move sur",move)
    return move,birth

################################################################################
# distance
################################################################################
def distance(a,b):
    return abs(a[0]-b[0])**2 + abs(a[1]-b[1])**2

################################################################################
# hunt
################################################################################
def hunt(c,carte,pr_age):
#     print("hunt",c)
    vois = set([(-1,0),(-1,-1),(-1,1),(1,-1),(1,1),(1,0),(0,-1),(0,1)])
    if c[0]==0:
        vois.discard((-1,0)); vois.discard((-1,1)); vois.discard((-1,-1))
    elif c[0]==NBCASES-1:
        vois.discard((1,0)); vois.discard((1,-1)); vois.discard((1,1))

    if c[1]==0:
        vois.discard((0,-1)); vois.discard((1,-1)); vois.discard((-1,-1))
    elif c[1]==NBCASES-1:
        vois.discard((0,1)); vois.discard((-1,1)); vois.discard((1,1))

#     print("vois",vois)
    vois2 = set()
    for v in vois:
#         print(v,"?")
        if plusTuple(c,v) in pr_age:
#             print("sortie miam vers",v)
            return v, True
        
        if plusTuple(c,v) not in carte:
            vois2.add(v)
#     print("vois2",vois2)
                    
    if not vois2:
#         print("sortie no vois2")
        return None, False

    vois2 = { plusTuple(c,v):v for v in vois2}
#     print("c",c,"=================vois2",vois2)
#     input()
    av  = 3
    flag= True
    pos = plusTuple(c,(-1,-2))
#     print("pos",pos)
#     input()
    v   = (1,0)
    while av < DISTFLAIR or not flag:
        if dansTerrain(pos) and pos in pr_age:
#             print("potentiel")
            d = distance(pos,c)
            for w in vois2:
                if distance(w,pos)<d:
#                     print("c",c,": proies trouvée en",pos,"av",av)
#                     print("sortie1: w",w,"vois2[w]",vois2[w])
                    return vois2[w], False
#             print("pas mieux dans vois2")
        for i in range(av):
            pos = plusTuple(pos,v)
#             print("pos",pos)
#             input()
            if dansTerrain(pos) and pos in pr_age:
#                 print("potentiel")
                d = distance(pos,c)
                for w in vois2:
                    if distance(w,pos)<d:
#                         print("c",c,": proies trouvée en",pos,"av",av)
#                         print("sortie2: w",w,"vois2[w]",vois2[w])
                        return vois2[w], False
#                 print("pas mieux dans vois2")
        v = (-v[1],v[0])
        if flag:
            av += 1
        flag = not flag
        
    r = vois2[random.choice(list(vois2))]
#     print("sortie random: vois2",vois2,"list(vois2)",list(vois2),"r",r)
    return r, False


# 
# 
#     plusProcheProie = NBCASES**2*2
#     bestVois = None
#     for v in vois2:
#         for p in proies_age:
# #             if v[0]*p[0]>=0 or v[1]*p[1]>=0: #optim?
#                 dist = distance(plusTuple(c,v),p)
#                 if dist<DISTFLAIR**2 and dist < plusProcheProie:
#                     plusProcheProie = dist
#                     bestVois = v
# #     print("move vers",bestVois)
#     if bestVois == None:
#         bestVois = random.choice(list(vois2))
#     return bestVois, False

################################################################################
# life
################################################################################
def life(pred_age, pred_objgfx, pred_nrj, proies_age, proies_objgfx, carte):
    global dobj
#     print(f"PRED AVANT {len(pred_age)} {len(pred_objgfx)} {len(pred_nrj)}")
#     print(f"PROIES AVANT {len(proies_age)} {len(proies_objgfx)}")
#     print(f"CARTE AVANT {len(carte)}")
#     print(f"pred_age entrée: {pred_age}")
#     print(f"pred_nrj entrée: {pred_nrj}")
#     assert(len(proies_age)==len(proies_objgfx)), print("fail1")
#     assOgfx(proies_age, proies_objgfx, pred_age, pred_objgfx, pred_nrj, carte,"début life")
    npred_age = dict(pred_age)
    for c in pred_age:
#         print(f"PRED allons-y pour {c}")
#         assOgfx(proies_age, proies_objgfx, npred_age, pred_objgfx, pred_nrj, carte,"début tour pred_age")
        npred_age[c] -= 1 # on diminue l'âge
        pred_nrj[c] -= 1 # et l'énergie
        if npred_age[c]==0 or pred_nrj[c]==0: # si dead
#             if pred_nrj[c]!=0:
#                 print("PRED DEAD DE FAIM!!",c)
#             else:
#                 print("PRED DEAD de vieillesse!!",c)
            g.supprimer(pred_objgfx[c])
            npred_age.pop(c)
            del dobj[pred_objgfx[c]]
            pred_objgfx.pop(c)
            pred_nrj.pop(c)
            carte.pop(c)
#             assOgfx(proies_age, proies_objgfx, npred_age, pred_objgfx, pred_nrj, carte,"post dead pred age ou nrj")
        else:
#             print("not dead")
            move,eat = hunt(c, carte, proies_age)
#             print("hunt renvoie",move, eat)
            if move:
                nextpos = plusTuple(move,c)
#                 print(f"PRED {c} bouge de {move} vers {nextpos}")
#                 assOgfx(proies_age, proies_objgfx, npred_age, pred_objgfx, pred_nrj, carte, "ap hunt")
                if eat:
#                     print("MIAM!!",nextpos)
                    g.supprimer(proies_objgfx[nextpos])
                    proies_age.pop(nextpos)
                    del dobj[proies_objgfx[nextpos]]
                    proies_objgfx.pop(nextpos)
                    carte.pop(nextpos)
                    if pred_nrj[c]+NRJMIAM>NRJMAX:
                        pred_nrj[c] = NRJMAX
                    else:
                        pred_nrj[c] += NRJMIAM
#                     assOgfx(proies_age, proies_objgfx, npred_age, pred_objgfx, pred_nrj, carte, "pos miam")
#                     if pred_nrj[c] >= NRJBIRTH:
#                         i=naissancePred(npred_age, pred_objgfx, pred_nrj, carte)
#                         assOgfx(proies_age, proies_objgfx, npred_age, pred_objgfx, pred_nrj, carte,"post naissance pred")
#                         print("BIRTHPRED!!",i)
            
#                 assert(len(proies_age)==len(proies_objgfx)), print("fail2")
#                 assOgfx(proies_age, proies_objgfx, npred_age, pred_objgfx, pred_nrj, carte,"av depl pred")
                g.deplacer(pred_objgfx[c],move[0]*SIZECASE,move[1]*SIZECASE)
                pred_objgfx[nextpos] = pred_objgfx[c]
                pred_objgfx.pop(c)
                pred_nrj[nextpos] = pred_nrj[c]
                pred_nrj.pop(c)
                carte[nextpos] = carte[c]
                carte.pop(c)
                npred_age[nextpos] = pred_age[c]
                npred_age.pop(c)
#                 assOgfx(proies_age, proies_objgfx, npred_age, pred_objgfx, pred_nrj, carte,"ap depl pred")

                if eat and pred_nrj[nextpos] >= NRJBIRTH:
                    i=naissancePred(npred_age, pred_objgfx, pred_nrj, carte)
#                     assOgfx(proies_age, proies_objgfx, npred_age, pred_objgfx, pred_nrj, carte,"post naissance pred")
#                     print("BIRTHPRED!!",i)
#     print(f"PRED MILIEU {len(npred_age)} {len(pred_objgfx)} {len(pred_nrj)}")
#     print(f"PROIES MILIEU {len(proies_age)} {len(proies_objgfx)}")
#     print(f"CARTE MILIEU {len(carte)}")
#     print("npred_age:",npred_age.keys())
#     print("proies_age:",proies_age.keys())
#     print("carte:",carte.keys())
#     print(f"proies_age entrée: {proies_age}")
    nproies_age = dict(proies_age)
    for c in proies_age:
#         print(f"PROIES allons-y pour {c}")
#         assOgfx(nproies_age, proies_objgfx, npred_age, pred_objgfx, pred_nrj, carte,"deb tour proies")
        proies_age[c] = proies_age[c]-1 # on diminue l'âge
        if proies_age[c] == 0: # si dead
#             print("DEAD!!",c)
            g.supprimer(proies_objgfx[c])
            nproies_age.pop(c)
            del dobj[proies_objgfx[c]]
            proies_objgfx.pop(c)
            carte.pop(c)
#             assOgfx(nproies_age, proies_objgfx, npred_age, pred_objgfx, pred_nrj, carte,"ap mort proies")
        else:
#             print("not dead")
#             assOgfx(nproies_age, proies_objgfx, npred_age, pred_objgfx, pred_nrj, carte,"av voisinage")
            move,repro = voisinage(c, carte, nproies_age, npred_age)
#             assOgfx(nproies_age, proies_objgfx, npred_age, pred_objgfx, pred_nrj, carte,"ap voisinage")
            if repro:
#                 print("NAISSANCE!",plusTuple(repro,c))
                naissanceProie(plusTuple(c,repro), nproies_age, proies_objgfx, carte,npred_age)
#                 assOgfx(nproies_age, proies_objgfx, npred_age, pred_objgfx, pred_nrj, carte,"ap naiss proies")
#                 input()
            if move:
#                 print(f"PROIE {c} bouge de {move}: {plusTuple(c,move)}")
                nextpos = plusTuple(move,c)
                g.deplacer(proies_objgfx[c],move[0]*SIZECASE,move[1]*SIZECASE)
                proies_objgfx[nextpos] = proies_objgfx[c]
                proies_objgfx.pop(c)
                try:
                    carte[nextpos] = carte[c]
                except KeyError:
                    print("carte:",carte.keys())
                    #print(f"nextpos:{nextpos}, c:{c}")
                    input()
                carte.pop(c)
                nproies_age[nextpos] = proies_age[c]
                nproies_age.pop(c)
#     print(f"PRED APRES {len(npred_age)} {len(pred_objgfx)} {len(pred_nrj)}")
#     print(f"PROIES APRES {len(nproies_age)} {len(proies_objgfx)}")
#     print(f"CARTE APRES {len(carte)}")
        
    g.update()
    return npred_age, nproies_age


################################################################################
# MAIN #########################################################################
################################################################################
# ouverture de fenêtre
g = ouvrirFenetre(SIZECASE*NBCASES,SIZECASE*NBCASES)
# dessinerTerrain()
g.update()

proies_age = {} # dico des âges de proies
proies_objgfx = {} # dico des objets graphiques liés aux proies
proies_eff = [] # effectifs des proies
pred_age = {} # dico des âges de prédateurs
pred_nrj = {} # dico des énergies de prédateurs
pred_objgfx = {} # dico des objets graphiques liés aux prédateurs
pred_eff = [] # effectifs des prédateurs
carte = {} # dico des objets graphiques des cases
dobj = {}

tour = 0
# maxtours = int(input("Combien de tours? "))
maxtours = TOURS
naissanceProie(NBPROIES_START, proies_age, proies_objgfx, carte,pred_age)
while tour<maxtours:
#     print("Tour ",tour)
# NAISSANCE PROIE
    naissanceProie(FBIRTHPROIE, proies_age, proies_objgfx, carte,pred_age)
    g.update()
    if tour<NBPRED_START:
        naissancePred(pred_age, pred_objgfx, pred_nrj, carte)
        g.update()
    tour += 1

    pred_age, proies_age = life(pred_age, pred_objgfx, pred_nrj, proies_age, proies_objgfx, carte)
    g.pause(.1)
    proies_eff.append(len(proies_age))
    pred_eff.append(len(pred_age))
        
pyplt.plot(range(maxtours), proies_eff, color="green")
pyplt.plot(range(maxtours), pred_eff, color="red")
pyplt.show()
# fermeture fenêtre
input("fermer-fenetre - presser ENTREE")
g.fermer_fenetre()
