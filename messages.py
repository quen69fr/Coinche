# coding: utf-8

from affichage import *
from outils import *


class Messages:
    monPseudo = None
    monCoequipierPseudo = None

    def __init__(self, x=LARGEUR / 2 + 100, y=87, largeur=LARGEUR / 2 - 100 * 2, hauteur=600):
        self.liste_messages = []
        self.message = ''
        self.bouton = Bouton(LARGEUR / 4 * 3, 36, '', 220, 54, 'Messages',
                             couleurRect=BLANC, couleurCountour=NOIR, centrer=True)
        self.x = x
        self.y = y
        self.largeur = largeur
        self.hauteur = hauteur
        self.taille_police = 24
        m = 10
        h = self.taille_police * 2 - 5
        largeur_bouton_envoyer = 80
        self.rect_barre = (self.x + m, self.y + self.hauteur - m - h, self.largeur - 3 * m - largeur_bouton_envoyer, h)

        self.bouton_envoyer = Bouton(self.x + self.largeur - largeur_bouton_envoyer - m, self.y + self.hauteur - m - h
                                     , '', largeur_bouton_envoyer, h, 'Envoyer', tailleTexte=18)

    def affiche(self):
        self.bouton.affiche()
        if self.bouton.selectionner:
            afficheBulleRectanle(self.x, self.y, self.largeur, self.hauteur, 'h')
            pygame.draw.rect(SCREEN, GRIS_FONCE, self.rect_barre, 3)
            affiche_texte(self.message, self.rect_barre[0] + 10, self.rect_barre[1] + 10, taille=self.taille_police)
            self.bouton_envoyer.affiche()

            l = self.liste_messages[:]
            l.reverse()
            y = self.rect_barre[1] - 10
            for i, (message, pseudo) in enumerate(l):
                t = None
                y -= self.taille_police + 15
                if i != 0 and pseudo == l[i - 1][1]:
                    y += 12
                if i != len(l) - 1 and pseudo == l[i + 1][1]:
                    t = message
                if y <= self.y + 10:
                    break
                if pseudo == Messages.monPseudo:
                    affiche_texte(message, self.x + self.largeur - 10, y, taille=self.taille_police,
                                  x_0left_1centre_2right=2)
                else:
                    if t is None:
                        t = f'{pseudo} : {message}'
                    if pseudo == Messages.monCoequipierPseudo:
                        affiche_texte(t, self.x + 10, y, taille=self.taille_police)
                    else:
                        affiche_texte(t, self.x + 10, y, couleur=GRIS_FONCE, taille=self.taille_police)

    def gere_clavier(self, event):
        if self.bouton.selectionner:
            if event.key == pygame.K_RETURN or event.key == 271:
                if self.message != '':
                    r = self.message
                    self.message = ''
                    return r
            elif event.key == pygame.K_BACKSPACE:
                self.message = self.message[:-1]
            else:
                if len(self.message) < 30:
                    self.message += event.unicode
        return None

    def gere_clic(self, x_souris, y_souris):
        if self.bouton.clic(x_souris, y_souris):
            if self.bouton.selectionner:
                self.bouton.selectionner = False
            else:
                self.bouton.selectionner = True
        elif self.bouton.selectionner:
            if self.bouton.selectionner:
                if self.bouton_envoyer.clic(x_souris, y_souris):
                    if self.message != '':
                        r = self.message
                        self.message = ''
                        return r
        return None
