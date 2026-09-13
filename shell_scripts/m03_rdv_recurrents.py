#!/usr/bin/env python3
"""
M03 — Rendez-vous récurrents (ex: infirmière tous les matins).

Home Assistant (2026.8.2, vérifié sur la doc officielle le 14/08) ne
supporte PAS de champ `rrule` sur le service `calendar.create_event` —
c'est une demande d'évolution encore ouverte côté HA, pas un bug de ce
projet. Contournement : ce script stocke les règles de récurrence dans
www/rdv_recurrents.txt, et une automation HA
(m03_rdv_recurrents_creer_du_jour, packages/oblig_m03_ecran_msg/
m03_rdv_recurrents.yaml, tous les jours à 00:05) crée l'événement du jour
sur calendar.calendrier_local si le jour de la semaine correspond à une
règle. La toute première occurrence (le jour choisi dans le formulaire) est
créée immédiatement par aidant.html via calendar.create_event, comme un
RDV normal — ce script ne gère QUE les occurrences futures.

Format d'une ligne : id|joursCSV|HH:MM|note
  - id       : timestamp unix (identifiant unique de la règle)
  - joursCSV : jours cochés, ex "MO,TU,WE,TH,FR" (codes RRULE 2 lettres)
  - HH:MM    : heure (identique pour tous les jours de la règle)
  - note     : texte libre (<=60 car, contrôlé côté aidant.html ; les "|"
               éventuels sont remplacés par "-" côté client avant envoi)

Actions (argv[1]) :
  add <joursCSV> <heure> <note>  → ajoute une règle, imprime son id
  delete <id>                     → retire la règle correspondante
  list                             → imprime toutes les règles (1/ligne)
  today <jour_2_lettres>          → imprime "HH:MM|note" des règles du jour
"""
import sys
import time
from pathlib import Path

FILE = Path("/config/www/rdv_recurrents.txt")


def read_lines():
    if not FILE.exists():
        return []
    return [l.strip() for l in FILE.read_text(encoding="utf-8").splitlines() if l.strip()]


def write_lines(lines):
    FILE.parent.mkdir(parents=True, exist_ok=True)
    FILE.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")


def do_add(jours, heure, note):
    lines = read_lines()
    # 2026-09-13 : anti-doublon — recréer une règle identique (mêmes jours,
    # même heure, même note) ne doit PAS ajouter une 2e ligne : sinon
    # l'automation quotidienne créerait 2 fois chaque événement.
    for l in lines:
        parts = l.split("|", 3)
        if len(parts) == 4 and parts[1] == jours and parts[2] == heure and parts[3] == note:
            print(parts[0])  # renvoie l'id déjà existant
            return
    rule_id = str(int(time.time()))
    lines.append(f"{rule_id}|{jours}|{heure}|{note}")
    write_lines(lines)
    print(rule_id)


def do_delete(rule_id):
    lines = read_lines()
    lines = [l for l in lines if not l.startswith(rule_id + "|")]
    write_lines(lines)


def do_list():
    for l in read_lines():
        print(l)


def do_today(jour):
    for l in read_lines():
        parts = l.split("|", 3)
        if len(parts) != 4:
            continue
        _id, jours, heure, note = parts
        if jour in jours.split(","):
            print(f"{heure}|{note}")


def main():
    args = sys.argv[1:]
    action = args[0] if args else ""
    if action == "add" and len(args) >= 3:
        note = args[3] if len(args) > 3 else ""
        do_add(args[1], args[2], note)
    elif action == "delete" and len(args) >= 2:
        do_delete(args[1])
    elif action == "list":
        do_list()
    elif action == "today" and len(args) >= 2:
        do_today(args[1])
    else:
        print("Usage: m03_rdv_recurrents.py [add jours heure note|delete id|list|today jour]", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
