#!/usr/bin/env python3
"""
M31 — Liste les photos disponibles pour le diaporama kiosk.

Usage :
  m31_photos_liste.py

Sortie stdout : une ligne par photo, format "source|nom_fichier"
  source = "www"   → /config/www/photos_famille/<nom> (dépôt manuel Samba,
                      mécanisme historique, servi SANS authentification
                      sous /local/photos_famille/<nom>)
  source = "media" → /media/photos_famille/<nom> (upload via le bouton
                      "Choisir des photos" de config.html, 2026-08-15 —
                      dossier "média local" de HA, servi AVEC
                      authentification HA sous /media/local/photos_famille/<nom>)

Les deux sources sont scannées et concaténées (www d'abord, puis media),
chacune triée par nom de fichier (insensible à la casse). Rien si les deux
dossiers sont vides ou absents — kiosk.html affiche alors le placeholder
"Pas de photo déposée".

Extensions acceptées : .jpg .jpeg .png .gif (insensible à la casse).

annotations_log:
- Création (2026-08-15) : remplace le mécanisme à photo unique fixe
  (photo_actuelle.jpg) par une vraie liste dynamique (source unique : www).
- Révision 2026-08-15 (même jour) : ajout de la source "media" — nouveau
  bouton d'upload dans config.html (POST /api/media_source/local_source/upload,
  endpoint interne HA). Les deux sources coexistent : www reste utilisable
  pour qui préfère déposer via Samba, media pour l'upload simple depuis
  config.html. Format de sortie changé de "nom_fichier" à "source|nom_fichier"
  en conséquence — kiosk.html adapté (refreshPhotoList()/renderPhoto()).
"""
import os

DOSSIER_WWW = "/config/www/photos_famille"
DOSSIER_MEDIA = "/media/photos_famille"
EXTENSIONS = (".jpg", ".jpeg", ".png", ".gif")


def lister(dossier):
    if not os.path.isdir(dossier):
        return []
    try:
        fichiers = [
            f for f in os.listdir(dossier)
            if f.lower().endswith(EXTENSIONS) and os.path.isfile(os.path.join(dossier, f))
        ]
    except OSError:
        return []
    fichiers.sort(key=str.lower)
    return fichiers


def main():
    for f in lister(DOSSIER_WWW):
        print("www|" + f)
    for f in lister(DOSSIER_MEDIA):
        print("media|" + f)


if __name__ == "__main__":
    main()
