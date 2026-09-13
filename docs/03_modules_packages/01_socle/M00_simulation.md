# M00-SIM — Capteurs Fictifs (Prototypage Sans Matériel)

> Fiche rédigée le 2026-08-11 à partir de `raspi/packages/m00_simulation.yaml` (local).
> Source live : `Z:\packages\m00_simulation.yaml`.

## Rôle
Module **socle / simulation** : simuler les capteurs Zigbee pas encore achetés/pairés (**SNZB-06P**, **WOOX SOS**, **Aqara lit**) pour tester la logique des automations **M02/M04/M05 sans matériel physique**. Chaque helper se manipule à la main dans Developer Tools > États, ou via une carte dashboard simple (fournie en commentaire du YAML, à coller dans `dashboard_modules.yaml`).

⚠️ **À FAIRE LE JOUR OÙ LE VRAI MATÉRIEL ARRIVE** :
- Remplacer les entity_id `input_boolean.sim_*` par les vrais entity_id Z2M dans `m02_inactivite.yaml`, `m04_sos.yaml`, `m05_capteur_lit.yaml`
- Supprimer ce fichier (ou le laisser inactif, il ne gêne rien s'il n'est plus référencé nulle part)

## Dépendances
| Élément | Source | Statut |
|:--------|:-------|:-------|
| `input_boolean.sim_snzb06p_presence` | Simulation du radar SONOFF SNZB-06P (Z2M) | ⚠️ Placeholder — à remplacer par le vrai entity_id Z2M au pairage |
| `input_boolean.sim_sos_bouton` | Simulation du bouton WOOX SOS | ⚠️ Placeholder — idem (m04_sos.yaml) |
| `input_boolean.sim_lit_occupe` | Simulation du capteur Aqara sous matelas | ⚠️ Placeholder — idem (m05_capteur_lit.yaml) |

## Entités
| Entité | Rôle |
|:-------|:-----|
| `input_boolean.sim_snzb06p_presence` | « SIMU — Présence Salon (radar) » — `initial: true` — simule la présence détectée par le radar |
| `input_boolean.sim_sos_bouton` | « SIMU — Bouton SOS pressé » — `initial: false` — simule l'appui SOS |
| `input_boolean.sim_lit_occupe` | « SIMU — Lit Occupé » — `initial: false` — simule le capteur de lit |

## Automations
| ID | Alias | Déclencheur | Action |
|:---|:------|:------------|:-------|
| `sim_sos_impulsion` | SIMU - Reset auto bouton SOS après appui | `input_boolean.sim_sos_bouton` → on | Attente 2 s puis `input_boolean.turn_off` sur `sim_sos_bouton` |

Mode `single`. Cette automation imite un vrai bouton Zigbee qui n'a pas d'état « on » permanent — c'est une **impulsion**, pas un interrupteur.

## Pièges connus / TODO avant déploiement
1. **Placeholders de simulation** : remplacer les `input_boolean.sim_*` par les vrais entity_id Z2M dans m02_inactivite.yaml, m04_sos.yaml, m05_capteur_lit.yaml le jour où le matériel arrive
2. **Supprimer ce fichier** (ou le laisser inactif) au passage au matériel réel
3. **`sim_sos_bouton` = impulsion** : reset automatique après 2 s — ne pas chercher un état « on » permanent (mimétisme d'un vrai bouton Zigbee)
4. **Aucune valeur réelle** : ces états servent uniquement au prototypage — ne pas les utiliser pour du diagnostic
5. **Carte dashboard optionnelle** : un bloc « 🧪 Simulation capteurs (proto sans matériel) » est fourni en commentaire du YAML pour piloter les faux capteurs sans Developer Tools

## Annotations
- 2026-08-05 : création du module de simulation. Permet de tester M02/M04/M05 sans matériel Zigbee physique. m02/m04/m05 modifiés en parallèle pour pointer vers ces entités fictives à la place des placeholders Z2M.
