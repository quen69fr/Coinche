# coding: utf-8

from reseauMessage import *
from ecranPreparation import *
from ecranMiseEnPlace import *
from messages import *
from joueur import *
from enchere import *
from outils import *

if __name__ == "__main__":
    etat_partie = ETAT_PARTIE_MISE_EN_PLACE
    reseau = ReseauClient()

    monPseudo = ''
    playWithBelote = False
    play10en10 = False
    random_liste_carte = []
    dictionnaire_joueur = {}
    monJoueur = MonJoueur
    monCoequipier = AutreJoueur
    monEquipe = Equipe
    equipeAdverse = Equipe
    paquetCartes = []
    ecran_mise_en_place = EcranMiseEnPlace()
    ecran_preparation = EcranPreparation()

    action_possible = True
    affichage = True
    listePseudoOrdreTour = []
    listeJoueurOrdreTour = []
    joueurDistribution = None
    joueurTour = None
    joueurPremier = None
    joueurSuivant = False
    belotesTour = []
    belotes = []
    distribution = False
    encheres = []
    fenetre_enchere = FenetreEnchere()
    pli = Pli()
    gelEcranCompteur = 0
    messages = Messages()
    historiqueEnchere = HistoriqueEnchere()

    clic_up_down_gauche = 0
    clic_gauche = False
    clic_up_down_droit = 0
    clic_droit = False

    while True:
        # ----------------------------------- Evenements -----------------------------------
        souris = pygame.mouse.get_pos()
        x_souris = souris[0]
        y_souris = souris[1]

        clic_droit = False
        clic_gauche = False
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if etat_partie == ETAT_PARTIE_MISE_EN_PLACE and (ecran_mise_en_place.etat == ETAT_IP
                                                                 or ecran_mise_en_place.etat == ETAT_PSEUDO):
                    ecran_mise_en_place.gere_clavier(event)
                if etat_partie == ETAT_PARTIE_JEU or etat_partie == ETAT_PARTIE_ENCHERE:
                    r = messages.gere_clavier(event)
                    if r is not None:
                        messages.nouveauMessage(r, monPseudo)
                        reseau.envoieMessage(r)
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
            if clic_up_down_gauche == 1:
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    clic_up_down_gauche = 0
                    clic_gauche = True
                    if X_IMAGE_QUITTER_BOUTON < x_souris < X_IMAGE_QUITTER_BOUTON + LARGEUR_IMAGE_BOUTON \
                            and Y_IMAGE_QUITTER_BOUTON < y_souris < (Y_IMAGE_QUITTER_BOUTON + HAUTEUR_IMAGE_BOUTON):
                        pygame.quit()
                        exit(0)
            else:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    clic_up_down_gauche = 1
            if clic_up_down_droit == 1:
                if event.type == pygame.MOUSEBUTTONUP and event.button == 3:
                    clic_up_down_droit = 0
                    clic_droit = True
            else:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                    clic_up_down_droit = 1

        # ---------------------------- Preparation de la partie ----------------------------
        if etat_partie == ETAT_PARTIE_MISE_EN_PLACE:
            if clic_gauche:
                ecran_mise_en_place.clic(x_souris, y_souris)
            if ecran_mise_en_place.etat == ETAT_IP:
                if ecran_mise_en_place.validee:
                    reseau.adresse_ip = ecran_mise_en_place.message
                    ecran_mise_en_place.etat_suivant()
            elif ecran_mise_en_place.etat == ETAT_PSEUDO:
                if ecran_mise_en_place.validee:
                    monPseudo = ecran_mise_en_place.message
                    monJoueur = MonJoueur(monPseudo)
                    dictionnaire_joueur[monPseudo] = monJoueur
                    reseau.login(monPseudo)
                    ecran_mise_en_place.etat_suivant()
            elif ecran_mise_en_place.etat == ETAT_ATTENTE_JOUEURS:
                evt = reseau.regardeEvenementsNonFait()
                if evt is not None:
                    if evt[EVENT_TYPE] == EVT_DEAL:
                        random_liste_carte = evt[EVENT_CONTENU]
                    elif evt[EVENT_TYPE] == EVT_LOGIN:
                        if evt[EVENT_PSEUDO] == monPseudo:
                            monJoueur = MonJoueur(monPseudo)
                            dictionnaire_joueur[monPseudo] = monJoueur
                        else:
                            p = evt[EVENT_PSEUDO]
                            if p not in ecran_mise_en_place.listePseudoAGerer:
                                dictionnaire_joueur[p] = AutreJoueur(p)
                                ecran_mise_en_place.listePseudoAGerer.append(p)
                        if len(ecran_mise_en_place.listePseudoAGerer) == 3:
                            listePseudoOrdreTour = sorted(ecran_mise_en_place.listePseudoAGerer + [monPseudo])
                            ecran_preparation.listeJoueurOrdreTour = listePseudoOrdreTour
                            etat_partie = ETAT_PARTIE_PREPARATION

        elif etat_partie == ETAT_PARTIE_PREPARATION:
            start = False
            evt = reseau.regardeEvenementsNonFait()
            if evt is not None:
                if evt[EVENT_TYPE] == EVT_TEAM:
                    ecran_preparation.evenement_team(evt[EVENT_PSEUDO], evt[EVENT_CONTENU])
                elif evt[EVENT_TYPE] == EVT_BELOTE:
                    playWithBelote = not playWithBelote
                elif evt[EVENT_TYPE] == EVT_PREMIER_JOUEUR:
                    ecran_preparation.evenement_premier_joueur()
                elif evt[EVENT_TYPE] == EVT_10_EN_10:
                    play10en10 = not play10en10
                elif evt[EVENT_TYPE] == EVT_START:
                    start = True

            if clic_gauche:
                if ecran_preparation.clic_premier_joueur(x_souris, y_souris):
                    reseau.envoiePremierJoueur()
                    ecran_preparation.evenement_premier_joueur()
                elif ecran_preparation.clic_start(x_souris, y_souris):
                    reseau.envoieStart()
                    start = True
                elif ecran_preparation.clic_belote(x_souris, y_souris):
                    reseau.envoieBelotte()
                    playWithBelote = not playWithBelote
                elif ecran_preparation.clic_10_en_10(x_souris, y_souris):
                    reseau.envoie10en10()
                    play10en10 = not play10en10
                else:
                    for pseudo in listePseudoOrdreTour:
                        if pseudo == monPseudo:
                            continue
                        if dictionnaire_joueur[pseudo].clic(x_souris, y_souris):
                            reseau.team(pseudo)
                            ecran_preparation.evenement_team(monPseudo, pseudo)

            joueurCommencePseudo = listePseudoOrdreTour[0]

            i = listePseudoOrdreTour.index(monPseudo)
            monAdversaireDroitePseudo = listePseudoOrdreTour[i - 1]
            monAdversaireGauchePseudo = listePseudoOrdreTour[i - 3]
            monCoequipierPseudo = listePseudoOrdreTour[i - 2]
            monCoequipier = dictionnaire_joueur[monCoequipierPseudo]
            dictionnaire_joueur[monAdversaireGauchePseudo].met_a_jour_hdg('g')
            monCoequipier.met_a_jour_hdg('h')
            dictionnaire_joueur[monAdversaireDroitePseudo].met_a_jour_hdg('d')

            if start:
                Messages.monPseudo = monPseudo
                Messages.monCoequipierPseudo = monCoequipierPseudo
                HistoriqueEnchere.monPseudo = monPseudo
                HistoriqueEnchere.monCoequipierPseudo = monCoequipierPseudo
                monEquipe = Equipe([monJoueur, monCoequipier])
                equipeAdverse = Equipe([dictionnaire_joueur[monAdversaireGauchePseudo],
                                        dictionnaire_joueur[monAdversaireDroitePseudo]])

                monJoueur.joueurSuivant = equipeAdverse.joueurs[0]
                equipeAdverse.joueurs[0].joueurSuivant = monCoequipier
                monCoequipier.joueurSuivant = equipeAdverse.joueurs[1]
                equipeAdverse.joueurs[1].joueurSuivant = monJoueur

                FenetreEnchere.monJoueur = monJoueur
                joueurDistribution = dictionnaire_joueur[joueurCommencePseudo]
                paquetCartes = [Carte(LISTE_NOMS_CARTES[n]) for n in random_liste_carte]

                if play10en10:
                    FenetreEnchere.enchere_cran = 10
                if playWithBelote:
                    FenetreEnchere.valeur_max = 200

                etat_partie = ETAT_PARTIE_ENCHERE
                distribution = True

        # ------------------------------ Gestion de la partie ------------------------------
        elif gelEcranCompteur == 0:
            if not distribution and not joueurSuivant:
                evt = reseau.regardeEvenementsNonFait()
                if evt is not None:
                    if evt[EVENT_TYPE] == EVT_BET:
                        joueur_evenement = dictionnaire_joueur[evt[EVENT_PSEUDO]]
                        nouvelleEnchere = evt[EVENT_CONTENU]
                        nouvelleAnnonce = nouvelleEnchere[PARAM_VALEUR]
                        if nouvelleAnnonce != PASSE:
                            nouvelleAnnonce = Enchere(int(nouvelleEnchere[PARAM_VALEUR]),
                                                      int(nouvelleEnchere[PARAM_COULEUR]),
                                                      joueur=joueur_evenement,
                                                      coinche=int(nouvelleEnchere[PARAM_COINCHE]))
                            encheres.append(nouvelleAnnonce)
                        joueurTour = joueur_evenement
                        joueur_evenement.derniereEnchere = nouvelleAnnonce
                        joueurSuivant = True

                    elif evt[EVENT_TYPE] == EVT_PLAY:
                        joueur_evenement = dictionnaire_joueur[evt[EVENT_PSEUDO]]
                        nouvelleCarte, belote = evt[EVENT_CONTENU]
                        pli.ajouteCarte(nouvelleCarte, joueur_evenement)
                        if joueur_evenement == monJoueur:
                            monJoueur.catres.remove(monJoueur.trouve_carte_nom(nouvelleCarte))
                        joueurSuivant = True
                        if int(belote) == 1:
                            belotesTour.append((joueur_evenement, pli.joueur_cartes[-1][1].couleur))
                        if len(pli.joueur_cartes) >= 4 and len(reseau.evenementsNonFait) == 0:
                            gelEcranCompteur = -1
                            continue

                    elif evt[EVENT_TYPE] == EVT_MESSAGE:
                        messages.nouveauMessage(evt[EVENT_CONTENU], evt[EVENT_PSEUDO])

            if action_possible and not reseau.evenementsNonFait:
                if clic_droit:
                    carte = monJoueur.clic_sur_cartes(x_souris, y_souris)
                    if carte is not None:
                        monJoueur.gere_cartes_selectionnees(carte)
                if clic_gauche:
                    if X_IMAGE_SAUVEGARE_BOUTON < x_souris < X_IMAGE_SAUVEGARE_BOUTON + LARGEUR_IMAGE_BOUTON \
                            and Y_IMAGE_SAUVEGARE_BOUTON < y_souris < (Y_IMAGE_SAUVEGARE_BOUTON + HAUTEUR_IMAGE_BOUTON):
                        reseau.sauvegarde()
                    elif X_IMAGE_RELOAD_BOUTON < x_souris < X_IMAGE_RELOAD_BOUTON + LARGEUR_IMAGE_BOUTON \
                            and Y_IMAGE_RELOAD_BOUTON < y_souris < (Y_IMAGE_RELOAD_BOUTON + HAUTEUR_IMAGE_BOUTON):
                        etat_partie = ETAT_PARTIE_PREPARATION
                        playWithBelote = False
                        play10en10 = False
                        reseau.id_actuelle = 0
                        listePseudoOrdreTour = sorted(listePseudoOrdreTour)
                        messages = Messages()
                        ecran_preparation.listeJoueurOrdreTour = listePseudoOrdreTour
                        continue
                    elif X_IMAGE_TAKE_BACK_BOUTON < x_souris < X_IMAGE_TAKE_BACK_BOUTON + LARGEUR_IMAGE_BOUTON \
                            and Y_IMAGE_TAKE_BACK_BOUTON < y_souris < (Y_IMAGE_TAKE_BACK_BOUTON + HAUTEUR_IMAGE_BOUTON):
                        reseau.take_back()
                    else:
                        r = messages.gere_clic(x_souris, y_souris)
                        if r is not None:
                            messages.nouveauMessage(r, monPseudo)
                            reseau.envoieMessage(r)
                        historiqueEnchere.gere_clic(x_souris, y_souris)
                        if joueurPremier in monEquipe.joueurs:
                            monEquipe.gere_clic(x_souris, y_souris)
                        else:
                            equipeAdverse.gere_clic(x_souris, y_souris)

                if etat_partie == ETAT_PARTIE_ENCHERE:
                    if clic_gauche:
                        r = fenetre_enchere.gere_clic(x_souris, y_souris)
                        if r is not None:
                            if isinstance(r, Enchere):
                                r.joueur = monJoueur
                                encheres.append(r)
                                joueurTour = monJoueur
                                reseau.envoieEnchere(r.valeur, r.couleur, r.coincher)
                            else:
                                reseau.envoieEnchere(PASSE)
                            monJoueur.derniereEnchere = r
                            joueurSuivant = True

                elif etat_partie == ETAT_PARTIE_JEU:
                    if joueurTour == monJoueur:
                        if clic_gauche:
                            r = monJoueur.clic_sur_cartes(x_souris, y_souris)
                            if r is not None:
                                if monJoueur.carte_possible_pour_pli(r, pli, encheres[-1]):
                                    belote = False
                                    if playWithBelote:
                                        c = r.couleur if encheres[-1].couleur == DICTIONNAIRE_COULEURS['TA'] else \
                                            encheres[-1].couleur
                                        if r.belote(c):
                                            if (monJoueur, c) in belotes:
                                                belote = True
                                            elif monJoueur.nb_carte_belote(c) == 2:
                                                if monJoueur.boutonCarteBelote is None or \
                                                        not monJoueur.boutonCarteBelote.parametre == r:
                                                    monJoueur.boutonCarteBelote = r.boutonBelote()
                                                    r = None
                                                elif monJoueur.boutonCarteBelote.selectionner:
                                                    belote = True
                                    if r is not None:
                                        pli.ajouteCarte(r, monJoueur)
                                        monJoueur.catres.remove(r)
                                        monJoueur.boutonCarteBelote = None
                                        monJoueur.boutonCarteBelote = None
                                        reseau.envoieCarte(r.nom, belote)
                                        joueurSuivant = True
                                        if belote:
                                            belotesTour.append((monJoueur, pli.joueur_cartes[-1][1].couleur))
                                        if len(pli.joueur_cartes) >= 4:
                                            gelEcranCompteur = -1
                                            continue

            while distribution or joueurSuivant:
                if distribution:
                    distribution = False
                    for joueur in dictionnaire_joueur.values():
                        joueur.derniereEnchere = None
                    listeJoueurOrdreTour = [joueurDistribution.joueurSuivant]
                    listeJoueurOrdreTour.append(listeJoueurOrdreTour[0].joueurSuivant)
                    listeJoueurOrdreTour.append(listeJoueurOrdreTour[1].joueurSuivant)
                    listeJoueurOrdreTour.append(joueurDistribution)
                    monJoueur.catres = []
                    for j in range(3):
                        i = listeJoueurOrdreTour.index(monJoueur)
                        if j < 1.5:
                            monJoueur.catres.extend(paquetCartes[j * 12 + i * 3:j * 12 + i * 3 + 3])
                        else:
                            monJoueur.catres.extend(paquetCartes[j * 12 + i * 3 - i:j * 12 + i * 3 + 2 - i])
                    monJoueur.prepare_cartes()
                    joueurPremier = joueurDistribution.joueurSuivant
                    joueurTour = joueurPremier
                    etat_partie = ETAT_PARTIE_ENCHERE
                    encheres = []
                    belotes = []
                    fenetre_enchere.nouvelle_enchere(encheres[-1] if len(encheres) > 0 else None, monEquipe,
                                                     joueurTour == monJoueur)

                if joueurSuivant:
                    joueurSuivant = False
                    if etat_partie == ETAT_PARTIE_ENCHERE:
                        if len(encheres) == 0 and joueurTour == joueurDistribution:
                            distribution = True
                            nouv = [paquetCartes[n] for n in random_liste_carte]
                            paquetCartes = nouv
                            joueurDistribution = joueurDistribution.joueurSuivant
                        elif len(encheres) > 0 \
                                and (joueurTour.joueurSuivant == encheres[-1].joueur or encheres[-1].coincher == 2):
                            etat_partie = ETAT_PARTIE_JEU
                            pli = Pli()
                            monEquipe.boutonPli.selectionner = False
                            equipeAdverse.boutonPli.selectionner = False
                            joueurTour = joueurDistribution.joueurSuivant
                            joueurPremier = joueurTour
                            joueurDistribution = joueurTour
                        else:
                            joueurTour = joueurTour.joueurSuivant
                            fenetre_enchere.nouvelle_enchere(encheres[-1] if len(encheres) > 0 else None, monEquipe,
                                                             joueurTour == monJoueur)
                    elif etat_partie == ETAT_PARTIE_JEU:
                        joueurTour = joueurTour.joueurSuivant
                        if joueurTour == joueurPremier:
                            joueurGangnant = pli.trouveJoueurGagnant(encheres[-1])
                            if joueurGangnant in monEquipe.joueurs:
                                monEquipe.plis.append(pli)
                            else:
                                equipeAdverse.plis.append(pli)
                            pli = Pli()
                            for x in belotesTour:
                                if x not in belotes:
                                    belotes.append(x)
                            belotesTour = []
                            if len(monJoueur.catres) == 0:
                                distribution = True
                                paquetCartes = []
                                if encheres[-1].joueur == monJoueur or encheres[-1].joueur == monCoequipier:
                                    paquetCartes = monEquipe.regroupe_cartes() + equipeAdverse.regroupe_cartes()
                                else:
                                    paquetCartes = equipeAdverse.regroupe_cartes() + monEquipe.regroupe_cartes()
                                paquetCartes = paquetCartes[15:len(paquetCartes)] + paquetCartes[0:15]
                                monEquipe.fin_tour(encheres[-1], joueurGangnant in monEquipe.joueurs, belotes)
                                equipeAdverse.fin_tour(encheres[-1], joueurGangnant in equipeAdverse.joueurs, belotes)
                            else:
                                joueurPremier = joueurGangnant
                                joueurTour = joueurPremier

        else:
            gelEcranCompteur -= 1
            if clic_gauche:
                if joueurPremier in monEquipe.joueurs:
                    e = monEquipe
                else:
                    e = equipeAdverse
                if not e.gere_clic(x_souris, y_souris) and not e.boutonPli.selectionner:
                    if gelEcranCompteur < 0:
                        gelEcranCompteur = 0

        # ----------------------------------- Affichage ------------------------------------
        if affichage:
            SCREEN.blit(IMAGE_FOND, (0, 0))
            SCREEN.blit(IMAGE_QUITTER_BOUTON, (X_IMAGE_QUITTER_BOUTON, Y_IMAGE_QUITTER_BOUTON))
            if etat_partie == ETAT_PARTIE_MISE_EN_PLACE:
                ecran_mise_en_place.affiche()
                if monPseudo != '':
                    monJoueur.affiche(etat_partie, True, None)
            elif etat_partie == ETAT_PARTIE_PREPARATION:
                ecran_preparation.affiche(playWithBelote, play10en10)
                for pseudo in listePseudoOrdreTour:
                    dictionnaire_joueur[pseudo].affiche(etat_partie, False,
                                                        dictionnaire_joueur[listePseudoOrdreTour[0]])
            else:
                SCREEN.blit(IMAGE_SAUVEGARE_BOUTON, (X_IMAGE_SAUVEGARE_BOUTON, Y_IMAGE_SAUVEGARE_BOUTON))
                SCREEN.blit(IMAGE_RELOAD_BOUTON, (X_IMAGE_RELOAD_BOUTON, Y_IMAGE_RELOAD_BOUTON))
                SCREEN.blit(IMAGE_TAKE_BACK_BOUTON, (X_IMAGE_TAKE_BACK_BOUTON, Y_IMAGE_TAKE_BACK_BOUTON))
                for joueur in dictionnaire_joueur.values():
                    joueur.affiche(etat_partie, joueurTour == joueur, joueurDistribution)
                pli.affiche()
                monEquipe.affiche(encheres[-1] if len(encheres) > 0 else None)
                equipeAdverse.affiche(encheres[-1] if len(encheres) > 0 else None)
                if etat_partie == ETAT_PARTIE_ENCHERE:
                    fenetre_enchere.affiche()
                elif etat_partie == ETAT_PARTIE_JEU:
                    for joueur, couleur in belotesTour:
                        joueur.afficheBelote((joueur, couleur) in belotes)
                messages.affiche()
                historiqueEnchere.affiche(encheres)

        pygame.display.update()
        pygame.time.Clock().tick(FPS)
