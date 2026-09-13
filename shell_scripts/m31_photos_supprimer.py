#!/usr/bin/env python3
# ╭──────────────────────────────────────────────────────────────────────────╮
# │   M31 — SUPPRESSION D'UNE PHOTO (www ou media)                          │
# ╰──────────────────────────────────────────────────────────────────────────╯
# Créé le 2026-08-15, pour photos.html (page dédiée protégée par PIN).
#
# Contourne volontairement la limitation documentée de HA : le service natif
# de suppression média (media_source/local_source/remove) n'existe qu'en
# WebSocket, pas en REST (voir m31_photos.yaml). Plutôt que d'implémenter un
# client WebSocket côté navigateur (complexe, jamais fait dans ce projet),
# ce script supprime directement le fichier sur disque via shell_command —
# même pattern déjà utilisé et éprouvé pour m31_photos_liste.py.
#
# Sécurité : le nom de fichier reçu est réduit à os.path.basename() avant
# toute opération, et rejeté s'il diffère de l'original (protège contre un
# nom contenant "../" ou un chemin absolu). La source ne peut être que
# "www" ou "media" (mappée en dur vers les 2 dossiers connus).
#
# Sortie (une ligne, lue par photos.html) :
#   OK        → fichier supprimé
#   NOTFOUND  → fichier déjà absent (pas une erreur bloquante côté page)
#   ERROR: .. → argument invalide ou échec de suppression

import os
import sys

DOSSIER_WWW = "/config/www/photos_famille"
DOSSIER_MEDIA = "/media/photos_famille"


def main():
    if len(sys.argv) < 3:
        print("ERROR: arguments manquants (source, nom_fichier)")
        return

    source = sys.argv[1].strip()
    nom = sys.argv[2].strip()

    if source == "www":
        dossier = DOSSIER_WWW
    elif source == "media":
        dossier = DOSSIER_MEDIA
    else:
        print("ERROR: source invalide")
        return

    nom_sain = os.path.basename(nom)
    if not nom_sain or nom_sain != nom or nom_sain in (".", ".."):
        print("ERROR: nom de fichier invalide")
        return

    chemin = os.path.join(dossier, nom_sain)
    if not os.path.isfile(chemin):
        print("NOTFOUND")
        return

    try:
        os.remove(chemin)
        print("OK")
    except OSError as e:
        print("ERROR: " + str(e))


if __name__ == "__main__":
    main()
