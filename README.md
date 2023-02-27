# Projet Slitherlink

**Auteurs :** Tran Sylvain, Aoudia Hakim

**Date :** 2021 (L1, semestre 2)

**Objectif :**  
Réaliser le jeu Slitherlink en python avec la bibliothèque graphique de l'UGE fltk.

**Principe du jeu :**  
Le jeu se joue sur une grille de points dont les cases formées par ceux-ci sont soit vides soit numérotées entre 0 et 3.
Quand on fait un clic gauche entre deux points, un segment apparaît.  
Le but est de former une seule boucle en satisfaisant toutes les cases numérotées avec des segments.
Chaque case numérotée doit avoir le même nombre de segments adjacents que son chiffre (Ex: Une case 2 doit avoir 2 segments adjacents).

Ici, le joueur peut jouer autant de coups qu'il le souhaite et n'a pas de temps limite pour gagner.  
On a également implémenté un solveur automatique de la grille que le joueur peut activer en cas de difficulté.


**Documentation Technique et Utilisateur :**  
Voir le fichier `rapport.pdf`