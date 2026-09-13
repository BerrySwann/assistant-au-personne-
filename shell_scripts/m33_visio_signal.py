#!/usr/bin/env python3
# ╭──────────────────────────────────────────────────────────────────────────╮
# │   M33 — SIGNALISATION VISIO (WebRTC) SANS DROITS ADMIN                   │
# ╰──────────────────────────────────────────────────────────────────────────╯
# Créé le 2026-08-16, pour la visioconférence maison (kiosk.html <-> aidant.html).
#
# POURQUOI CE SCRIPT
# Une visio WebRTC a besoin d'un "serveur de signalisation" : un canal par
# lequel les deux correspondants s'échangent leurs descriptions de session
# (SDP) et leurs candidats réseau (ICE) AVANT de pouvoir se parler en direct.
# Une fois connectés, l'image et le son passent en direct d'un appareil à
# l'autre — ce canal ne sert QUE pendant les quelques secondes d'établissement.
#
# Home Assistant sait déjà faire ça nativement : les événements du WebSocket
# (fire_event / subscribe_events) transportent sans problème un SDP de 4 Ko
# (testé en direct le 16/08). MAIS ces deux commandes sont réservées aux
# comptes ADMINISTRATEUR. Or tout l'intérêt du système de droits construit la
# veille (voir M10) est justement que les aidants soient des comptes NON-admin.
# Les rendre admin pour pouvoir passer un appel viderait ce travail de son sens.
#
# D'où ce contournement par shell_command — exactement la même approche que
# m31_photos_televerser.py, déjà éprouvée en non-admin avec de gros volumes.
#
# PRINCIPE
# Une boîte aux lettres par destinataire, sous forme de fichier texte :
#   /tmp/m33_visio_signal__kiosk.txt   <- messages À DESTINATION du kiosk
#   /tmp/m33_visio_signal__aidant.txt  <- messages À DESTINATION de l'aidant
# Chaque message est une ligne encodée en base64 (voir plus bas). La lecture
# est DESTRUCTRICE : on renvoie les messages en attente puis on vide la boîte,
# ce qui évite de retraiter deux fois la même offre ou le même candidat.
#
# POURQUOI DU BASE64
# Le contenu transporté est du JSON contenant du SDP : guillemets, sauts de
# ligne, caractères spéciaux. shell_command passe ses arguments par une vraie
# ligne de commande système — un tel contenu brut y serait massacré (ou pire,
# interprété). Le base64 ne contient que des caractères sûrs. La page encode
# avant d'envoyer, décode après avoir lu.
# Taille : un SDP fait ~4 Ko, soit ~5,5 Ko en base64 — très en dessous de la
# limite mesurée sur cette instance (100 000 caractères par appel, cf.
# m31_photos_televerser.py). Aucun découpage nécessaire ici.
#
# SÉCURITÉ
# Le rôle reçu est comparé à une liste blanche stricte (kiosk / aidant) avant
# toute opération sur un chemin — impossible d'écrire ailleurs via un rôle
# contenant "../" ou un chemin absolu. Les fichiers vivent dans /tmp, donc
# disparaissent au redémarrage : aucune trace persistante d'un appel.
#
# Sortie (lue par kiosk.html / aidant.html) :
#   envoyer  -> "OK"
#   lire     -> les messages en attente, un par ligne (vide si aucun)
#   purger   -> "OK"
#   erreur   -> "ERROR: <message>"

import os
import sys

DOSSIER = "/tmp"
ROLES_AUTORISES = ("kiosk", "aidant")
# Garde-fou : au-delà, on considère que la boîte n'est plus relevée (page
# fermée brutalement en pleine négociation) et on repart de zéro, plutôt que
# de laisser un fichier grossir indéfiniment.
TAILLE_MAX = 400_000


def chemin_boite(role):
    return os.path.join(DOSSIER, "m33_visio_signal__" + role + ".txt")


def role_valide(role):
    return role if role in ROLES_AUTORISES else None


def action_envoyer(destinataire, donnee):
    if not donnee:
        print("ERROR: message vide")
        return
    boite = chemin_boite(destinataire)
    try:
        if os.path.isfile(boite) and os.path.getsize(boite) > TAILLE_MAX:
            os.remove(boite)
        with open(boite, "a") as f:
            f.write(donnee.strip() + "\n")
        print("OK")
    except OSError as e:
        print("ERROR: " + str(e))


def action_lire(destinataire):
    boite = chemin_boite(destinataire)
    if not os.path.isfile(boite):
        return  # aucune sortie = aucun message en attente
    try:
        with open(boite, "r") as f:
            contenu = f.read()
        # Lecture destructrice : on vide AVANT d'afficher, pour qu'un appel
        # concurrent ne relise pas les mêmes messages.
        os.remove(boite)
        sys.stdout.write(contenu)
    except OSError as e:
        print("ERROR: " + str(e))


def action_purger():
    try:
        for role in ROLES_AUTORISES:
            boite = chemin_boite(role)
            if os.path.isfile(boite):
                os.remove(boite)
        print("OK")
    except OSError as e:
        print("ERROR: " + str(e))


def main():
    if len(sys.argv) < 2:
        print("ERROR: action manquante")
        return

    action = sys.argv[1].strip()

    if action == "purger":
        action_purger()
        return

    if len(sys.argv) < 3:
        print("ERROR: destinataire manquant")
        return

    destinataire = role_valide(sys.argv[2].strip())
    if not destinataire:
        print("ERROR: destinataire invalide")
        return

    if action == "envoyer":
        action_envoyer(destinataire, sys.argv[3] if len(sys.argv) > 3 else "")
        return

    if action == "lire":
        action_lire(destinataire)
        return

    print("ERROR: action invalide")


if __name__ == "__main__":
    main()
