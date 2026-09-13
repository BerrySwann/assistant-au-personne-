#!/usr/bin/env python3
# ╭──────────────────────────────────────────────────────────────────────────╮
# │   M31 — TÉLÉVERSEMENT D'UNE PHOTO SANS DROITS ADMIN (par morceaux)      │
# ╰──────────────────────────────────────────────────────────────────────────╯
# Créé le 2026-08-15 (suite), pour photos.html (page dédiée protégée par PIN).
#
# Contourne volontairement une restriction native de Home Assistant : la
# route officielle d'upload média (POST /api/media_source/local_source/upload)
# contient dans son code source (local_source.py) :
#     if not request["hass_user"].is_admin: raise Unauthorized()
# → réservée aux comptes administrateur. Un compte "aidant" PIN-gated mais
# non-admin reçoit un 401, quel que soit son token (confirmé en direct le
# 15/08 : le compte non-admin du téléphone échouait UNIQUEMENT sur cet
# endpoint, alors que la galerie et la suppression — via shell_command,
# jamais admin-only — fonctionnaient déjà normalement avec le même token).
#
# Plutôt que d'exiger le statut admin pour chaque compte qui doit pouvoir
# envoyer une photo (donnerait accès à toute la config HA, pas juste aux
# photos), ce script écrit le fichier directement sur disque via
# shell_command — même logique que m31_photos_supprimer.py, qui contourne
# déjà une autre limitation native (suppression média WebSocket-only).
#
# Pourquoi en plusieurs morceaux (3 étapes debut/chunk/fin) plutôt qu'un
# seul appel avec le fichier entier en base64 : shell_command exécute la
# commande comme une vraie ligne de commande système (Jinja → argv), qui a
# une taille limite (ARG_MAX, souvent ~2 Mo sur Linux, parfois moins en
# conteneur). Une photo de téléphone (souvent 3-10 Mo, donc 4-14 Mo une
# fois encodée en base64) dépasserait cette limite en un seul appel.
# Seuil réel mesuré en direct sur cette instance HA (2026-08-15, via curl) :
# 100 000 caractères/appel passe, 150 000 échoue (HTTP 500, "Server got
# itself in trouble"). Solution : le texte base64 est découpé côté page
# (photos.html, morceaux de 50 000 caractères, marge de sécurité) et
# envoyé par appels successifs, qui
# s'accumulent dans un fichier temporaire texte (pas de décodage tant que
# tous les morceaux ne sont pas reçus) ; la dernière étape décode le tout
# et écrit l'image finale.
#
# Sécurité : le nom de fichier reçu est réduit à os.path.basename() avant
# toute opération, rejeté s'il diffère de l'original (protège contre un
# nom contenant "../" ou un chemin absolu) — même garde-fou que
# m31_photos_supprimer.py. Écrit uniquement dans /media/photos_famille/
# (jamais /config/www/, qui reste réservé au dépôt manuel Samba).
#
# Sortie (une ligne, lue par photos.html) :
#   OK        → étape réussie (debut/chunk/fin)
#   ERROR: .. → argument invalide ou échec disque

import base64
import os
import sys

DOSSIER_MEDIA = "/media/photos_famille"
DOSSIER_TEMP = "/tmp"


def nom_valide(nom):
    nom_sain = os.path.basename(nom)
    if not nom_sain or nom_sain != nom or nom_sain in (".", ".."):
        return None
    return nom_sain


def chemin_temp(nom_sain):
    return os.path.join(DOSSIER_TEMP, "m31_upload__" + nom_sain + ".b64")


def main():
    if len(sys.argv) < 3:
        print("ERROR: arguments manquants (etape, nom)")
        return

    etape = sys.argv[1].strip()
    nom = sys.argv[2].strip()
    donnee = sys.argv[3] if len(sys.argv) > 3 else ""

    nom_sain = nom_valide(nom)
    if not nom_sain:
        print("ERROR: nom de fichier invalide")
        return

    temp = chemin_temp(nom_sain)

    if etape == "debut":
        try:
            with open(temp, "w") as f:
                f.write("")
            print("OK")
        except OSError as e:
            print("ERROR: " + str(e))
        return

    if etape == "chunk":
        try:
            with open(temp, "a") as f:
                f.write(donnee)
            print("OK")
        except OSError as e:
            print("ERROR: " + str(e))
        return

    if etape == "fin":
        if not os.path.isfile(temp):
            print("ERROR: aucun envoi en cours pour ce fichier")
            return
        try:
            with open(temp, "r") as f:
                b64_complet = f.read()
            contenu = base64.b64decode(b64_complet)
            chemin_final = os.path.join(DOSSIER_MEDIA, nom_sain)
            with open(chemin_final, "wb") as f:
                f.write(contenu)
            os.remove(temp)
            print("OK")
        except (OSError, ValueError) as e:
            print("ERROR: " + str(e))
        return

    print("ERROR: etape invalide")


if __name__ == "__main__":
    main()
