# coding: utf-8

from commun import *
from flask import Flask, request, jsonify
import random
import json

MODE_SAUVEGARDE = False
FICHIER_SAUVEGARDE = 'sauvegarde.json'

app = Flask(__name__)


class Evenement():
    id_max = 1

    def __init__(self, pseudo, type, contenu=None):
        self.id = Evenement.id_max
        Evenement.id_max += 1
        self.pseudo = pseudo
        self.type = type
        self.contenu = contenu
        # print(f'--> Event : {self.id}    : {self.type}')

    def dump(self):
        return {EVENT_ID: self.id, EVENT_PSEUDO: self.pseudo, EVENT_TYPE: self.type, EVENT_CONTENU: self.contenu}


liste_pseudos_joueurs = []
liste_events = []
liste_joueurs_team = []
listeJoueursClasses = []

if MODE_SAUVEGARDE:
    with open(FICHIER_SAUVEGARDE, 'r') as fichier:
        dic_sauvegarde = json.load(fichier)
        liste_pseudos_joueurs = dic_sauvegarde['liste_pseudos_joueurs']
        liste_joueurs_team = dic_sauvegarde['liste_joueurs_team']
        listeJoueursClasses = dic_sauvegarde['listeJoueursClasses']
        if len(dic_sauvegarde['events']) > 0:
            for dic_event in dic_sauvegarde['events']:
                event = Evenement(None, None, None)
                event.__dict__.update(dic_event)
                liste_events.append(event)
            Evenement.id_max = len(liste_events) + 1


@app.route(f'/coinche/{EVT_SAUVEGARDE}')
def sauvegarde():
    dic = {'liste_pseudos_joueurs': liste_pseudos_joueurs,
           'liste_joueurs_team': liste_joueurs_team,
           'listeJoueursClasses': listeJoueursClasses,
           'events': [event.__dict__ for event in liste_events]}
    with open(FICHIER_SAUVEGARDE, "w") as fichier:
        json.dump(dic, fichier)
    return str(1)


@app.route(f'/coinche/{EVT_LOGIN}')
def login():
    pseudo = request.args.get(PARAM_PSEUDO)
    # print(pseudo)
    if len(liste_pseudos_joueurs) > 3:
        return str(0)
    if pseudo not in liste_pseudos_joueurs:
        liste_pseudos_joueurs.append(pseudo)
    liste_events.append(Evenement(pseudo, EVT_LOGIN))
    return str(1)


@app.route(f'/coinche/{EVT_TEAM}')
def team():
    pseudo = request.args.get(PARAM_PSEUDO)
    pseudo2 = request.args.get(PARAM_PSEUDO2)
    # print(f'pseudo : {pseudo}, pseudo2 : {pseudo2}')
    if pseudo in liste_pseudos_joueurs and pseudo2 in liste_pseudos_joueurs:
        l = []
        for team in liste_joueurs_team:
            l.extend(team)
        if pseudo not in l and pseudo2 not in l:
            liste_joueurs_team.append([pseudo, pseudo2])
            liste_events.append(Evenement(pseudo, EVT_TEAM, pseudo2))
            return str(1)
    return str(0)


@app.route(f'/coinche/{EVT_BET}')
def bet():
    pseudo = request.args.get(PARAM_PSEUDO)
    valeur = request.args.get(PARAM_VALEUR)
    couleur = request.args.get(PARAM_COULEUR)
    coinche = request.args.get(PARAM_COINCHE)
    # print(f'pseudo : {pseudo}, valeur : {valeur}, couleur : {couleur}, coinche : {coinche}')
    liste_events.append(Evenement(pseudo, EVT_BET, {PARAM_VALEUR: valeur, PARAM_COULEUR: couleur, PARAM_COINCHE: coinche}))
    return str(1)


@app.route(f'/coinche/{EVT_PLAY}')
def play():
    pseudo = request.args.get(PARAM_PSEUDO)
    carte = request.args.get(PARAM_CARTE)
    # print(f'pseudo : {pseudo}, carte : {carte}')
    liste_events.append(Evenement(pseudo, EVT_PLAY, carte))
    return str(1)

@app.route(f'/coinche/{EVT_MESSAGE}')
def message():
    pseudo = request.args.get(PARAM_PSEUDO)
    msg = request.args.get(PARAM_MSG)
    # print(f'pseudo : {pseudo}, msg : {msg}')
    liste_events.append(Evenement(pseudo, EVT_MESSAGE, msg))
    return str(1)

@app.route(f'/coinche/{PLAYER_LIST}')
def playerList():
    if len(listeJoueursClasses) == 0 and len(liste_joueurs_team) == 2:
        random.shuffle(liste_joueurs_team)
        random.shuffle(liste_joueurs_team[0])
        random.shuffle(liste_joueurs_team[1])
        listeJoueursClasses.extend([liste_joueurs_team[0][0], liste_joueurs_team[1][0],
                                    liste_joueurs_team[0][1], liste_joueurs_team[1][1]])
        # print(f'listeJoueurs : {listeJoueursClasses}')
    return jsonify(listeJoueursClasses)


@app.route(f'/coinche/{EVENT}')
def event():
    pseudo = request.args.get(PARAM_PSEUDO)
    id_str = request.args.get(PARAM_ID)
    # print(f'pseudo : {pseudo}, id : {id_str}')
    l = []
    if id_str is not None:
        try:
            id = int(id_str)
        except:
            pass
        else:
            for i in range(id, len(liste_events)):
                event = liste_events[i]
                if event.pseudo != pseudo or id == 0:
                    l.append(event.dump())
    return jsonify(l)


if __name__ == '__main__':
    random_liste_carte = [i for i in range(32)]
    random.shuffle(random_liste_carte)
    liste_events.append(Evenement(None, EVT_DEAL, random_liste_carte))
    app.run(host='0.0.0.0', port=12800)
