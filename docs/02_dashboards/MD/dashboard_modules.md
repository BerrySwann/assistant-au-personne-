# Dashboard Modules (configuration)

> Fiche rédigée le 2026-08-11 à partir de `raspi/dashboards/dashboard_modules.yaml`.
> ⚠️ Fichier modifié récemment (11 août) - version locale à comparer avec `Z:\dashboards\dashboard_modules.yaml`.

## Rôle
Dashboard de **configuration** : activation/désactivation des modules, réglages détaillés, gestion des aidants et des sessions TV.

## 5 vues
| Vue | Contenu principal |
|:----|:------------------|
| ✅ Général | Modules obligatoires (M00...) - section « ✅ Obligatoires » |
| 🛡️ Sécurité & Santé | Modules sécurité + **M04 — Aidants de proximité (reçoivent le SOS)** |
| 🎵 Confort & Loisirs | Confort + **M11 — Réglages des 3 sessions TV** + Réglages avancés TV (communs) |
| 🌡️ Environnement | Température, humidité, ambiance |
| 👨👩👧 Lien Famille | Lien famille (visio, messages) |

## Cartes utilisées
- 42 cartes `custom` (mushroom, button-card, auto-entities...)
- 6 `vertical-stack`, 6 `panel`, 5 `entities`, 3 `horizontal-stack`, 1 `grid`

## Caractéristiques
| Élément | Détail |
|:--------|:-------|
| Mode | YAML |
| URL | `/lovelace-modules` |
| Icône | `mdi:cog-outline` |
| Public | Administrateurs |

## Notes
- C'est le plus gros dashboard du projet (48 Ko local)
- Règle projet : **ne jamais modifier ce fichier via l'éditeur UI Lovelace** (risque d'écrasement) - uniquement en YAML local puis déploiement
- La carte aidants utilise le filtre `person.*` (sauf `person.eric`) + helpers `m04_prox_<id>` (voir M04)
