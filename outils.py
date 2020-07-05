# coding: utf-8

# ------------------------------------- IMPORTS --------------------------------------
import pygame.gfxdraw
from pygame.locals import FULLSCREEN
import math
import random
from os import listdir
from commun import *
from operator import itemgetter, attrgetter
import copy

LARGEUR = 1360
HAUTEUR = 700

pygame.init()
f = open("FullScreen.txt", "r")
if f.read().upper() == 'OUI':
    SCREEN = pygame.display.set_mode((LARGEUR, HAUTEUR), FULLSCREEN)
else:
    SCREEN = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("COINCHE")

FPS = 100

f = open("AdresseIP.txt", "r")
ADRESSE_IP = f.read()

IMAGE_FOND = pygame.image.load('Image/Fond.png')
IMAGE_PANNEAU_JOUEUR = pygame.image.load('Image/PanneauJoueur.png')
IMAGE_PANNEAU_JOUEUR_SELECTIONNE = pygame.image.load('Image/PanneauJoueurSelectionne.png')
LARGEUR_IMAGE_PANNEAU_JOUEUR = IMAGE_PANNEAU_JOUEUR.get_width()
HAUTEUR_IMAGE_PANNEAU_JOUEUR = IMAGE_PANNEAU_JOUEUR.get_height()
IMAGE_PANNEAU_SCORE_DROITE = pygame.image.load('Image/PanneauScore.png')
IMAGE_PANNEAU_SCORE_GAUCHE = pygame.transform.flip(IMAGE_PANNEAU_SCORE_DROITE, True, False)
LARGEUR_IMAGE_PANNEAU_SCORE = IMAGE_PANNEAU_SCORE_DROITE.get_width()
HAUTEUR_IMAGE_PANNEAU_SCORE = IMAGE_PANNEAU_SCORE_DROITE.get_height()
IMAGE_JETON_DEALER = pygame.image.load('Image/Dealer.png')
LARGEUR_IMAGE_JETON_DEALER = IMAGE_JETON_DEALER.get_width()
HAUTEUR_IMAGE_JETON_DEALER = IMAGE_JETON_DEALER.get_height()
IMAGE_JOUEUR_TOUR = pygame.image.load('Image/JoueurTour.png')
IMAGE_SAUVEGARE_BOUTON = pygame.image.load('Image/SauvegardeBouton.png')
LARGEUR_IMAGE_BOUTON = IMAGE_SAUVEGARE_BOUTON.get_width()
HAUTEUR_IMAGE_BOUTON = IMAGE_SAUVEGARE_BOUTON.get_height()
X_IMAGE_SAUVEGARE_BOUTON = 8
Y_IMAGE_SAUVEGARE_BOUTON = 8
IMAGE_QUITTER_BOUTON = pygame.image.load('Image/QuitterBouton.png')
X_IMAGE_QUITTER_BOUTON = LARGEUR - 8 - LARGEUR_IMAGE_BOUTON
Y_IMAGE_QUITTER_BOUTON = 8

ENCHERE_CRAN = 5

LISTE_NOMS_CARTES = []
DICTIONNAIRE_IMAGES_CARTES = {}
DICTIONNAIRE_POINTS_CARTE_VALEUR = {1:  {'NA': 11, 'A': 11, 'SA': 19},
                                    10: {'NA': 10, 'A': 10, 'SA': 10},
                                    13: {'NA': 4 , 'A': 4 , 'SA': 4 },
                                    12: {'NA': 3 , 'A': 3 , 'SA': 3 },
                                    11: {'NA': 2 , 'A': 20, 'SA': 2 },
                                    9:  {'NA': 0 , 'A': 14, 'SA': 0 },
                                    8:  {'NA': 0 , 'A': 0 , 'SA': 0 },
                                    7:  {'NA': 0 , 'A': 0 , 'SA': 0 }}

for nompng in listdir('Image/Cartes'):
    nom = nompng[:-4]
    if nom != 'dos-bleu':
        LISTE_NOMS_CARTES.append(nom)
        DICTIONNAIRE_IMAGES_CARTES[nom] = pygame.image.load('Image/Cartes/' + nompng)

IMAGE_CARTE_DOS = pygame.image.load('Image/Cartes/dos-bleu.png')
DICTIONNAIRE_COULEURS = {'pique': 3, 'coeur': 2, 'trefle': 1, 'carreau': 0, 'SA': -1}
PASSE = 'passe'

IMAGES_VIGNETTES = {3: pygame.image.load('Image/pique.png'), 2: pygame.image.load('Image/coeur.png'),
                    1: pygame.image.load('Image/trefle.png'), 0: pygame.image.load('Image/carreau.png'),
                    -1: pygame.image.load('Image/sa.png')}
LARGEUR_VIGNETTE = IMAGES_VIGNETTES[0].get_width()
HAUTEUR_VIGNETTE = IMAGES_VIGNETTES[0].get_height()

ETAT_PARTIE_MISE_EN_PLACE = 0
ETAT_PARTIE_PREPARATION = 1
ETAT_PARTIE_ENCHERE = 2
ETAT_PARTIE_JEU = 3


def point_inside_polygon(x, y, poly):
    n = len(poly)
    inside = False
    p1x, p1y = poly[0]
    for i in range(n + 1):
        p2x, p2y = poly[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside