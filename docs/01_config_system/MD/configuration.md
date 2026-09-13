# Configuration système

> Fiche rédigée le 2026-08-11 à partir de `raspi/configuration.yaml` (local).
> ⚠️ **Écart local vs prod signalé** : la prod (`Z:\configuration.yaml`) contient **2 ressources HACS en plus** : `auto-entities` et `html-template-card`. Vérifier si le local doit être mis à jour (ou si ces ressources ne sont plus utilisées).

## Rôle
Fichier racine qui déclare :
- Les intégrations par défaut (`default_config`)
- Les thèmes (`frontend.themes` → `!include_dir_merge_named themes`)
- **L'architecture packages** : `homeassistant.packages` → `!include_dir_named packages` (un fichier YAML par module)
- Un **panel_custom** « Outils Dev » dans la barre latérale (raccourci vers developer-tools/yaml)
- Les dashboards Lovelace (mode YAML pour 4 dashboards dédiés)
- Les fichiers `automations.yaml`, `scripts.yaml`, `scenes.yaml`

## Panel custom (ajout 2026-08-11)
`panel_custom.developer-tools-sidebar` : bouton « Outils Dev » (icône mdi:hammer-wrench) dans la barre latérale, qui ouvre directement `developer-tools/yaml` en iframe.

## Architecture packages
`!include_dir_named packages` charge **tous** les fichiers `.yaml` du dossier `packages/` - c'est le socle du projet modulaire (un module = un fichier).

⚠️ Conséquence : les fichiers `.bak` dans `packages/` sont ignorés (seuls les `.yaml` sont chargés), mais tout `.yaml` présent y est chargé - attention aux fichiers de test.

## Ressources frontend (HACS)
| Local | Prod (Z:) |
|:------|:----------|
| mushroom | mushroom |
| button-card | button-card |
| card-mod | card-mod |
| - | **auto-entities** |
| - | **html-template-card** |

## Dashboards déclarés
| URL | Titre | Mode | Fichier |
|:----|:------|:-----|:--------|
| `/lovelace-kiosk` | Kiosk TV | YAML | `dashboards/dashboard_kiosk.yaml` |
| `/lovelace-aidant` | Interface Aidant | YAML | `dashboards/dashboard_aidant.yaml` |
| `/lovelace-modules` | Configuration | YAML | `dashboards/dashboard_modules.yaml` |
| `/lovelace-test-simulation` | 🧪 Tests Simulation | YAML | `dashboards/dashboard_test_simulation.yaml` |

## Notes
- Les notifications SOS/aidants sont gérées **dynamiquement par dashboard** (voir `packages/m04_groupe_aidants.yaml`) - pas de groupe notify statique dans ce fichier
- `automations.yaml` / `scripts.yaml` / `scenes.yaml` existent mais sont quasi vides : la logique vit dans les packages
