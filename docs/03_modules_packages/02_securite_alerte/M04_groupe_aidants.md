# M04-GROUPE — Envoi alertes aux aidants

> Fiche rédigée le 2026-08-11 à partir de `raspi/packages/m04_groupe_aidants.yaml` (local).
> Source live : `Z:\packages\m04_groupe_aidants.yaml`.

## Rôle
Réécrit le 2026-08-05 (v2) : abandon des groupes natifs HA « Aides > Groupe » (jugés trop cachés dans l'UI par l'utilisateur, cf. retour direct). À la place, la liste des destinataires SOS est calculée **dynamiquement** à partir des cases à cocher `input_boolean.m04_proximite_aidant_N` définies dans `packages/m04_gestion_aidants.yaml` — visibles et modifiables sur le dashboard Configuration, sans passer par un menu HA caché.
- Le script `m04_envoyer_alerte_sos` notifie les seuls aidants de proximité cochés (template Jinja : filtre des `input_boolean` sur `on` → liste des `person.x` correspondants).
- Le script `m04_envoyer_alerte_moderee` notifie **tous** les aidants (cochés ou non), avec titre/message passés en paramètres de script.

⚠️ Les `person.x` sont des **comptes FICTIFS** confirmés par l'utilisateur le 2026-08-05 — à remplacer par les vrais entity_id une fois les vrais aidants inscrits dans HA (Paramètres > Personnes + appli Companion pour que `notify.send_message` puisse réellement les notifier).

## Dépendances
| Élément | Source | Statut |
|:--------|:-------|:-------|
| `input_boolean.m04_proximite_aidant_1` … `_7` | Module M04-gestion (m04_gestion_aidants.yaml) | Détermine les destinataires du SOS (cases cochées) |
| `person.aidant_1_admin_ok` … `person.aidant_7_hs` | HA Paramètres > Personnes | ⚠️ Comptes fictifs de test - appli Companion requise pour les notifications réelles |
| `notify.send_message` (cible « person ») | HA | ⚠️ Nécessite HA récent - sinon repasser sur l'ancien mécanisme (`notify.mobile_app_xxx` un par un) |

## Scripts
| Script | Alias | Comportement |
|:-------|:------|:-------------|
| `m04_envoyer_alerte_sos` | M04 - Envoyer alerte SOS aux aidants de proximité cochés | `notify.send_message` vers les `person.x` dont l'`input_boolean.m04_proximite_aidant_N` associé est `on` (template `selectattr('ib', 'is_state', 'on')` + `map(attribute='person')`) ; titre « 🚨 SOS déclenché », message « Bouton d'urgence pressé. Vérifier la personne immédiatement. » |
| `m04_envoyer_alerte_moderee` | M04 - Envoyer alerte modérée à tous les aidants | Champs de script `titre` et `message` ; `notify.send_message` vers les 7 `person.x` (tous, cochés ou non) |

## Pièges connus / TODO
1. **Aidants fictifs** : les `person.x` sont des comptes de test — remplacer par les vrais entity_id une fois les vrais aidants inscrits dans HA (Paramètres > Personnes + appli Companion pour que `notify.send_message` puisse réellement les notifier)
2. **`notify.send_message` avec cible « person »** nécessite un HA récent ; si l'HA est plus ancien et que ça ne fonctionne pas, prévenir pour repasser sur l'ancien mécanisme (`notify.mobile_app_xxx` un par un)
3. **Historique v1** : 21 entités custom supprimées, remplacées par `person.x` + 2 groupes natifs HA (`.storage`) — les groupes ont ensuite été abandonnés en v2 (UI trop cachée)

## Annotations
- 2026-08-05 v1 : 21 entités custom supprimées, remplacées par person.x + 2 groupes natifs HA (.storage).
- 2026-08-05 v2 : groupes natifs abandonnés (UI « Aides > Groupe » jugée trop cachée par l'utilisateur). Remplacés par calcul dynamique de la cible SOS à partir des cases à cocher input_boolean.m04_proximite_aidant_N (packages/m04_gestion_aidants.yaml), visibles sur le dashboard Configuration. Les 7 person.x sont des comptes fictifs de test.
