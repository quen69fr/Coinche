
from affichage import *
from outils import *

class EcranPreparation:
    def __init__(self):
        self.listeJoueurOrdreTour = []

        m = 6
        self.boutonPremierJoueur = (LARGEUR // 2, (HAUTEUR - 3 * (m + HAUTEUR_IMAGE_PANNEAU_JOUEUR)) // 2 - 50)
        self.boutonBelote = ((LARGEUR - LARGEUR_IMAGE_PANNEAU_JOUEUR - m) // 2,
                             (HAUTEUR - (m + HAUTEUR_IMAGE_PANNEAU_JOUEUR)) // 2 - 50)
        self.bouton10en10 = ((LARGEUR + LARGEUR_IMAGE_PANNEAU_JOUEUR + m) // 2,
                             (HAUTEUR - (m + HAUTEUR_IMAGE_PANNEAU_JOUEUR)) // 2 - 50)
        self.boutonStart = (LARGEUR // 2, (HAUTEUR + m + HAUTEUR_IMAGE_PANNEAU_JOUEUR) // 2 - 25)

    def evenement_team(self, pseudo1, pseudo2):
        p1 = self.listeJoueurOrdreTour[0]
        self.listeJoueurOrdreTour.remove(pseudo2)
        self.listeJoueurOrdreTour.insert([2, 3, 1][self.listeJoueurOrdreTour.index(pseudo1)], pseudo2)
        while not self.listeJoueurOrdreTour[0] == p1:
            self.evenement_premier_joueur()

    def evenement_premier_joueur(self):
        self.listeJoueurOrdreTour.append(self.listeJoueurOrdreTour.pop(0))

    def clic_panneau(self, x_souris, y_souris, x, y):
        return (x - LARGEUR_IMAGE_PANNEAU_JOUEUR // 2 <= x_souris <= x + LARGEUR_IMAGE_PANNEAU_JOUEUR // 2 and
                y - HAUTEUR_IMAGE_PANNEAU_JOUEUR // 2 <= y_souris <= y + HAUTEUR_IMAGE_PANNEAU_JOUEUR // 2)

    def clic_premier_joueur(self, x_souris, y_souris):
        x, y = self.boutonPremierJoueur
        return self.clic_panneau(x_souris, y_souris, x, y)

    def clic_start(self, x_souris, y_souris):
        x, y = self.boutonStart
        return self.clic_panneau(x_souris, y_souris, x, y)

    def clic_10_en_10(self, x_souris, y_souris):
        x, y = self.bouton10en10
        return self.clic_panneau(x_souris, y_souris, x, y)

    def clic_belote(self, x_souris, y_souris):
        x, y = self.boutonBelote
        return self.clic_panneau(x_souris, y_souris, x, y)

    def affiche(self, belote, _10_en_10):
        x, y = self.boutonPremierJoueur
        image = IMAGE_PANNEAU_JOUEUR
        SCREEN.blit(image, (x - LARGEUR_IMAGE_PANNEAU_JOUEUR / 2, y - HAUTEUR_IMAGE_PANNEAU_JOUEUR / 2))
        affiche_texte("Dealer", x, y, centrer=True)

        x, y = self.boutonStart
        image = IMAGE_PANNEAU_JOUEUR_SELECTIONNE
        SCREEN.blit(image, (x - LARGEUR_IMAGE_PANNEAU_JOUEUR / 2, y - HAUTEUR_IMAGE_PANNEAU_JOUEUR / 2))
        affiche_texte("JOUER", x, y, centrer=True)

        x, y = self.boutonBelote
        image = IMAGE_PANNEAU_JOUEUR_SELECTIONNE if belote else IMAGE_PANNEAU_JOUEUR
        SCREEN.blit(image, (x - LARGEUR_IMAGE_PANNEAU_JOUEUR / 2, y - HAUTEUR_IMAGE_PANNEAU_JOUEUR / 2))
        affiche_texte("Belote", x, y, centrer=True)

        x, y = self.bouton10en10
        image = IMAGE_PANNEAU_JOUEUR_SELECTIONNE if _10_en_10 else IMAGE_PANNEAU_JOUEUR
        SCREEN.blit(image, (x - LARGEUR_IMAGE_PANNEAU_JOUEUR / 2, y - HAUTEUR_IMAGE_PANNEAU_JOUEUR / 2))
        affiche_texte("10 en 10", x, y, centrer=True)


