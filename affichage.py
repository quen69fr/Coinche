# coding: utf-8

from outils import *

# Couleurs et polices:
POLICE_NONE = 'Font/freesansbold.ttf'
COEF_POLICE = 1

NOIR = (0, 0, 0)
GRIS_FONCE = (50, 50, 50)
GRIS_MOYEN = (90, 90, 90)
GRIS_CLAIR = (190, 190, 190)
BLANC = (255, 255, 255)
BLEU = (0, 0, 255)
VERT = (52, 175, 0)
ROUGE = (255, 0, 0)
ORANGE = (255, 127, 0)
JAUNE = (255, 255, 0)


def affiche_texte(texte, x, y, font=None, taille=30, couleur=NOIR, centrer=False, y_0top_1centre_2bottom=0,
                  x_0left_1centre_2right=0, return_largeur=False, return_hauteur=False):
    if font is None:
        font = POLICE_NONE
    police = pygame.font.Font(font, int(taille))
    surface = police.render(texte, True, couleur)
    if centrer:
        rect = surface.get_rect(center=(x, y))
    elif y_0top_1centre_2bottom == 0:
        if x_0left_1centre_2right == 0:
            rect = surface.get_rect(topleft=(x, y))
        elif x_0left_1centre_2right == 1:
            rect = surface.get_rect(midtop=(x, y))
        else:
            rect = surface.get_rect(topright=(x, y))
    elif y_0top_1centre_2bottom == 1:
        if x_0left_1centre_2right == 0:
            rect = surface.get_rect(midleft=(x, y))
        elif x_0left_1centre_2right == 1:
            rect = surface.get_rect(center=(x, y))
        else:
            rect = surface.get_rect(midright=(x, y))
    else:
        if x_0left_1centre_2right == 0:
            rect = surface.get_rect(bottomleft=(x, y))
        elif x_0left_1centre_2right == 1:
            rect = surface.get_rect(midbottom=(x, y))
        else:
            rect = surface.get_rect(bottomright=(x, y))
    SCREEN.blit(surface, rect)
    if return_largeur and return_hauteur:
        return surface.get_width(), surface.get_height()
    if return_largeur:
        return surface.get_width()
    if return_hauteur:
        return surface.get_height()


def afficheBulleRectanle(x, y, largeur, hauteur, hbdg, tailleFleche=18, largeurBords=3, couleurFond=BLANC, couleurBord=NOIR):
    largeurBords *= 2
    longeurFleche = int(tailleFleche * 0.8)
    tailleFlecheSurDeux = int(tailleFleche / 2)
    largeurSurDeux = largeur / 2
    if hbdg == 'h':
        pygame.draw.polygon(SCREEN, couleurBord, [(x + largeurSurDeux, y - longeurFleche),
                                                  (x + largeurSurDeux + tailleFlecheSurDeux, y),
                                                  (x + largeurSurDeux - tailleFlecheSurDeux, y)])
    elif hbdg == 'b':
        pygame.draw.polygon(SCREEN, couleurBord, [(x + largeurSurDeux, y + hauteur + longeurFleche),
                                                  (x + largeurSurDeux + tailleFlecheSurDeux, y + hauteur),
                                                  (x + largeurSurDeux - tailleFlecheSurDeux, y + hauteur)])
    elif hbdg == 'g':
        pygame.draw.polygon(SCREEN, couleurBord, [(x - longeurFleche, y + hauteur / 2),
                                                  (x, y + hauteur / 2 + tailleFlecheSurDeux),
                                                  (x, y + hauteur / 2 - tailleFlecheSurDeux)])
    elif hbdg == 'd':
        pygame.draw.polygon(SCREEN, couleurBord, [(x + largeur + longeurFleche, y + hauteur / 2),
                                                  (x + largeur, y + hauteur / 2 + tailleFlecheSurDeux),
                                                  (x + largeur, y + hauteur / 2 - tailleFlecheSurDeux)])
    pygame.draw.rect(SCREEN, couleurFond, (x, y, largeur, hauteur))
    pygame.draw.rect(SCREEN, couleurBord, (x, y, largeur, hauteur), 3)
    if hbdg == 'h':
        pygame.draw.polygon(SCREEN, couleurFond, [(x + largeurSurDeux, y - longeurFleche + largeurBords),
                                                  (x + largeurSurDeux + tailleFlecheSurDeux, y + largeurBords),
                                                  (x + largeurSurDeux - tailleFlecheSurDeux, y + largeurBords)])
    elif hbdg == 'b':
        pygame.draw.polygon(SCREEN, couleurFond, [(x + largeurSurDeux, y + hauteur + longeurFleche - largeurBords),
                                                  (x + largeurSurDeux + tailleFlecheSurDeux, y + hauteur - largeurBords),
                                                  (x + largeurSurDeux - tailleFlecheSurDeux, y + hauteur - largeurBords)])
    elif hbdg == 'g':
        pygame.draw.polygon(SCREEN, couleurFond, [(x - longeurFleche + largeurBords, y + hauteur / 2),
                                                  (x + largeurBords, y + hauteur / 2 + tailleFlecheSurDeux),
                                                  (x + largeurBords, y + hauteur / 2 - tailleFlecheSurDeux)])
    elif hbdg == 'd':
        pygame.draw.polygon(SCREEN, couleurFond, [(x + largeur + longeurFleche - largeurBords, y + hauteur / 2),
                                                  (x + largeur - largeurBords, y + hauteur / 2 + tailleFlecheSurDeux),
                                                  (x + largeur - largeurBords, y + hauteur / 2 - tailleFlecheSurDeux)])


class Bouton:
    def __init__(self, x, y, parametre, largeur, hauteur, texte, policeTexte=None, tailleTexte=30,
                 couleurTexte=NOIR, largeurContour=3, couleurRect=GRIS_CLAIR, couleurCountour=GRIS_CLAIR,
                 selectionner=False, couleurTexteSelec=NOIR, couleurRectSelec=GRIS_CLAIR, centrer=False):
        self.x = x
        self.y = y
        self.largeur = largeur
        self.hauteur = hauteur
        if centrer == True:
            self.x -= int(self.largeur / 2)
            self.y -= int(self.hauteur / 2)
        self.parametre = parametre
        self.texte = texte
        self.policeTexte = policeTexte
        self.tailleTexte = tailleTexte
        self.couleurTexte = couleurTexte
        self.largeurContour = largeurContour
        self.couleurRect = couleurRect
        self.couleurCountour = couleurCountour
        self.selectionner = selectionner
        self.couleurRectSelec = couleurRectSelec
        self.couleurTexteSelec = couleurTexteSelec

    def affiche(self):
        cRect = self.couleurRect
        cTexte = self.couleurTexte
        if self.selectionner == True:
            cRect = self.couleurRectSelec
            cTexte = self.couleurTexteSelec
        pygame.draw.rect(SCREEN, cRect, (self.x, self.y, self.largeur, self.hauteur), 0)
        pygame.draw.rect(SCREEN, self.couleurCountour, (self.x, self.y, self.largeur, self.hauteur),
                         self.largeurContour)
        affiche_texte(self.texte, self.x + int(self.largeur / 2), self.y + int(self.hauteur / 2), self.policeTexte,
                      self.tailleTexte, cTexte, True)

    def clic(self, x_souris, y_souris):
        if self.x <= x_souris <= self.x + self.largeur and self.y <= y_souris <= self.y + self.hauteur:
            return True
        return False
