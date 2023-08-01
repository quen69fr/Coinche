# coding: utf-8

from affichage import *
from outils import *


# ==========================================================
class Pli:
    def __init__(self):
        self.joueur_cartes = []

    def ajouteCarte(self, carte_ou_nom, joueur):
        if isinstance(carte_ou_nom, Carte):
            self.joueur_cartes.append((joueur, carte_ou_nom))
        else:
            self.joueur_cartes.append((joueur, Carte(carte_ou_nom)))

    def trouveJoueurGagnant(self, enchere):
        joueur_carte_gagnante = None
        if enchere.couleur == DICTIONNAIRE_COULEURS["TA"]:
            for joueur, carte in self.joueur_cartes:
                if joueur_carte_gagnante is None or (carte.couleur == joueur_carte_gagnante[1].couleur
                                                     and (joueur_carte_gagnante[1].nb_pointsTA < carte.nb_pointsTA
                                                          or (joueur_carte_gagnante[1].nb_pointsTA == carte.nb_pointsTA
                                                              and joueur_carte_gagnante[1].valeur < carte.valeur))):
                    joueur_carte_gagnante = (joueur, carte)
        else:
            for joueur, carte in self.joueur_cartes:
                if carte.couleur == enchere.couleur:
                    if joueur_carte_gagnante is None or joueur_carte_gagnante[1].nb_pointsA < carte.nb_pointsA \
                            or (joueur_carte_gagnante[1].nb_pointsA == carte.nb_pointsA and carte.valeur == 8):
                        joueur_carte_gagnante = (joueur, carte)
            if joueur_carte_gagnante is not None:
                return joueur_carte_gagnante[0]
            for joueur, carte in self.joueur_cartes:
                if joueur_carte_gagnante is None or (carte.couleur == joueur_carte_gagnante[1].couleur
                                                     and (joueur_carte_gagnante[1].nb_points < carte.nb_points
                                                          or (joueur_carte_gagnante[1].nb_points == carte.nb_points
                                                              and joueur_carte_gagnante[1].valeur < carte.valeur))):
                    joueur_carte_gagnante = (joueur, carte)

        return joueur_carte_gagnante[0]

    def calculPoints(self, enchere):
        nb_points = 0
        for _, carte in self.joueur_cartes:
            if enchere.couleur == DICTIONNAIRE_COULEURS["SA"]:
                nb_points += carte.nb_pointsSA
            elif enchere.couleur == DICTIONNAIRE_COULEURS["TA"]:
                nb_points += carte.nb_pointsTA
            elif carte.couleur == enchere.couleur:
                nb_points += carte.nb_pointsA
            else:
                nb_points += carte.nb_points
        return nb_points

    def affiche(self, x=LARGEUR / 2, y=HAUTEUR / 2 - 90):
        for joueur, carte in self.joueur_cartes:
            if isinstance(joueur, MonJoueur):
                carte.affiche(x, y + 83, 5, 0)
            else:
                if joueur.hdg == 'h':
                    carte.affiche(x, y - 83, -2, 0)
                elif joueur.hdg == 'd':
                    carte.affiche(x + 110, y, -1, 0)
                else:
                    carte.affiche(x - 110, y, 6, 0)


# ==========================================================
class HistoriqueEnchere:
    monPseudo = None
    monCoequipierPseudo = None

    def __init__(self, x=150, y=87, largeur=LARGEUR / 2 - 150 * 2, hauteur=600):
        self.bouton = Bouton(LARGEUR / 4, 36, '', 220, 54, 'Historique',
                             couleurRect=BLANC, couleurCountour=NOIR, centrer=True)
        self.x = x
        self.y = y
        self.largeur = largeur
        self.hauteur = hauteur
        self.taille_police = 30

    def gere_clic(self, x_souris, y_souris):
        if self.bouton.clic(x_souris, y_souris):
            if self.bouton.selectionner:
                self.bouton.selectionner = False
            else:
                self.bouton.selectionner = True

    def affiche(self, encheres):
        self.bouton.affiche()
        if self.bouton.selectionner:
            afficheBulleRectanle(self.x, self.y, self.largeur, self.hauteur, 'h')
            l = encheres[:]
            l.reverse()
            y = self.y + self.hauteur - 10
            for i, enchere in enumerate(l):
                pseudo = enchere.joueur.pseudo
                affiche_couleur = False
                if enchere.coincher == 0:
                    t = f'{pseudo} : {enchere.valeur}'
                    affiche_couleur = True
                elif enchere.coincher == 1:
                    t = f'{pseudo} : Coinché !'
                else:
                    t = f'{pseudo} : Sur-coinché !!'
                y -= self.taille_police + 15
                if pseudo == HistoriqueEnchere.monPseudo:
                    x = self.x + self.largeur - 10
                    xt = x
                    if affiche_couleur:
                        xt -= LARGEUR_VIGNETTE + 5
                    affiche_texte(t, xt, y, taille=self.taille_police, x_0left_1centre_2right=2)
                    if affiche_couleur:
                        SCREEN.blit(IMAGES_VIGNETTES[enchere.couleur], (x - LARGEUR_VIGNETTE, y - 2))
                elif pseudo == HistoriqueEnchere.monCoequipierPseudo:
                    x = self.x + self.largeur - 10
                    xt = x
                    if affiche_couleur:
                        xt -= LARGEUR_VIGNETTE + 5
                    affiche_texte(t, xt, y, couleur=GRIS_FONCE, taille=self.taille_police, x_0left_1centre_2right=2)
                    if affiche_couleur:
                        SCREEN.blit(IMAGES_VIGNETTES[enchere.couleur], (x - LARGEUR_VIGNETTE, y - 2))
                else:
                    l = affiche_texte(t, self.x + 10, y, couleur=GRIS_FONCE, taille=self.taille_police,
                                      return_largeur=True)
                    if affiche_couleur:
                        SCREEN.blit(IMAGES_VIGNETTES[enchere.couleur], (self.x + 10 + l + 5, y - 2))


# ==========================================================
class Equipe:
    def __init__(self, joueurs):
        self.joueurs = joueurs
        self.nombrePoints = 0
        self.nb_points_fait_derniere_partie = 0
        self.nb_points_annonces_derniere_partie = 0
        self.plis = []
        self.monEquipe = isinstance(self.joueurs[0], MonJoueur)

        # Affichage :
        self.y_texte = 460
        self.y_texte_pts = 500
        dx = 77
        y = 400
        l = 385
        h = 385
        if self.monEquipe:
            x = LARGEUR - 37
            self.texte = 'MON EQUIPE'
            self.x_texte = LARGEUR - 215
            self.image = IMAGE_PANNEAU_SCORE_DROITE
            self.x_image, self.y_image = LARGEUR - LARGEUR_IMAGE_PANNEAU_SCORE, 330
            self.rectangleBullePlis = LARGEUR - dx - l, y - h / 2, l, h, 'd'
        else:
            x = 37
            self.texte = 'ADVERSAIRES'
            self.x_texte = 215
            self.image = IMAGE_PANNEAU_SCORE_GAUCHE
            self.x_image, self.y_image = 0, 330
            self.rectangleBullePlis = dx, y - h / 2, l, h, 'g'
        self.boutonPli = Bouton(x, 400, '', 50, 50, '0', tailleTexte=40, couleurRect=BLANC, couleurCountour=NOIR,
                                centrer=True)
        m = 10
        l = 120
        h = HAUTEUR_VIGNETTE + 2 * m
        y = 560
        self.xt, self.yt = self.x_texte + m - l / 2, y + m
        self.xv, self.yv = self.x_texte + 75 - l / 2, y + m
        self.rectangleBulle = (self.x_texte - l / 2, y, l, h)

        self.rectangleEtTexteBulleCoinche = (self.x_texte - l / 2 - 10, y + h + m, l + 20, h,
                                             self.x_texte + m - l / 2 - 10, y + 2 * m + h)
        self.rectangleEtTexteBulleSurCoinche = (self.x_texte - l / 2 - 38, y + h + m, l + 76, h,
                                                self.x_texte + m - l / 2 - 38, y + 2 * m + h)

    def calcul_points(self, enchere, dis_de_der):
        r = 0
        if dis_de_der:
            r = 10
        for pli in self.plis:
            r += pli.calculPoints(enchere)
        return r

    def nb_belotes(self, belotes):
        r = 0
        for joueur, _ in belotes:
            if joueur in self.joueurs:
                r += 1
        return r

    def fin_tour(self, enchere, dis_de_der, belotes):
        nb = self.calcul_points(enchere, dis_de_der)
        nb_belote = self.nb_belotes(belotes)
        self.nb_points_fait_derniere_partie = nb + 20 * nb_belote
        valeur_enchere = enchere.valeur
        enchere_coincher = enchere.coincher
        suplement = 0
        if (enchere.joueur in self.joueurs and enchere_coincher != 1) or (enchere.joueur not in self.joueurs
                                                                          and enchere_coincher == 1):
            self.nb_points_annonces_derniere_partie = valeur_enchere
            if nb >= max(80, valeur_enchere - 20 * nb_belote) or (nb == 162 and valeur_enchere == 250):
                suplement += 10 * int((valeur_enchere + 5) / 10)
                if len(self.plis) == 8:
                    suplement += 250
                else:
                    suplement += 10 * int((nb + 5) / 10)
        else:
            self.nb_points_annonces_derniere_partie = 0
            if nb > 162 - max(80, valeur_enchere - 20 * (len(belotes) - nb_belote)) \
                    and not (nb == 0 and valeur_enchere == 250):
                suplement += 160
                suplement += 10 * int((valeur_enchere + 5) / 10)
            else:
                if enchere_coincher == 0:
                    suplement += (10 * int((nb + 5) / 10))

        self.nombrePoints += suplement * (enchere_coincher + 1) + 20 * nb_belote
        self.plis = []

    def regroupe_cartes(self):
        p = []
        for pli in self.plis:
            for _, carte in pli.joueur_cartes:
                p.append(carte)
        return p

    def gere_clic(self, x_souris, y_souris):
        if len(self.plis) > 0:
            if self.boutonPli.clic(x_souris, y_souris):
                if self.boutonPli.selectionner:
                    self.boutonPli.selectionner = False
                else:
                    self.boutonPli.selectionner = True
                return True
        return False

    def affiche(self, enchere):
        SCREEN.blit(self.image, (self.x_image, self.y_image))
        affiche_texte(self.texte, self.x_texte, self.y_texte, centrer=True)
        affiche_texte(str(self.nombrePoints), self.x_texte, self.y_texte_pts, taille=44, centrer=True)
        if self.nb_points_annonces_derniere_partie == 0:
            texte = str(self.nb_points_fait_derniere_partie)
            tailleTexte = 30
        else:
            texte = f'{self.nb_points_fait_derniere_partie}/{self.nb_points_annonces_derniere_partie}'
            tailleTexte = 25
        affiche_texte(texte, self.x_texte, self.y_texte_pts - 111, taille=tailleTexte, centrer=True)
        if enchere is not None and ((enchere.joueur in self.joueurs and enchere.coincher != 1)
                                    or enchere.joueur not in self.joueurs and enchere.coincher == 1):
            x, y, l, h = self.rectangleBulle
            afficheBulleRectanle(x, y, l, h, 'h')
            affiche_texte(str(enchere.valeur), self.xt, self.yt, taille=35)
            SCREEN.blit(IMAGES_VIGNETTES[enchere.couleur], (self.xv, self.yv))
            if enchere.coincher == 1:
                x, y, l, h, x2, y2 = self.rectangleEtTexteBulleCoinche
                afficheBulleRectanle(x, y, l, h, 'h')
                affiche_texte('Coinché', x2, y2, couleur=GRIS_FONCE)
            elif enchere.coincher == 2:
                x, y, l, h, x2, y2 = self.rectangleEtTexteBulleSurCoinche
                afficheBulleRectanle(x, y, l, h, 'h')
                affiche_texte('Sur-coinché', x2, y2, couleur=GRIS_FONCE)

        n = str(len(self.plis))
        if self.boutonPli.texte != n:
            self.boutonPli.texte = n
            self.boutonPli.selectionner = False
        if len(self.plis) > 0:
            self.boutonPli.affiche()
            if self.boutonPli.selectionner:
                x, y, l, h, hbdg = self.rectangleBullePlis
                afficheBulleRectanle(x, y, l, h, hbdg)
                self.plis[-1].affiche(x + l / 2, y + h / 2)


# ==========================================================
class AutreJoueur:
    def __init__(self, pseudo):
        self.pseudo = pseudo
        self.joueurSuivant = None
        self.hdg = ''
        self.derniereEnchere = PASSE
        self.x = LARGEUR / 2
        self.y = 80
        self.xt = self.x
        self.yt = self.y - 35
        self.x_jeton, self.y_jeton = -100, -100

    def met_a_jour_hdg(self, hdg):
        self.hdg = hdg
        self.y_jeton = 80
        if self.hdg == 'h':
            self.x = LARGEUR / 2
            self.y = HAUTEUR_IMAGE_PANNEAU_JOUEUR / 2 + 4 + 50
            self.xt = self.x
            self.yt = self.y - 50
            self.x_jeton = 785
        elif self.hdg == 'd':
            self.x = LARGEUR - 159
            self.y = 200
            self.xt = LARGEUR - LARGEUR_IMAGE_PANNEAU_JOUEUR / 2 - 5
            self.yt = self.y - 35
            self.x_jeton = LARGEUR - 244 - LARGEUR_IMAGE_JETON_DEALER
        else:
            self.x = 159
            self.y = 200
            self.xt = LARGEUR_IMAGE_PANNEAU_JOUEUR / 2 + 5
            self.yt = self.y - 35
            self.x_jeton = 244

    def affiche(self, etat_partie, monTour, joueur_dealer):
        if (etat_partie == ETAT_PARTIE_JEU and joueur_dealer == self.joueurSuivant) \
                or (etat_partie in [ETAT_PARTIE_ENCHERE, ETAT_PARTIE_PREPARATION] and joueur_dealer == self):
            SCREEN.blit(IMAGE_JETON_DEALER, (self.x_jeton, self.y_jeton))
        c = NOIR
        affiche_carte = False
        image = IMAGE_PANNEAU_JOUEUR
        if monTour:
            if etat_partie == ETAT_PARTIE_JEU:
                affiche_carte = True
            image = IMAGE_PANNEAU_JOUEUR_SELECTIONNE
        SCREEN.blit(image, (self.xt - LARGEUR_IMAGE_PANNEAU_JOUEUR / 2, self.yt - HAUTEUR_IMAGE_PANNEAU_JOUEUR / 2))
        affiche_texte(self.pseudo.upper(), self.xt, self.yt, couleur=c, centrer=True)
        if affiche_carte:
            SCREEN.blit(IMAGE_JOUEUR_TOUR, (self.xt - LARGEUR_IMAGE_PANNEAU_JOUEUR / 2 + 198,
                                            self.yt - HAUTEUR_IMAGE_PANNEAU_JOUEUR / 2 + 33))
        if etat_partie == ETAT_PARTIE_ENCHERE and (monTour or self.derniereEnchere is not None):
            m = 10
            l = 120
            h = HAUTEUR_VIGNETTE + 2 * m
            afficheBulleRectanle(self.x - l / 2, self.y, l, h, self.hdg)
            if monTour:
                affiche_texte(' ... ', self.x + m - l / 2 - 13, self.y + m - 50, taille=90, couleur=GRIS_FONCE)
            elif self.derniereEnchere == PASSE:
                affiche_texte('Passe', self.x + m - l / 2 + 7, self.y + m + 2, taille=30, couleur=GRIS_FONCE)
            elif self.derniereEnchere is not None:
                if self.derniereEnchere.coincher == 0:
                    affiche_texte(str(self.derniereEnchere.valeur), self.x + m - l / 2, self.y + m, taille=35)
                    SCREEN.blit(IMAGES_VIGNETTES[self.derniereEnchere.couleur], (self.x + 75 - l / 2, self.y + m))
                else:
                    mx = 0
                    if self.hdg == 'd':
                        mx = 1
                    elif self.hdg == 'h':
                        mx = 0.5
                    if self.derniereEnchere.coincher == 1:
                        afficheBulleRectanle(self.x - l / 2 - 50 * mx, self.y, l + 50, h, self.hdg)
                        affiche_texte('Coinché !', self.x + m - l / 2 + 7 - 50 * mx, self.y + m + 2,
                                      taille=30, couleur=GRIS_FONCE)
                    else:
                        afficheBulleRectanle(self.x - l / 2 - mx * 116, self.y, l + 116, h, self.hdg)
                        affiche_texte('Sur-coinché !!', self.x + m - l / 2 + 7 - 116 * mx, self.y + m + 2,
                                      taille=30, couleur=GRIS_FONCE)

    def clic(self, x_souris, y_souris):
        return (self.xt - LARGEUR_IMAGE_PANNEAU_JOUEUR // 2 <= x_souris <= self.xt + LARGEUR_IMAGE_PANNEAU_JOUEUR // 2
                and
                self.yt - HAUTEUR_IMAGE_PANNEAU_JOUEUR // 2 <= y_souris <= self.yt + HAUTEUR_IMAGE_PANNEAU_JOUEUR // 2)

    def afficheBelote(self, rebelote):
        m = 10
        l = 162 if rebelote else 128
        h = HAUTEUR_VIGNETTE + 2 * m
        afficheBulleRectanle(self.x - l / 2, self.y, l, h, self.hdg)
        texte = 'Rebelote' if rebelote else 'Belote'
        affiche_texte(texte, self.x + m - l / 2 + 7, self.y + m + 2, taille=30, couleur=GRIS_FONCE)


# ==========================================================
class MonJoueur:
    def __init__(self, pseudo):
        self.pseudo = pseudo
        self.catres = []
        self.joueurSuivant = None
        self.derniereEnchere = None
        self.clignotte = 0
        self.boutonCarteBelote = None

    def affiche(self, etat_partie, monTour, joueur_dealer):
        if (etat_partie == ETAT_PARTIE_JEU and joueur_dealer == self.joueurSuivant) \
                or (etat_partie in [ETAT_PARTIE_ENCHERE, ETAT_PARTIE_PREPARATION] and joueur_dealer == self):
            SCREEN.blit(IMAGE_JETON_DEALER, (463, 436))
        c = NOIR
        affiche_carte = False
        image = IMAGE_PANNEAU_JOUEUR
        if monTour:
            if etat_partie == ETAT_PARTIE_JEU:
                affiche_carte = True
            image = IMAGE_PANNEAU_JOUEUR_SELECTIONNE
        SCREEN.blit(image, (LARGEUR / 2 - LARGEUR_IMAGE_PANNEAU_JOUEUR / 2, 480 - HAUTEUR_IMAGE_PANNEAU_JOUEUR / 2))
        if len(self.pseudo) < 7:
            t = f'MOI : {self.pseudo.upper()}'
        else:
            t = f'{self.pseudo.upper()}'
        affiche_texte(t, LARGEUR / 2, 480, couleur=c, centrer=True)
        if affiche_carte:
            SCREEN.blit(IMAGE_JOUEUR_TOUR, (LARGEUR / 2 - LARGEUR_IMAGE_PANNEAU_JOUEUR / 2 + 198,
                                            480 - HAUTEUR_IMAGE_PANNEAU_JOUEUR / 2 + 33))
        self.affiche_cartes()

    def affiche_cartes(self, x=LARGEUR / 2, y=800 + HAUTEUR - 80, angle_total=40, angle_min=8, rayon=800):
        nb_cartes = len(self.catres)

        angle_entre_cartes = angle_min
        if nb_cartes > angle_total / angle_min:
            angle_entre_cartes = angle_total / nb_cartes

        for i in range(nb_cartes):
            a = (((nb_cartes - i - 1) + 0.5 - nb_cartes / 2) * angle_entre_cartes)
            self.catres[i].affiche(x, y, a, rayon)

        if self.boutonCarteBelote is not None:
            self.boutonCarteBelote.parametre.affichePanneauBelote()
            self.boutonCarteBelote.affiche()

    def clic_sur_cartes(self, x_souris, y_souris):
        if self.boutonCarteBelote is not None and self.boutonCarteBelote.clic(x_souris, y_souris):
            self.boutonCarteBelote.selectionner = True
            return self.boutonCarteBelote.parametre
        r = None
        l = self.catres[:]
        l.reverse()
        for carte in l:
            if carte.clic(x_souris, y_souris):
                r = carte
                break
        return r

    def gere_cartes_selectionnees(self, carte_clic):
        carte_selec = None
        for i, carte in enumerate(self.catres):
            if carte.selectionner:
                carte_selec = carte
        if carte_selec is None:
            carte_clic.selectionner = True
        else:
            carte_selec.selectionner = False
            if carte_clic != carte_selec:
                self.catres.remove(carte_selec)
                self.catres.insert(self.catres.index(carte_clic) + 1, carte_selec)

    def prepare_cartes(self):
        self.catres = sorted(self.catres, key=attrgetter('couleur', 'nb_pointsA', 'valeur'), reverse=True)

    def carte_possible_pour_pli(self, carte, pli, enchere):
        if len(pli.joueur_cartes) == 0:
            return True
        else:
            couleur_jouee = pli.joueur_cartes[0][1].couleur
            couleur_atout = couleur_jouee if enchere.couleur == DICTIONNAIRE_COULEURS["TA"] else enchere.couleur
            couleur_carte = carte.couleur
            plus_gros_atout_joue = None
            for _, c in pli.joueur_cartes:
                if c.couleur == couleur_atout:
                    if plus_gros_atout_joue is None or plus_gros_atout_joue.nb_pointsA < c.nb_pointsA \
                            or (plus_gros_atout_joue.nb_pointsA == c.nb_pointsA
                                and plus_gros_atout_joue.valeur < c.valeur):
                        plus_gros_atout_joue = c
            if couleur_jouee == couleur_carte:
                if couleur_carte == couleur_atout:
                    if plus_gros_atout_joue.nb_pointsA < carte.nb_pointsA \
                            or (plus_gros_atout_joue.nb_pointsA == carte.nb_pointsA
                                and plus_gros_atout_joue.valeur < carte.valeur):
                        return True
                    else:
                        for c in self.catres:
                            if c.couleur == couleur_atout and \
                                    (plus_gros_atout_joue.nb_pointsA < c.nb_pointsA
                                     or (plus_gros_atout_joue.nb_pointsA == c.nb_pointsA
                                         and plus_gros_atout_joue.valeur < c.valeur)):
                                return False
                        return True
                else:
                    return True
            else:
                for c in self.catres:
                    if c.couleur == couleur_jouee:
                        return False
                if enchere.couleur == DICTIONNAIRE_COULEURS["TA"] or \
                        pli.trouveJoueurGagnant(enchere) == self.joueurSuivant.joueurSuivant:
                    return True
                else:
                    if couleur_carte == couleur_atout:
                        if plus_gros_atout_joue is None or plus_gros_atout_joue.nb_pointsA < carte.nb_pointsA or \
                                (plus_gros_atout_joue.nb_pointsA == carte.nb_pointsA
                                 and plus_gros_atout_joue.valeur < carte.valeur):
                            return True
                        else:
                            for c in self.catres:
                                if c.couleur == couleur_atout and \
                                        (plus_gros_atout_joue is None or plus_gros_atout_joue.nb_pointsA < c.nb_pointsA
                                         or (plus_gros_atout_joue.nb_pointsA == c.nb_pointsA
                                             and plus_gros_atout_joue.valeur < c.valeur)):
                                    return False
                            return True
                    else:
                        for c in self.catres:
                            if c.couleur == couleur_atout and \
                                    (plus_gros_atout_joue is None or plus_gros_atout_joue.nb_pointsA < c.nb_pointsA
                                     or (plus_gros_atout_joue.nb_pointsA == c.nb_pointsA
                                         and plus_gros_atout_joue.valeur < c.valeur)):
                                return False
                        return True

    def trouve_carte_nom(self, nom):
        for carte in self.catres:
            if carte.nom == nom:
                return carte

    def nb_carte_belote(self, couleur):
        n = 0
        for carte in self.catres:
            if carte.belote(couleur):
                n += 1
        return n

    def afficheBelote(self, rebelote):
        m = 10
        l = 162 if rebelote else 128
        h = HAUTEUR_VIGNETTE + 2 * m
        x = (LARGEUR + LARGEUR_IMAGE_PANNEAU_JOUEUR + l) // 2 + 16
        y = 480 - h // 2 - 3
        afficheBulleRectanle(x - l / 2, y, l, h, 'g')
        texte = 'Rebelote' if rebelote else 'Belote'
        affiche_texte(texte, x + m - l / 2 + 7, y + m + 2, taille=30, couleur=GRIS_FONCE)


# ==========================================================
class Carte:
    def __init__(self, nom):
        self.nom = nom
        valeur, couleur = self.nom.split('-')
        if valeur[0] == '0':
            valeur = valeur[1]
        self.valeur = eval(valeur)
        self.couleur = DICTIONNAIRE_COULEURS[couleur]
        self.image = DICTIONNAIRE_IMAGES_CARTES[self.nom]
        self.selectionner = False
        self.nb_points = DICTIONNAIRE_POINTS_CARTE_VALEUR[self.valeur]['NA']
        self.nb_pointsA = DICTIONNAIRE_POINTS_CARTE_VALEUR[self.valeur]['A']
        self.nb_pointsSA = DICTIONNAIRE_POINTS_CARTE_VALEUR[self.valeur]['SA']
        self.nb_pointsTA = DICTIONNAIRE_POINTS_CARTE_VALEUR[self.valeur]['TA']

        self.x_centre = 0
        self.y_centre = 0
        self.angle = 0
        self.rayon = 0
        self.x_image = 0
        self.y_image = 0
        self.largeur_image = 0
        self.hauteur_image = 0

    # ----------------------------------------------------
    def belote(self, couleur):
        return self.valeur in [12, 13] and (couleur is None or self.couleur == couleur)

    # ----------------------------------------------------
    def affiche(self, x, y, angle, rayon):
        self.angle = angle
        self.a_rad = self.angle * math.pi / 180
        self.rayon = rayon
        if self.selectionner:
            self.rayon += 10
        self.x_centre = x - math.sin(self.a_rad) * self.rayon
        self.y_centre = y - math.cos(self.a_rad) * self.rayon

        image_tournee = pygame.transform.rotozoom(self.image, self.angle, 1)

        self.largeur_image = image_tournee.get_width()
        self.hauteur_image = image_tournee.get_height()
        self.x_image = int(self.x_centre - self.largeur_image / 2)
        self.y_image = int(self.y_centre - self.hauteur_image / 2)

        SCREEN.blit(image_tournee, (self.x_image, self.y_image))

    def affichePanneauBelote(self):
        x = self.x_centre - math.sin(self.a_rad) * 105
        y = self.y_centre - math.cos(self.a_rad) * 105
        l, h = 150, 65
        m = 15
        x -= l / 2 + m
        y -= h + m
        afficheBulleRectanle(x, y, l + 2 * m, h + m - 2, 'b')

    def boutonBelote(self):
        x = self.x_centre - math.sin(self.a_rad) * 105
        y = self.y_centre - math.cos(self.a_rad) * 105
        l, h = 150, 65
        m = 15
        x -= l / 2 + m
        y -= h + m
        return Bouton(x + m, y + m, self, l, h - m, 'Belote')

    # ----------------------------------------------------
    def clic(self, x_souris, y_souris):
        image_tournee = pygame.transform.rotozoom(self.image, self.angle, 1)

        xp = x_souris - self.x_image
        yp = y_souris - self.y_image
        if 0 <= xp < self.largeur_image and 0 <= yp < self.hauteur_image:
            if image_tournee.get_at((xp, yp))[3] != 0:
                return True
        return False
