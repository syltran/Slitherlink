# Sylvain TRAN et Hakim AOUDIA
# TP a-b
import fltk
from time import time


# Tâche 1: Structures de données
# --Chargement de la grille--

def representation_grille(nomfile, i=0):
    """Permet de charger la grille à partir d'un fichier texte
    :param nonfile: fichier texte/ format .txt

    >>> representation_grille("grille0.txt", i=0)
    [['2', '2'], ['2', '2']]
    """
    file = open(nomfile, "r")

    liste = []
    for line in file:
        # print(line.strip())
        liste.append([])

        # .strip() pour suprim les retours à la ligne
        for caractere in line.strip():
            if caractere == "_":
                liste[i].append(None)
            else:
                liste[i].append(caractere)

        i += 1
    return liste


def verif_grille(indices):
    """
    Renvoie True si indices est valide, False sinon
    """

    if verif_longueurLignes(indices) is False:
        print("les lignes ne font pas toutes la même longueur")
        return False

    if verif_caractInvalide(indices) is False:
        print("il y a un ou des caractères invalides")
        print("les seuls caractères autorisés sont '_', '0', '1', '2' ou '3'")
        return False

    if verif_grilleVide(indices) is False:
        print('Votre grille est vide')
        return False

    return True


def verif_longueurLignes(indices):
    """
    Renvoie False si indices contient des lignes
    qui ne font pas toutes la même longueur, True sinon

    >>> verif_longueurLignes([['2', '2', '2'], ['2', '2']])
    False
    """
    for i in range(len(indices)-1):
        if len(indices[i]) != len(indices[i+1]):
            return False
    return True


def verif_caractInvalide(indices):
    """
    Renvoie False si on trouve un caractère invalide dans indices, True sinon

    >>> verif_caractInvalide([['2', '$'], ['#', '2']])
    False
    """
    for i in range(len(indices)):
        for j in range(len(indices[i])):
            if indices[i][j] not in ["0", "1", "2", "3", None]:
                return False
    return True


def verif_grilleVide(indices):
    """Renvoie False si indices contient que des None ou des 0, True sinon

    >>> verif_grilleVide([[None, '0'], ['0', None]])
    False
    >>> verif_grilleVide([[None, None], [None, None]])
    False
    """
    for i in range(len(indices)):
        for j in range(len(indices[i])):
            if indices[i][j] in ["1", "2", "3"]:
                return True
    return False


def est_trace(etat, segment):
    """
    Renvoyant True si segment est tracé dans etat, et False sinon

    >>> etat = {((0, 1), (1, 1)) : -1, ((1, 1), (2, 1)) : 1}
    >>> segment = ((1, 1), (2, 1))
    >>> est_trace(etat, segment)
    True
    """
    if segment in etat and etat[segment] == 1:
        return True
    return False


def est_interdit(etat, segment):
    """
    Renvoyant True si segment est interdit dans etat, et False sinon

    >>> etat = {((0, 1), (1, 1)) : -1, ((1, 1), (2, 1)) : 1}
    >>> segment = ((0, 1), (1, 1))
    >>> est_interdit(etat, segment)
    True
    """
    if segment in etat and etat[segment] == -1:
        return True
    return False


def est_vierge(etat, segment):
    """
    Renvoyant True si segment est vierge dans etat, et False sinon
    >>> etat = {((0, 1), (1, 1)) : -1, ((1, 1), (2, 1)) : 1}
    >>> segment = ((2, 1), (3, 1))
    >>> est_vierge(etat, segment)
    True
    """
    if segment not in etat:
        return True
    return False


def tracer_segment(etat, segment):
    """
    Modifiant etat afin de représenter le fait que segment est maintenant tracé
    """
    etat[segment] = 1


def interdire_segment(etat, segment):
    """
    Modifiant etat afin de représenter le fait
    que segment est maintenant interdit
    """
    etat[segment] = -1


def effacer_segment(etat, segment):
    """
    Modifiant etat afin de représenter le fait
    que segment est maintenant vierge
    """
    del etat[segment]


def segments_traces(etat, sommet):
    """
    Renvoyant la liste des segments tracés adjacents à sommet dans etat

    >>> etat = {((2, 4), (2, 5)) : -1, ((2, 3), (2, 4)) :1, \
                ((2, 4), (3, 4)) : 1}
    >>> sommet = (2, 4)
    >>> segments_traces(etat, sommet)
    [((2, 3), (2, 4)), ((2, 4), (3, 4))]
    """
    segment_adj = []
    for seg in etat:
        if etat[seg] == 1:
            if sommet in seg:
                segment_adj.append(seg)
    return segment_adj


def segments_interdits(etat, sommet):
    """
    Renvoyant la liste des segments interdits adjacents à sommet dans etat

    >>> etat = {((1, 4), (2, 4)) : -1, \
                ((2, 4), (2, 5)) : -1, ((2, 3), (2, 4)) : 1}
    >>> sommet = (2, 4)
    >>> segments_interdits(etat, sommet)
    [((1, 4), (2, 4)), ((2, 4), (2, 5))]
    """
    segment_adj = []
    for seg in etat:
        if etat[seg] == -1:
            if sommet in seg:
                segment_adj.append(seg)
    return segment_adj


def segments_vierges(etat, sommet):
    """
    Renvoyant la liste des segments vierges adjacents à sommet dans etat

    >>> etat = {((2, 4), (2, 5)) : -1, ((2, 3), (2, 4)) : 1}
    >>> sommet = (2, 4)
    >>> segments_vierges(etat, sommet)
    [((1, 4), (2, 4)), ((2, 4), (3, 4))]
    """
    segment_adj = []
    segTraces = segments_traces(etat, sommet)
    segInterdits = segments_interdits(etat, sommet)

    i, j = sommet
    lst = [((i, j-1), (i, j)), ((i-1, j), (i, j)),
           ((i, j), (i, j+1)), ((i, j), (i+1, j))]
    for seg in lst:
        if seg not in segTraces:
            if seg not in segInterdits:
                segment_adj.append(seg)  # seg est forcement vierge
    return segment_adj


def statut_case(indices, etat, case):
    """
    Recevant le tableau d’indices, l’état de la grille et
    les coordonnées d’une case (pas d’un sommet !)
    et renvoyant None si cette case ne porte aucun indice,
    et un nombre entier sinon :
        – 0 si l’indice est satisfait ;
        – positif s’il est encore possible de satisfaire
        l’indice en traçant des segments autour de la case ;
        – négatif s’il n’est plus possible de satisfaire
        l’indice parce que trop de segments sont
        déjà tracés ou interdits autour de la case.

    >>> indices = [['2', '2'], ['2', '2']]
    >>> etat = {((0, 0), (0, 1)): 1, ((0, 0), (1, 0)): 1, ((0, 1), (0, 2)): 1}
    >>> statut_case(indices, etat, (0, 0))
    0

    >>> statut_case(indices, etat, (0, 1))
    1

    >>> etat = {((0, 0), (0, 1)): 1, ((0, 0), (1, 0)): 1, ((1, 0), (1, 1)): 1}
    >>> statut_case(indices, etat, (0, 0))
    -1
    """
    i, j = case

    if indices[i][j] is None:
        return None

    segTraces = []
    segInterdits = []
    lst = [((i, j), (i+1, j)), ((i, j), (i, j+1)),
           ((i, j+1), (i+1, j+1)), ((i+1, j), (i+1, j+1))]
    for seg in lst:
        if est_trace(etat, seg) is True:  # si seg est tracé dans etat
            segTraces.append(seg)
        elif est_interdit(etat, seg) is True:  # si seg est interdit dans etat
            segInterdits.append(seg)

    if int(indices[i][j]) == len(segTraces):
        return 0
    elif int(indices[i][j]) + len(segInterdits) <= 4\
            and int(indices[i][j]) > len(segTraces):
        return 1
    elif int(indices[i][j]) < len(segTraces):
        return -1
    elif int(indices[i][j]) < len(segInterdits):
        return -1


# Tâche 2 : conditions de victoire


def indices_satisfait(indices, etat):
    """
    Vérifie si chaque indice est satisfait :
    chaque case contenant un indice k compris entre 0 et 3 doit avoir
    exactement k côtés tracés. Renvoie True si c'est le cas, False sinon

    >>> indices = [['2', '2'], ['2', '2']]
    >>> etat = {((0, 0), (0, 1)): 1, ((0, 1), (0, 2)): 1, \
                ((0, 2), (1, 2)): 1, ((1, 2), (2, 2)): 1, \
                ((2, 1), (2, 2)): 1, ((2, 0), (2, 1)): 1, \
                ((1, 0), (2, 0)): 1, ((0, 0), (1, 0)): 1}
    >>> indices_satisfait(indices, etat)
    True

    >>> indices_satisfait(indices, {((0, 0), (0, 1)): 1, ((0, 0), (1, 0)): 1})
    False
    """
    for i in range(len(indices)):
        for j in range(len(indices[i])):

            if indices[i][j] in ind:  # si la case à l'indice 0, 1, 2 ou 3
                if statut_case(indices, etat, (i, j)) != 0:
                    # si on a un indice qui n'est pas
                    # satisfait on renvoie False
                    return False
    return True


def longueur_boucle(etat, segment, nb_segments=1):
    """
    Vérifie que l’ensemble des segments tracés forme une unique boucle fermée.
    :param segment : segment tracé dans etat quelconque

    >>> etat = {((0, 0), (0, 1)): 1, ((0, 1), (0, 2)): 1, \
                ((0, 2), (1, 2)): 1, ((1, 2), (2, 2)): 1, \
                ((2, 1), (2, 2)): 1, ((2, 0), (2, 1)): 1, \
                ((1, 0), (2, 0)): 1, ((0, 0), (1, 0)): 1}
    >>> segment = ((0, 0), (0, 1))
    >>> longueur_boucle(etat, segment)
    8
    """
    # etape 1, 2
    depart = segment[0]
    precedent = segment[0]
    courant = segment[1]

    # etape 2bis
    if len(segments_traces(etat, depart)) != 2:
        return None

    # etape 3
    while courant != depart:
        # etape a
        segment_adj = segments_traces(etat, courant)
        # etape b
        if len(segment_adj) != 2:
            return None
        else:
            # print("courant = ", courant, "precedent = ", precedent)
            # print(segment_adj)
            # etape c
            for seg in segment_adj:
                for sommet in seg:
                    if sommet != courant and sommet != precedent:
                        newSommet = sommet
            # etape d
            precedent = courant
            courant = newSommet

            nb_segments += 1  # compte segments parcouru
    # etape 4
    return nb_segments


def Total_segTrace(etat):
    """
    Compte le nombre total de segments tracés dans etat

    >>> etat = {((2, 4), (2, 5)) : -1, \
                ((2, 3), (2, 4)) : 1, ((2, 4), (3, 4)) : 1}
    >>> Total_segTrace(etat)
    2
    """
    cmpt = 0
    for seg in etat:
        if est_trace(etat, seg) is True:
            cmpt += 1
    return cmpt


def segTrace_quelconque(etat):
    """
    Renvoie un segment tracé quelconque dans etat

    >>> etat = {((2, 4), (2, 5)) : -1, ((2, 3), (2, 4)) : 1, \
                ((2, 4), (3, 4)) : 1}
    >>> segTrace_quelconque(etat)
    ((2, 3), (2, 4))
    """
    for seg in etat:
        if est_trace(etat, seg) is True:
            return seg


# Tâche 3: Interface graphique


def dessine_rond(indices, marge, taille, color):
    """
    Dessine les sommets de la grille
    """
    for i in range(len(indices)+1):
        for j in range(len(indices[0])+1):
            fltk.cercle(marge + j * taille, marge + i * taille,
                        3, remplissage=color, tag="Ronds")


def colorer_indice(indices, etat):
    """
    Dessine et colorie les indices selon le nombre de
    segments tracés les entourant :
    - en bleu, s’il y a exactement le bon nombre de segments
    - en noir, s’il n’y en a pas encore assez
    - en rouge, s’il y en a trop
    """
    for i in range(len(indices)):
        for j in range(len(indices[i])):
            if indices[i][j] in ind:  # si la case à l'indice 0, 1, 2 ou 3
                statut = statut_case(indices, etat, (i, j))

                if statut == 0:  # nbre de segments tracés satisfait
                    color = "lightblue"
                elif statut == 1:  # il n'y en a pas assez
                    color = "black"
                else:  # il y en a trop
                    color = "red"

                fltk.texte(Marge + taille_case * j + taille_case/2,
                           Marge + taille_case * i + taille_case/2,
                           indices[i][j], couleur=color,
                           ancrage="center", tag='Indices')


def detection_segment(x, y):
    """
    Gère la detection des clics sur les segments.
    Si un clic tombent à proximité d’un segment, on renvoie ses coordonnées.
    Sinon, on renvoie None

    >>> detection_segment(54, 55)

    >>> detection_segment(56, 21)
    ((0, 0), (0, 1))
    """
    newX = (x - Marge) / taille_case
    newY = (y - Marge) / taille_case
    # print(newX, newY)

    # segment vertical
    if -0.1 + round(newX) < newX < 0.1 + round(newX):
        if int(newY) + 0.1 < newY < int(newY) + 1 - 0.1:
            # print("i =", int(newY), "j =", round(newX))

            segment = ((int(newY), round(newX)), (int(newY) + 1, round(newX)))
            return segment

    # segment horizontal
    if -0.1 + round(newY) < newY < 0.1 + round(newY):
        if int(newX) + 0.1 < newX < int(newX) + 1 - 0.1:
            # print("i =", round(newY), "j =", int(newX))

            segment = ((round(newY), int(newX)), (round(newY), int(newX) + 1))
            return segment

    return None


def clic(ty, ev):
    """
    Gère les clics du joueur :
    - Un clic Gauche aura pour effet de tracer un segment
    - Un clic Droit aura pour effet de marquer un segment comme interdit
    N'importe quel clic sur un segment déjà tracé ou interdit
    aura pour effet d’effacer la déduction.
    """
    if ty == 'ClicGauche':  # Traces
        x, y = fltk. abscisse(ev), fltk.ordonnee(ev)
        seg = detection_segment(x, y)

        if seg is not None:
            if seg not in etat:
                tracer_segment(etat, seg)
            else:
                effacer_segment(etat, seg)

            scoreCoups[0] += 1
            # print(etat)

    elif ty == 'ClicDroit':  # Interdits
        x, y = fltk.abscisse(ev), fltk.ordonnee(ev)
        seg = detection_segment(x, y)

        if seg is not None:
            if seg not in etat:
                interdire_segment(etat, seg)
            else:
                effacer_segment(etat, seg)

            scoreCoups[0] += 1
            # print(etat)


def dessine_segmentTrace(etat):
    """
    Dessine les segments tracés
    """
    for seg in etat:
        if etat[seg] == 1:
            S1, S2 = seg
            fltk.ligne(Marge + S1[1] * taille_case,
                       Marge + S1[0] * taille_case,
                       Marge + S2[1] * taille_case,
                       Marge + S2[0] * taille_case,
                       epaisseur=3, tag='Trace')


def dessine_segmentInterdit(etat):
    """Dessine les segments interdits
    """
    for seg in etat:
        if etat[seg] == -1:
            S1, S2 = seg
            x = (Marge + S1[1] * taille_case + Marge + S2[1] * taille_case)/2
            y = (Marge + S1[0] * taille_case + Marge + S2[0] * taille_case)/2

            fltk.image(x, y, 'croix.png', tag='Interdit')


# ----Menu Jeu----

def menu_debutJeu(xFleche, yFleche):
    """
    Gère le menu de début de jeu :
    Le jouer aura le choix entre :
    - Jouer, lui permettant de jouer au jeu
    - Quitter, lui permettant de quitter le jeu
    """
    poseFleche = 0
    while True:
        fltk.efface("fleche")
        fltk.image(250, 250, "fondmenu.png")
        fltk.image(xFleche, yFleche, "fleche.png", tag='fleche')
        # texte(250, 25, "SLITHERLINK", ancrage="center")
        fltk.texte(370, 350, "Jouer", ancrage="center")
        fltk.texte(370, 400, "Quitter", ancrage="center")

        fltk.mise_a_jour()

        ev = fltk.donne_ev()
        ty = fltk.type_ev(ev)
        if ty == "Touche":
            if fltk.touche(ev) == "Up":
                if poseFleche > 0:
                    yFleche -= 50
                    poseFleche -= 1

            elif fltk.touche(ev) == "Down":
                if poseFleche < 1:
                    yFleche += 50
                    poseFleche += 1

            elif fltk.touche(ev) == 'Return':  # Entrée
                fltk.efface_tout()
                if poseFleche == 0:  # Jouer
                    return True
                return False  # Quitter


def menu_choixGrille(xFleche, yFleche, listeGrille, NomGrille):
    """
    Gère le menu des grilles permettant au joueur
    de choisir une grille de son choix parmi un ensemble de grilles
    """
    poseFleche = 0
    while True:
        fltk.efface("fleche")
        fltk.efface("Ronds")
        fltk.efface("IndicesMenu")
        fltk.image(250, 250, "touches.png")
        fltk.image(xFleche, yFleche, "fleche.png", tag='fleche')

        nomfile = listeGrille[poseFleche]
        indices = representation_grille(nomfile)
        dessine_rond(indices, MargeMenu, taille_caseMenu, "gray")
        dessine_indiceMenu(indices)

        for i in range(len(NomGrille)):
            fltk.texte(420, 200 + (i*50), NomGrille[i], ancrage="ne")

        fltk.mise_a_jour()

        ev = fltk.donne_ev()
        ty = fltk.type_ev(ev)
        if ty == "Touche":
            if fltk.touche(ev) == "Up":
                if poseFleche > 0:
                    yFleche -= 50
                    poseFleche -= 1

            elif fltk.touche(ev) == "Down":
                if poseFleche < (len(listeGrille) - 1):
                    yFleche += 50
                    poseFleche += 1

            elif fltk.touche(ev) == 'Return':  # Entrée
                fltk.efface_tout()
                return listeGrille[poseFleche]


def menu_finJeu(xFleche, yFleche):
    """
    Gère le menu de fin de jeu.
    Le joueur aura le choix entre :
    - Rejouer, lui permettant de rejouer sur la même grille
    - Charger une autre grille, lui permettant de charger
    et joueur sur une autre grille
    - Quitter, lui permettant de quitter le jeu
    """
    poseFleche = 0
    while True:
        fltk.efface("fleche")
        fltk.image(xFleche, yFleche, "fleche.png", tag='fleche')
        fltk.texte(370, 350, "Rejouer", ancrage="center")
        fltk.texte(250, 400, "Charger une autre Grille", ancrage="center")
        fltk.texte(370, 450, "Quitter", ancrage="center")

        fltk.mise_a_jour()

        ev = fltk.donne_ev()
        ty = fltk.type_ev(ev)
        if ty == "Touche":
            if fltk.touche(ev) == "Up":
                if poseFleche > 0:
                    yFleche -= 50
                    poseFleche -= 1

            elif fltk.touche(ev) == "Down":
                if poseFleche < 2:
                    yFleche += 50
                    poseFleche += 1

            elif fltk.touche(ev) == 'Return':  # Entrée
                fltk.efface_tout()
                return poseFleche


def dessine_indiceMenu(indices):
    """
    Dessine les indices des grilles dans le Menu de choix des grilles
    """
    for i in range(len(indices)):
        for j in range(len(indices[i])):
            if indices[i][j] in ind:
                fltk.texte(MargeMenu + taille_caseMenu * j + taille_caseMenu/2,
                           MargeMenu + taille_caseMenu * i + taille_caseMenu/2,
                           indices[i][j], couleur="red", ancrage="center",
                           tag='IndicesMenu')


# Tâche 4: Recherche de solutions


def algo_backtracking(indices, etat, sommet):
    """
    L'algorithme qui permet de déterminer s’il est possible
    de résoudre la grille.
    Si c'est le cas, on renvoie True et la solution est représentée dans etat
    (et donc il ne reste plus qu'à dessiner la grille résolue),
    sinon on renvoie False

    >>> indices = [['2', '2'], ['2', '2']]
    >>> algo_backtracking(indices, {}, (0, 0))
    True
    >>> algo_backtracking(indices, {}, (1, 1))
    False
    """
    if len(segments_traces(etat, sommet)) == 2:
        if indices_satisfait(indices, etat) is True:
            return True

    elif len(segments_traces(etat, sommet)) > 2:
        return False

    else:
        i, j = sommet
        prec = sommet

        segs_adjs = [((i, j-1), (i, j)), ((i-1, j), (i, j)),
                     ((i, j), (i, j+1)), ((i, j), (i+1, j))]
        # On récupère les cases qui pourront être
        # impactées par un seg tracé à partir de sommet
        casesPossibles = [(i-1, j-1), (i-1, j), (i, j-1), (i, j)]

        for seg in segs_adjs:
            if verif_SegdansGrille(indices, seg) is True:
                # si le seg n'est pas déjà tracé dans état
                if est_trace(etat, seg) is False:
                    tracer_segment(etat, seg)

                    # mode Graphique
                    ev = fltk.donne_ev()
                    ty = fltk.type_ev(ev)
                    ModeGraphique(ty, ev)
                    SpeedAffichage(ty, ev)

                    if SGraph[-1] == "g":
                        fltk.attente(Speedaff[0])
                        fltk.efface('Trace')
                        fltk.efface('Indices')
                        dessine_segmentTrace(etat)
                        colorer_indice(indices, etat)
                        fltk.mise_a_jour()

                    if verif_IndicesExces(indices, etat, casesPossibles, seg)\
                       is True:
                        for sommet in seg:
                            if sommet != prec:
                                if algo_backtracking(indices, etat, sommet)\
                                   is True:
                                    return True
                                else:
                                    effacer_segment(etat, seg)
                    else:
                        effacer_segment(etat, seg)
    return False


def ModeGraphique(ty, ev):
    """
    Activer ou désactiver le mode Graphique du Solveur
    """
    if ty == "Touche":
        if fltk.touche(ev) == "g":
            SGraph.append("g")
            print('Mode solveur graphique activé')

        if fltk.touche(ev) == "d":
            SGraph.append("d")
            print('Mode solveur graphique désactivé')


def SpeedAffichage(ty, ev):
    """
    Gère la vitesse d'affichage du mode Graphique
    """
    if ty == "Touche":
        if fltk.touche(ev) == "a":
            Speedaff[0] += 0.5
            print("Vitesse d'affichage :", Speedaff[0], "s")

        if fltk.touche(ev) == "z" and Speedaff[0] > 0:
            Speedaff[0] -= 0.5
            print("Vitesse d'affichage :", Speedaff[0], "s")


def verif_SegdansGrille(indices, segment):
    """
    Vérifie si le segment est bien dans la grille.
    On renvoie True si c'est le cas, False sinon

    >>> indices = [['2', '2'], ['2', '2']]
    >>> verif_SegdansGrille(indices , ((0, 0), (0, 1)))
    True
    >>> verif_SegdansGrille(indices , ((0, -1), (0, 0)))
    False
    """
    sommet1, sommet2 = segment
    if 0 <= sommet1[0] < len(indices)+1\
       and 0 <= sommet1[1] < len(indices[0])+1:

        if 0 <= sommet2[0] < len(indices)+1\
           and 0 <= sommet2[1] < len(indices[0])+1:
            return True
    return False


def verif_IndicesExces(indices, etat, cases, segment):
    """
    Sert à vérifier si le segment tracé ne va pas faire dépasser
    le nombre de segments autorisés par les cases voisines.
    Si c'est le cas on renvoie False, sinon True

    >>> indices = [['3', '1'], ['3', None]]
    >>> etat = {((0, 0), (0, 1)): 1, ((0, 1), (0, 2)): 1, ((0, 2), (1, 2)): 1}
    >>> cases = [(-1, 1), (-1, 2), (0, 1), (0, 2)]
    >>> segment = ((0, 2), (1, 2))
    >>> verif_IndicesExces(indices, etat, cases, segment)
    False
    """
    for case in cases:
        i, j = case
        if verif_CasedansGrille(indices, i, j) is True:
            segsPossibles = [((i, j), (i+1, j)), ((i, j), (i, j+1)),
                             ((i, j+1), (i+1, j+1)), ((i+1, j), (i+1, j+1))]

            if segment in segsPossibles:
                if statut_case(indices, etat, (i, j)) == -1:
                    return False
    return True


def verif_CasedansGrille(indices, i, j):
    """
    Vérifie si la case (i, j) est bien dans la grille.
    On renvoie True si c'est le cas, False sinon

    >>> indices = [['2', '2'], ['2', '2']]
    >>> verif_CasedansGrille(indices, 1, 1)
    True
    >>> verif_CasedansGrille(indices, 0, 2)
    False
    """
    if 0 <= i < len(indices):
        if 0 <= j < len(indices[0]):
            return True
    return False


def Solveur(indices):
    """
    Renvoie True si la grille a été résolue.
    Vu que la solution de la grille ne passe pas forcément par un sommet
    en particulier, on va lancer la recherche à partir d'un sommet qui sera
    forcément un bon point de départ. Si une solution à été trouvé à partir
    de ce sommet, alors on renvoie True. Sinon, False

    >>> Solveur([['2', '2'], ['2', '2']])
    True
    >>> Solveur([['2', '2'], ['2', '1']])
    False
    """
    for i in range(len(indices)):
        for j in range(len(indices[i])):
            if indices[i][j] in ["3", "2", "1"]:

                if algo_backtracking(indices, etat, (i, j)) is True:
                    return True

                elif algo_backtracking(indices, etat, (i+1, j+1)) is True:
                    return True
    return False


def dessine_Grille(largeur, hauteur):
    """
    Dessine la grille et les sommets du jeu
    """
    fltk.ferme_fenetre()
    fltk.cree_fenetre(largeur, hauteur)
    dessine_rond(indices, Marge, taille_case, "black")


SGraph = ["d"]  # par défaut "d" pour mode Graphique désactivé
Speedaff = [0]  # par défaut vitesse à 0s


# ----Implémentation du jeu et Initialisation----


listeGrille = ["grille-vide.txt", "grille0.txt", "grille1.txt",
               "grille2.txt", "grille3.txt", "grille4.txt"]
NomGrille = ["grille-vide", "grille0", "grille1",
             "grille2", "grille3", "grille4"]
ind = ["0", "1", "2", "3"]
etat = {}

taille_caseMenu = 30
MargeMenu = 50
taille_case = 80
Marge = 15


fltk.cree_fenetre(500, 500)

if menu_debutJeu(450, 350) is True:  # Jouer
    nomfile = menu_choixGrille(450, 220, listeGrille, NomGrille)
    indices = representation_grille(nomfile)
    # print(indices)

    if verif_grille(indices) is False:
        quit()

else:  # Quitter
    quit()

largeurEcran = Marge*2 + taille_case * len(indices[0])
hauteurEcran = Marge*2 + taille_case * len(indices)
dessine_Grille(largeurEcran, hauteurEcran)


scoreCoups = [0]
tmpsdebut = int(time())  # on récupère le tmps au début


# Boucle Principale
while True:
    fltk.efface('Trace')
    fltk.efface('Interdit')
    fltk.efface("Indices")
    dessine_segmentTrace(etat)
    dessine_segmentInterdit(etat)
    colorer_indice(indices, etat)

    fltk.mise_a_jour()

    # Conditions mettant fin au jeu
    if indices_satisfait(indices, etat) is True:
        seg = segTrace_quelconque(etat)
        nbreSegParcouru = longueur_boucle(etat, seg)

        if nbreSegParcouru is not None:
            if nbreSegParcouru == nb_total:

                fltk.texte(largeurEcran/2, hauteurEcran/2, "Félicitation",
                           couleur="red", ancrage="center")

                score = str(scoreCoups[0])
                temps = str(int(time()) - tmpsdebut)
                fltk.texte(largeurEcran/2, hauteurEcran/2+35,
                           "Score: " + score + " coups",
                           couleur="red", taille=18, ancrage="center")
                fltk.texte(largeurEcran/2, hauteurEcran/2+65,
                           "Temps: " + temps + "s",
                           couleur="red", taille=18, ancrage="center")

                fileScore = open("scores.txt", "a", encoding="utf-8")
                fileScore.write("\nLa grille '" + nomfile
                                + "' a été réalisé en " + temps
                                + " secondes avec un score de " + score)

                fltk.attend_clic_gauche()
                fltk.ferme_fenetre()  # on ferme

                # on affiche une nouvelle fenetre
                # pour afficher le menu de fin de jeu
                fltk.cree_fenetre(500, 500)

                choix = menu_finJeu(450, 350)
                if choix == 0:  # Recommencer
                    etat = {}

                    dessine_Grille(largeurEcran, hauteurEcran)

                    scoreCoups[0] = 0  # on réinitialise le nombre de coups
                    tmpsdebut = int(time())  # on récupère le tmps au début

                elif choix == 1:  # Charger autre Grille
                    etat = {}

                    nomfile = menu_choixGrille(450, 220,
                                               listeGrille, NomGrille)
                    indices = representation_grille(nomfile)

                    if verif_grille(indices) is False:
                        quit()

                    largeurEcran = Marge*2 + taille_case * len(indices[0])
                    hauteurEcran = Marge*2 + taille_case * len(indices)
                    dessine_Grille(largeurEcran, hauteurEcran)

                    scoreCoups[0] = 0  # on réinitialise le nombre de coups
                    tmpsdebut = int(time())  # on récupère le tmps au début

                else:  # Quitter
                    quit()

    ev = fltk.donne_ev()
    ty = fltk.type_ev(ev)
    clic(ty, ev)
    ModeGraphique(ty, ev)

    if ty == "Touche":
        if fltk.touche(ev) == "p":  # Solveur
            etat = {}
            if Solveur(indices) is False:
                print("Il n'y a pas de solutions")
                quit()

    nb_total = Total_segTrace(etat)
    # print(nb_total)
