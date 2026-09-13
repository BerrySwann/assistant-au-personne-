#!/usr/bin/env python3
"""M32 - Musique : gestion des liens YouTube de la liste musique.

Actions (argument 1, argument 2 optionnel) :
  list          : imprime les liens numerotes, un par ligne (format : NN|url)
  add <url>     : ajoute <url> en fin de liste (99 max, pas de doublon)
  delete <num>  : supprime la ligne numero <num> (1 a 99)

Fichier : www/musique_liens.txt - une URL YouTube par ligne.
Le numero affiche (01, 02, ...) correspond a la position dans le fichier ;
c'est ce numero qu'on saisit pour supprimer une ligne.

Cree le 2026-09-13 (systeme musique M32, modele : m34_liens_youtube.py).
"""

import os
import re
import sys

FILE = os.environ.get("M32_MUSIQUE_FILE", "/config/www/musique_liens.txt")
MAX = 99
URL_RE = re.compile(r"^https?://(www\.|m\.)?(youtube\.com|youtu\.be)/", re.I)


def read_lines():
    if not os.path.exists(FILE):
        return []
    with open(FILE, encoding="utf-8") as handle:
        return [line.strip() for line in handle if line.strip()]


def write_lines(lines):
    os.makedirs(os.path.dirname(FILE), exist_ok=True)
    with open(FILE, "w", encoding="utf-8") as handle:
        handle.write("\n".join(lines) + "\n")


def main():
    action = sys.argv[1] if len(sys.argv) > 1 else ""
    arg = sys.argv[2].strip() if len(sys.argv) > 2 else ""

    lines = read_lines()

    if action == "list":
        for i, url in enumerate(lines, 1):
            print(f"{i:02d}|{url}")
        if not lines:
            print("(liste vide)")

    elif action == "add":
        if not arg:
            print("ERREUR: lien vide")
            return 1
        if not URL_RE.match(arg):
            print("ERREUR: lien YouTube invalide (youtube.com ou youtu.be)")
            return 1
        if arg in lines:
            print("ERREUR: lien deja present")
            return 1
        if len(lines) >= MAX:
            print(f"ERREUR: liste pleine ({MAX} max) — supprime des lignes d'abord")
            return 1
        lines.append(arg)
        write_lines(lines)
        print(f"OK: ajoute #{len(lines):02d}")

    elif action == "delete":
        try:
            num = int(arg)
        except ValueError:
            print("ERREUR: numero invalide")
            return 1
        if num < 1 or num > len(lines):
            print(f"ERREUR: numero hors plage (1 a {len(lines)})")
            return 1
        removed = lines.pop(num - 1)
        write_lines(lines)
        print(f"OK: supprime #{num:02d} ({removed})")

    else:
        print("actions: list | add <url> | delete <num>")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
