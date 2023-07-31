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


liste_events = []

if MODE_SAUVEGARDE:
    with open(FICHIER_SAUVEGARDE, 'r') as fichier:
        dic_sauvegarde = json.load(fichier)
        if len(dic_sauvegarde['events']) > 0:
            for dic_event in dic_sauvegarde['events']:
                event = Evenement(None, None, None)
                event.__dict__.update(dic_event)
                liste_events.append(event)
            Evenement.id_max = len(liste_events) + 1


@app.route(f'/coinche/{EVT_SAUVEGARDE}')
def sauvegarde():
    dic = {'events': [event.__dict__ for event in liste_events]}
    with open(FICHIER_SAUVEGARDE, "w") as fichier:
        json.dump(dic, fichier)
    return str(1)


@app.route(f'/coinche/{EVT_LOGIN}')
def login():
    pseudo = request.args.get(PARAM_PSEUDO)
    liste_events.append(Evenement(pseudo, EVT_LOGIN))
    return str(1)


@app.route(f'/coinche/{EVT_TEAM}')
def team():
    pseudo = request.args.get(PARAM_PSEUDO)
    pseudo2 = request.args.get(PARAM_PSEUDO2)
    # print(f'pseudo : {pseudo}, pseudo2 : {pseudo2}')
    liste_events.append(Evenement(pseudo, EVT_TEAM, pseudo2))
    return str(0)


@app.route(f'/coinche/{EVT_BELOTE}')
def belote():
    pseudo = request.args.get(PARAM_PSEUDO)
    # print(f'pseudo : {pseudo}, msg : {msg}')
    liste_events.append(Evenement(pseudo, EVT_BELOTE))
    return str(1)


@app.route(f'/coinche/{EVT_PREMIER_JOUEUR}')
def premier_joueur():
    pseudo = request.args.get(PARAM_PSEUDO)
    # print(f'pseudo : {pseudo}, msg : {msg}')
    liste_events.append(Evenement(pseudo, EVT_PREMIER_JOUEUR))
    return str(1)


@app.route(f'/coinche/{EVT_START}')
def start():
    pseudo = request.args.get(PARAM_PSEUDO)
    # print(f'pseudo : {pseudo}, msg : {msg}')
    liste_events.append(Evenement(pseudo, EVT_START))
    return str(1)


@app.route(f'/coinche/{EVT_10_EN_10}')
def e10_en_10():
    pseudo = request.args.get(PARAM_PSEUDO)
    # print(f'pseudo : {pseudo}, msg : {msg}')
    liste_events.append(Evenement(pseudo, EVT_10_EN_10))
    return str(1)


@app.route(f'/coinche/{EVT_BET}')
def bet():
    pseudo = request.args.get(PARAM_PSEUDO)
    valeur = request.args.get(PARAM_VALEUR)
    couleur = request.args.get(PARAM_COULEUR)
    coinche = request.args.get(PARAM_COINCHE)
    # print(f'pseudo : {pseudo}, valeur : {valeur}, couleur : {couleur}, coinche : {coinche}')
    liste_events.append(
        Evenement(pseudo, EVT_BET, {PARAM_VALEUR: valeur, PARAM_COULEUR: couleur, PARAM_COINCHE: coinche}))
    return str(1)


@app.route(f'/coinche/{EVT_PLAY}')
def play():
    pseudo = request.args.get(PARAM_PSEUDO)
    carte = request.args.get(PARAM_CARTE)
    belote_ = request.args.get(PARAM_BELOTE)
    # print(f'pseudo : {pseudo}, carte : {carte}')
    liste_events.append(Evenement(pseudo, EVT_PLAY, [carte, belote_]))
    return str(1)


@app.route(f'/coinche/{EVT_MESSAGE}')
def message():
    pseudo = request.args.get(PARAM_PSEUDO)
    msg = request.args.get(PARAM_MSG)
    # print(f'pseudo : {pseudo}, msg : {msg}')
    liste_events.append(Evenement(pseudo, EVT_MESSAGE, msg))
    return str(1)


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
