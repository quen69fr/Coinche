# coding: utf-8

from affichage import *
from outils import *


ETAT_IP = 0
ETAT_PSEUDO = 1
ETAT_COEQUIPIER = 2
ETAT_ATTENTE = 3
ETAT_FIN = 4


class EcranMiseEnPlace:
    def __init__(self, largeur=330, hauteur=190):
        self.x = LARGEUR / 2 - largeur / 2
        self.y = HAUTEUR / 2 - hauteur / 2
        self.largeur = largeur
        self.hauteur = hauteur
        self.etat = ETAT_IP

        h = 50
        m = 10
        self.message = ADRESSE_IP
        self.rect_barre = (self.x + m, self.y + m + h, self.largeur - 2 * m, 50)
        self.bouton = Bouton(self.x + m, self.rect_barre[1] + self.rect_barre[3] + m, '', self.rect_barre[2],
                             self.y + self.hauteur - self.rect_barre[1] - self.rect_barre[3] - 2 * m, 'Valider')
        self.validee = False
        self.listePseudoAGerer = []

        self.yPseudo = 300
        self.delta_xPseudo = 280

    def gere_clavier(self, event):
        self.validee = False
        if event.key == pygame.K_RETURN or event.key == 271:
            if self.message != '':
                self.validee = True
        elif event.key == pygame.K_BACKSPACE:
            self.message = self.message[:-1]
        else:
            self.message += event.unicode

    def clic(self, x_souris, y_souris):
        if self.bouton.clic(x_souris, y_souris):
            if self.message != '':
                self.validee = True

    def affichePseudo(self, x, y, pseudo, selectionne):
        image = IMAGE_PANNEAU_JOUEUR
        if selectionne:
            image = IMAGE_PANNEAU_JOUEUR_SELECTIONNE
        SCREEN.blit(image, (x - LARGEUR_IMAGE_PANNEAU_JOUEUR / 2, y - HAUTEUR_IMAGE_PANNEAU_JOUEUR / 2))
        affiche_texte(pseudo.upper(), x, y, centrer=True)

    def clicPseudo(self, x_souris, y_souris):
        if abs(self.yPseudo - y_souris) <= HAUTEUR_IMAGE_PANNEAU_JOUEUR / 2:
            for i, pseudo in enumerate(self.listePseudoAGerer):
                if abs(x_souris - LARGEUR / 2 - (i - 1) * 300) <= LARGEUR_IMAGE_PANNEAU_JOUEUR / 2:
                    return pseudo
        return None

    def affiche(self, monCoequipierPseudo):
        t = None
        if self.etat == ETAT_IP:
            t = 'Adresse ip'
        elif self.etat == ETAT_PSEUDO:
            t = 'Votre pseudo'
        else:
            for i in range(3):
                pseudo = ' '
                if len(self.listePseudoAGerer) >= i + 1:
                    pseudo = self.listePseudoAGerer[i]
                self.affichePseudo(LARGEUR / 2 + (i - 1) * self.delta_xPseudo, self.yPseudo, pseudo,
                                   monCoequipierPseudo == pseudo)
        if t is not None:
            pygame.draw.rect(SCREEN, BLANC, (self.x, self.y, self.largeur, self.hauteur))
            pygame.draw.rect(SCREEN, NOIR, (self.x, self.y, self.largeur, self.hauteur), 3)
            affiche_texte(t, self.x + self.largeur / 2, self.y + 30, taille=40, centrer=True)
            pygame.draw.rect(SCREEN, GRIS_FONCE, self.rect_barre, 3)
            affiche_texte(self.message, self.rect_barre[0] + 10, self.rect_barre[1] + 10)
            self.bouton.affiche()

    def etat_suivant(self):
        self.validee = False
        self.message = ''
        if self.etat != ETAT_FIN:
            self.etat += 1
