# coding: utf-8

from affichage import *
from outils import *


# ==========================================================
class Enchere:
    def __init__(self, valeur, couleur, joueur=None, coinche=0):
        self.valeur = valeur
        self.couleur = couleur
        self.coincher = coinche
        self.joueur = joueur


# ==========================================================
class Vignette:
    def __init__(self, image, x, y, marge_bordure, paramettre):
        self.image = image
        self.x = x
        self.y = y
        self.paramettre = paramettre
        self.largeur = LARGEUR_VIGNETTE + marge_bordure * 2
        self.hauteur = HAUTEUR_VIGNETTE + marge_bordure * 2
        self.marge_bordure = marge_bordure

    def affiche(self):
        pygame.draw.rect(SCREEN, BLANC, (self.x, self.y, self.largeur, self.hauteur))
        pygame.draw.rect(SCREEN, NOIR, (self.x, self.y, self.largeur, self.hauteur), 3)
        SCREEN.blit(self.image, (int(self.x + self.marge_bordure), int(self.y + self.marge_bordure)))

    def clic(self, x_souris, y_souris):
        if self.x <= x_souris <= self.x + self.largeur and self.y <= y_souris <= self.y + self.hauteur:
            return True
        return False


# ==========================================================
class FlechePlusMoins:
    def __init__(self, cx, cy, taille, couleur=GRIS_FONCE):
        self.cx = cx
        self.cy = cy
        self.taille = taille
        self.couleur = couleur
        tailleLargeurSurDeux = self.taille * 0.6
        espaceFlechesSurDeux = self.taille * 0.2
        self.listePoint1 = [(self.cx + tailleLargeurSurDeux, self.cy + espaceFlechesSurDeux),
                            (self.cx - tailleLargeurSurDeux, self.cy + espaceFlechesSurDeux),
                            (self.cx, self.cy + espaceFlechesSurDeux + self.taille)]
        self.listePoint2 = [(self.cx + tailleLargeurSurDeux, self.cy - espaceFlechesSurDeux),
                            (self.cx - tailleLargeurSurDeux, self.cy - espaceFlechesSurDeux),
                            (self.cx, self.cy - espaceFlechesSurDeux - self.taille)]

    def affiche(self):
        pygame.draw.polygon(SCREEN, self.couleur, self.listePoint1)
        pygame.draw.polygon(SCREEN, self.couleur, self.listePoint2)

    def clic(self, x_souris, y_souris):
        if point_inside_polygon(x_souris, y_souris, self.listePoint1):
            return -1
        if point_inside_polygon(x_souris, y_souris, self.listePoint2):
            return 1
        return 0


# ==========================================================
class FenetreEnchere:
    monJoueur = None
    enchere_cran = 5
    valeur_max = 160

    def __init__(self, largeur=550, hauteur=160, x=int(LARGEUR / 2 - 550 / 2), y=int(HAUTEUR / 2 - 160 / 2),
                 coef_largeur_premiere_partie=0.35, margeBordureVignette=10):
        self.x = x
        self.y = y
        self.largeur = largeur
        self.hauteur = hauteur
        self.valeur_min = 80
        self.valeur = 80
        self.monTour = False
        self.ancienneEnchere = None
        self.coinche_possible = False
        self.sur_coinche_possible = False
        self.augmentation_possible = True
        largeur_premiere_partie = coef_largeur_premiere_partie * largeur
        mb = margeBordureVignette
        m = (self.largeur - largeur_premiere_partie - 5 * (LARGEUR_VIGNETTE + 2 * mb)) / 6
        self.vignettes = [Vignette(IMAGES_VIGNETTES[i],
                                   self.x + largeur_premiere_partie + (2 - i) * (LARGEUR_VIGNETTE + 2 * mb + m) + m,
                                   self.y + m, mb, i) for i in range(-2, 4)]
        y2 = self.y + 3 * m + HAUTEUR_VIGNETTE
        self.boutonPasse = Bouton(self.x + m, y2, PASSE, largeur_premiere_partie - m, self.hauteur + self.y - y2 - m,
                                  'Passer')

        l = 6 * mb + 2 * m + 3 * LARGEUR_VIGNETTE
        self.boutonSurCoinche = Bouton(self.x + self.largeur - l - m, y2, 2, l,
                                       self.hauteur + self.y - y2 - m, 'Sur-coincher')
        self.boutonCoinche = Bouton(self.x + self.largeur - l - m, y2, 1, l, self.hauteur + self.y - y2 - m, 'Coincher')
        self.flechePlusMoins = FlechePlusMoins(self.x + largeur_premiere_partie - 2 * m - 5 - LARGEUR_VIGNETTE - mb,
                                               self.y + m + HAUTEUR_VIGNETTE / 2 + mb, 20)
        self.x_valeur, self.y_valeur = self.x + m + 5, self.y + m + 10

        xs = int(self.x + self.largeur / 2 - (l + 2 * m) / 2)
        ys = y2 - m
        self.rectFenetreSecondaire = (xs, ys, l + 2 * m, self.hauteur + self.y - y2 + m)
        self.boutonSurCoincheSecondaire = Bouton(xs + m, ys + m, 2, l, self.hauteur + self.y - y2 - m, 'Sur-coincher')
        self.boutonCoincheSecondaire = Bouton(xs + m, ys + m, 1, l, self.hauteur + self.y - y2 - m, 'Coincher')
        self.rectSiAugmentationImpossible = (self.x, self.y + HAUTEUR_VIGNETTE + 2 * m,
                                             self.largeur, self.hauteur - HAUTEUR_VIGNETTE - 2 * m)

    def affiche(self):
        if self.monTour:
            self.afficheMonTour()
        else:
            self.affichePasMonTour()

    def afficheMonTour(self):
        if self.augmentation_possible and not self.sur_coinche_possible:
            afficheBulleRectanle(self.x, self.y, self.largeur, self.hauteur, 'b')
            for vignette in self.vignettes:
                vignette.affiche()
            self.flechePlusMoins.affiche()
            affiche_texte(str(self.valeur), self.x_valeur, self.y_valeur, taille=40)
        else:
            x, y, l, h = self.rectSiAugmentationImpossible
            afficheBulleRectanle(x, y, l, h, 'b')
        self.boutonPasse.affiche()
        if self.coinche_possible:
            self.boutonCoinche.affiche()
        elif self.sur_coinche_possible:
            self.boutonSurCoinche.affiche()

    def affichePasMonTour(self):
        derniere_enchere = FenetreEnchere.monJoueur.derniereEnchere
        if derniere_enchere is not None:
            x, y, l, h = self.rectFenetreSecondaire
            m = 20
            h -= 20
            if self.coinche_possible or self.sur_coinche_possible:
                y -= h - 3
            else:
                y += 20
            afficheBulleRectanle(x, y, l, h, 'b')
            x += 50
            if derniere_enchere == PASSE:
                affiche_texte('Passe', x + m - 3, y + m + 2, taille=30, couleur=GRIS_FONCE)
            elif derniere_enchere is not None:
                if derniere_enchere.coincher == 0:
                    affiche_texte(str(derniere_enchere.valeur), x + m - 5, y + m, taille=35)
                    SCREEN.blit(IMAGES_VIGNETTES[derniere_enchere.couleur], (x + 80, y + m))
                elif derniere_enchere.coincher == 1:
                    affiche_texte('Coinché !', x + m - 25, y + m + 2, taille=30, couleur=GRIS_FONCE)
                else:
                    affiche_texte('Sur-coinché !!', x + m - 58, y + m + 2, taille=30, couleur=GRIS_FONCE)

        if self.coinche_possible or self.sur_coinche_possible:
            x, y, l, h = self.rectFenetreSecondaire
            afficheBulleRectanle(x, y, l, h, 'b')
            if self.coinche_possible:
                self.boutonCoincheSecondaire.affiche()
            else:
                self.boutonSurCoincheSecondaire.affiche()

    def cree_nouvelle_enchere(self, couleur=None, coinche=0):
        if coinche == 0:
            return Enchere(self.valeur, couleur)
        else:
            return Enchere(self.ancienneEnchere.valeur, self.ancienneEnchere.couleur, coinche=coinche)

    def gere_clic(self, x_souris, y_souris):
        if self.monTour:
            return self.gere_clic_monTour(x_souris, y_souris)
        else:
            if self.coinche_possible:
                if self.boutonCoincheSecondaire.clic(x_souris, y_souris):
                    return self.cree_nouvelle_enchere(coinche=self.boutonCoincheSecondaire.parametre)
            elif self.sur_coinche_possible:
                if self.boutonSurCoincheSecondaire.clic(x_souris, y_souris):
                    return self.cree_nouvelle_enchere(coinche=self.boutonSurCoincheSecondaire.parametre)
            return None

    def gere_clic_monTour(self, x_souris, y_souris):
        if self.augmentation_possible and not self.sur_coinche_possible:
            r = self.flechePlusMoins.clic(x_souris, y_souris)
            if r == 1:
                if self.valeur < 250:
                    if self.valeur == FenetreEnchere.valeur_max:
                        self.valeur = 250
                    else:
                        self.valeur += FenetreEnchere.enchere_cran
            elif r == -1:
                if self.valeur > self.valeur_min:
                    if self.valeur == 250:
                        self.valeur = FenetreEnchere.valeur_max
                    else:
                        self.valeur -= FenetreEnchere.enchere_cran

            for vignette in self.vignettes:
                if vignette.clic(x_souris, y_souris):
                    return self.cree_nouvelle_enchere(couleur=vignette.paramettre)

        if self.boutonPasse.clic(x_souris, y_souris):
            return self.boutonPasse.parametre

        if self.coinche_possible:
            if self.boutonCoinche.clic(x_souris, y_souris):
                return self.cree_nouvelle_enchere(coinche=self.boutonCoinche.parametre)
        elif self.sur_coinche_possible:
            if self.boutonSurCoinche.clic(x_souris, y_souris):
                return self.cree_nouvelle_enchere(coinche=self.boutonSurCoinche.parametre)
        return None

    def nouvelle_enchere(self, enchere, monEquipe, monTour):
        self.monTour = monTour
        self.valeur_min = 80
        self.valeur = self.valeur_min
        self.coinche_possible = False
        self.sur_coinche_possible = False
        self.ancienneEnchere = enchere
        self.augmentation_possible = True
        if enchere is not None:
            if enchere.valeur == 250:
                self.augmentation_possible = False
            else:
                self.valeur_min = enchere.valeur + FenetreEnchere.enchere_cran
                self.valeur = self.valeur_min
            if enchere.joueur not in monEquipe.joueurs:
                if enchere.coincher == 0:
                    self.coinche_possible = True
                elif enchere.coincher == 1:
                    self.sur_coinche_possible = True
            else:
                if enchere.coincher == 1:
                    self.augmentation_possible = False
