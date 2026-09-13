# Dashboard Test Simulation

> Fiche rédigée le 2026-08-11 à partir de `raspi/dashboards/dashboard_test_simulation.yaml`.
> Source live : `Z:\dashboards\dashboard_test_simulation.yaml`.

## Rôle
Dashboard de **test** : simule les capteurs et accélère la validation des automations (notamment M02 inactivité) sans matériel réel.

## 4 sections
| Section | Contenu |
|:--------|:--------|
| 🎛️ Faux capteurs (à manipuler) | `input_boolean` de simulation (présence, etc.) |
| 🌡️ Température & Porte (M01/M15) | Simulations temp salon/chambre, hygro, contact porte *(ajout 2026-08-11)* |
| ⚙️ Réglages (pour accélérer les tests) | Seuils, paramètres ajustables |
| 🚨 Résultats attendus (à observer) | Rappel des comportements attendus |
| 🔄 Modules actifs (à vérifier avant test) | État des interrupteurs de modules (M00) |

## Cartes utilisées
- 4 cartes `entities`, 1 carte `markdown`

## Caractéristiques
| Élément | Détail |
|:--------|:-------|
| Mode | YAML |
| URL | `/lovelace-test-simulation` |
| Icône | `mdi:test-tube` |
| Public | Testeurs / admin |

## Notes
- Indispensable tant que le radar SNZB-06P n'est pas pairé (le M02 utilise `input_boolean.sim_snzb06p_presence`)
- Se coordonne avec `m00_simulation.yaml` et `m00_simulation_sensors.yaml` (socle)
