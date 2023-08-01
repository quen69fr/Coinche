# coding: utf-8

import requests
import time
from commun import *


NB_MAX_REJEUX = 10
DELAY_SERVEUR_REQUESTS = 0.2


class ReseauClient:
    def __init__(self):
        self.pseudoJoueur = None
        self.adresse_ip = None
        self.port = '12800'
        self.id_actuelle = 0
        self.evenementsNonFait = []
        self.time_last_request = 0

    def envoie_au_serveur(self, type, dicParametre={}):
        lien = f'http://{self.adresse_ip}:{self.port}/coinche/{type}'
        if len(dicParametre) != 0:
            lien += '?'
            for cle, valeur in dicParametre.items():
                lien += f'{cle}={valeur}&'
            lien = lien[:-1]
        i = 0
        while i < NB_MAX_REJEUX:
            try:
                r = requests.get(lien).json()
            except:
                i += 1
            else:
                return r

    def login(self, pseudo):
        self.envoie_au_serveur(EVT_LOGIN, {PARAM_PSEUDO: pseudo})
        self.pseudoJoueur = pseudo

    def sauvegarde(self):
        self.envoie_au_serveur(EVT_SAUVEGARDE)

    def take_back(self):
        self.envoie_au_serveur(EVT_TAKE_BACK)

    def playerList(self):
        return self.envoie_au_serveur(PLAYER_LIST)

    def regardeEvenementsNonFait(self):
        if len(self.evenementsNonFait) == 0:
            if time.time() - self.time_last_request > DELAY_SERVEUR_REQUESTS:
                reponse = self.envoie_au_serveur(EVENT, {PARAM_PSEUDO: self.pseudoJoueur, PARAM_ID: self.id_actuelle})
                self.time_last_request = time.time()
                if len(reponse) != 0:
                    self.id_actuelle = reponse[-1][EVENT_ID]
                    self.evenementsNonFait = reponse
        else:
            evt = self.evenementsNonFait[0]
            self.evenementsNonFait.remove(evt)
            return evt

        return None

    def team(self, pseudoCoequipier):
        reponse = self.envoie_au_serveur(EVT_TEAM, {PARAM_PSEUDO: self.pseudoJoueur, PARAM_PSEUDO2: pseudoCoequipier})
        if reponse == 1:
            return True
        return False

    def envoieMessage(self, message):
        self.envoie_au_serveur(EVT_MESSAGE, {PARAM_PSEUDO: self.pseudoJoueur, PARAM_MSG: message})

    def envoieCarte(self, nomCarte, belote):
        self.envoie_au_serveur(EVT_PLAY, {PARAM_PSEUDO: self.pseudoJoueur, PARAM_CARTE: nomCarte,
                                          PARAM_BELOTE: 1 if belote else 0})

    def envoieEnchere(self, valeur, couleur=None, coinche=None):
        self.envoie_au_serveur(EVT_BET, {PARAM_PSEUDO: self.pseudoJoueur, PARAM_VALEUR: valeur,
                                         PARAM_COULEUR: couleur, PARAM_COINCHE: coinche})

    def envoieBelotte(self):
        self.envoie_au_serveur(EVT_BELOTE, {PARAM_PSEUDO: self.pseudoJoueur})

    def envoie10en10(self):
        self.envoie_au_serveur(EVT_10_EN_10, {PARAM_PSEUDO: self.pseudoJoueur})

    def envoiePremierJoueur(self):
        self.envoie_au_serveur(EVT_PREMIER_JOUEUR, {PARAM_PSEUDO: self.pseudoJoueur})

    def envoieStart(self):
        self.envoie_au_serveur(EVT_START, {PARAM_PSEUDO: self.pseudoJoueur})
