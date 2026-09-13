# M15 — Porte Extérieure

> Fiche rédigée le 2026-08-11 à partir de `raspi/packages/m15_porte_ext.yaml` (local).
> Source live : `Z:\packages\m15_porte_ext.yaml`.

## Rôle
Mesurer la durée cumulée d'ouverture de la porte extérieure depuis minuit, à partir du capteur d'ouverture SONOFF SNZB-04P (Zigbee Z2M).
- ⚠️ **ATTENTION — logique inversée** : state `off` = porte **OUVERTE** (le `history_stats` compte le temps passé en état `off`).
- Module minimal : aucune automation, aucun input_boolean — uniquement un capteur de statistiques.

## Dépendances
| Élément | Source | Statut |
|:--------|:-------|:-------|
| `binary_sensor.snzb04p_porte_ext_contact` | SONOFF SNZB-04P (Zigbee Z2M) | Capteur physique - ⚠️ logique inversée : state `off` = porte OUVERTE |

## Entités
| Entité | Rôle |
|:-------|:-----|
| `sensor.m15_porte_ext_duree_ouverture` | « M15 Porte Ext Durée Ouverture » (history_stats, `unique_id: m15_porte_ext_duree_ouverture`) - durée cumulée en état `off` (porte ouverte) depuis minuit (`type: time`) |

## Pièges connus / TODO
1. **Logique inversée** : `off` = porte OUVERTE — ne pas interpréter `off` comme « porte fermée » ; le compteur mesure bien le temps passé porte ouverte
2. Aucun TODO ni avertissement supplémentaire dans le YAML source (module minimal)

## Annotations
- Aucune `annotations_log` dans le YAML source.
