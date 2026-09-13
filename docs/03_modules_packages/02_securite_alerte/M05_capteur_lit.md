# M05 — Capteur Lit

> Fiche rédigée le 2026-08-11 à partir de `raspi/packages/m05_capteur_lit.yaml` (local).
> Source live : `Z:\packages\m05_capteur_lit.yaml`.

## Rôle
Suivre l'occupation du lit à partir d'un capteur Aqara MCCGQ11LM (Door/Window Sensor Zigbee Z2M) glissé entre matelas et sommier, et fournir la durée d'occupation du lit depuis minuit. Ce module est consommé par M02 (inactivité) pour distinguer une sieste normale d'une inactivité anormale.
- `on` = contact fermé = **lit occupé** (poids de la personne) ; `off` = contact ouvert = **lit inoccupé**.
- ⚠️ **Mode simulation actif** (2026-08-05, voir `m00_simulation.yaml`) : utilise `input_boolean.sim_lit_occupe` à la place du vrai capteur Aqara.

## Dépendances
| Élément | Source | Statut |
|:--------|:-------|:-------|
| `input_boolean.sim_lit_occupe` | Simulation M00 (m00_simulation.yaml) | ⚠️ Placeholder de simulation - à remplacer par le vrai entity_id Z2M (ex : `binary_sensor.aqara_lit_contact`) une fois pairé |
| Aqara MCCGQ11LM | Capteur Door/Window Zigbee Z2M | À pairer - glissé entre matelas et sommier (détection par le poids) |
| Module M02 (inactivité) | m02_inactivite.yaml | Consommateur du module - `binary_sensor.m05_lit_occupe` distingue sieste normale d'inactivité anormale |

## Entités
| Entité | Rôle |
|:-------|:-----|
| `binary_sensor.m05_lit_occupe` | « M05 Lit Occupé » (template, `device_class: occupancy`) - `on` = lit occupé, basé sur `input_boolean.sim_lit_occupe` |
| `sensor.m05_lit_duree_occupation` | « M05 Lit Durée Occupation » (history_stats, `unique_id: m05_lit_duree_occupation`) - durée cumulée en état `on` depuis minuit (`type: time`) |

## Pièges connus / TODO avant déploiement réel
1. **Simulation active** : `value_template` et `history_stats` pointent vers `input_boolean.sim_lit_occupe` — remplacer par le vrai entity_id Z2M (ex : `binary_sensor.aqara_lit_contact`) une fois pairé
2. **Entity_id à corriger après pairage réel** (voir annotations)
3. **Logique du capteur** : `on` = contact fermé = lit occupé (poids de la personne) ; `off` = contact ouvert = lit inoccupé

## Annotations
- 2026-08-05 : création module, consommé par M02 (inactivité) pour distinguer sieste normale d'inactivité anormale. Entity_id à corriger après pairage réel.
