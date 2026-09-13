# 🧪 PROTOCOLE DE TEST — Modules M02/M04/M05 (simulation sans matériel)
*Créé le 2026-08-05*

> À utiliser avec la page dashboard `🧪 Tests Simulation` (voir `dashboard_test_simulation.yaml`).
> Avant de commencer : Développeur → Recharger la configuration YAML (pour que
> `m00_simulation.yaml`, `m02_inactivite.yaml`, `m04_sos.yaml`, `m05_capteur_lit.yaml` soient pris en compte).

---

## Liste des boutons fictifs et leur rôle

| Bouton (input_boolean) | Simule | Comportement |
|---|---|---|
| `sim_snzb06p_presence` | Radar SNZB-06P (présence salon) | Interrupteur classique — ON = présence détectée, OFF = personne absente/immobile |
| `sim_sos_bouton` | Bouton WOOX SOS | **Impulsion** — passe à ON puis repasse automatiquement à OFF après 2s (imite un vrai appui bouton) |
| `sim_lit_occupe` | Capteur Aqara sous matelas | Interrupteur classique — ON = quelqu'un est couché, OFF = lit vide |

## Entités à observer pendant les tests

| Entité | Signifie |
|---|---|
| `input_boolean.m02_alerte_active` | Alerte inactivité déclenchée (heures actives/sieste) |
| `input_boolean.m02_absence_hors_horaires_nuit` | Alerte absence nocturne anormale |
| `input_boolean.m04_sos_declenche` | SOS déclenché |
| `sensor.m02_etat_temporel` | État horaire courant calculé (`actif` / `sieste` / `nuit` / `transition`) |

---

## Scénarios à tester

### Scénario 1 — Inactivité en heures actives
1. Vérifier `input_boolean.module_inactivite` = ON.
2. Vérifier l'heure réelle est en tranche "active" (8h-12h ou 15h-19h) — sinon utiliser le scénario 2 ou 3 à la place, ou attendre.
3. Baisser `input_number.m02_seuil_alerte_min` à **1 min** (pour ne pas attendre 45 min).
4. Passer `sim_snzb06p_presence` sur OFF.
5. Attendre 5-6 minutes (le check tourne toutes les 5 min).
6. **Résultat attendu** : `m02_alerte_active` passe à ON + notification visible.
7. Repasser `sim_snzb06p_presence` sur ON → `m02_alerte_active` doit repasser à OFF automatiquement (reset).
8. **Ne pas oublier de remettre `m02_seuil_alerte_min` à 45 après le test.**

### Scénario 2 — Sieste avec lit occupé (pas d'alerte attendue)
1. Doit être exécuté entre 12h et 15h (ou modifier temporairement l'heure système si besoin de tester hors plage — non recommandé, préférer tester au bon moment).
2. Passer `sim_lit_occupe` sur ON.
3. Passer `sim_snzb06p_presence` sur OFF.
4. Attendre 5-10 min.
5. **Résultat attendu** : aucune alerte ne se déclenche (`m02_alerte_active` reste OFF) — c'est le comportement normal, la sieste au lit n'est pas une anomalie.

### Scénario 3 — Absence nocturne anormale
1. Doit être exécuté après 23h (ou ajuster temporairement l'heure — même remarque que scénario 2).
2. Passer `sim_lit_occupe` sur OFF.
3. Passer `sim_snzb06p_presence` sur OFF.
4. Attendre 5-6 min.
5. **Résultat attendu** : `m02_absence_hors_horaires_nuit` passe à ON + notification.

### Scénario 4 — SOS
1. Vérifier `input_boolean.module_sos` = ON.
2. Passer `sim_sos_bouton` sur ON (il repassera seul à OFF après 2s, c'est normal).
3. **Résultat attendu** : `m04_sos_declenche` passe à ON immédiatement + notification "🚨 SOS déclenché".
4. Pour réinitialiser : repasser manuellement `input_boolean.m04_sos_declenche` sur OFF.

---

## Après les tests

- Remettre `input_number.m02_seuil_alerte_min` à sa valeur normale (45 min) si modifiée.
- Noter les résultats ici ou dans `dependances.md` (colonne statut des modules M02/M04/M05).
- Si un scénario échoue, ne pas corriger "à l'aveugle" — décrire précisément ce qui s'est passé vs attendu avant de modifier le YAML.

---

*Ce protocole couvre uniquement la logique en simulation. Une fois le vrai matériel pairé, un nouveau test de couverture physique (déplacement réel dans la pièce) sera nécessaire — voir `CAHIER_DES_CHARGES.md` §7.*
