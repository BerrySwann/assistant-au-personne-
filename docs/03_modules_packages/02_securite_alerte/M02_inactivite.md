# M02 — Détection Inactivité

> Fiche rédigée le 2026-08-11 à partir de `raspi/packages/m02_inactivite.yaml` (local).
> Source live : `Z:\packages\m02_inactivite.yaml`.

## Rôle
Détecter une inactivité anormale de l'occupant (aucun mouvement pendant un seuil configurable) et alerter la famille, en distinguant les périodes de la journée :
- **Heures actives** (8h-12h, 15h-19h) : aucun mouvement pendant 45 min (défaut) → alerte
- **Sieste** (12h-15h) + lit occupé → aucune alerte (normal)
- **Sieste** + lit inoccupé + 45 min sans mouvement → alerte douce
- **Nuit** (22h-8h) → aucune alerte (sommeil normal)
- **Nuit** + lit inoccupé après 23h + aucun mouvement → alerte « absence nocturne anormale »

## Dépendances
| Élément | Source | Statut |
|:--------|:-------|:-------|
| `input_boolean.sim_snzb06p_presence` | Radar SONOFF SNZB-06P (Z2M) | ⚠️ Placeholder de simulation - à remplacer par l'entity_id réel après pairage |
| `binary_sensor.m05_lit_occupe` | Module M05 (capteur Aqara MCCGQ11LM sous matelas) | Dépend du M05 |
| `input_boolean.module_inactivite` | M00 (interrupteur de module) | Conditionne l'automation |

⚠️ Variante radar : **SNZB-06P (5,8 GHz)** obligatoire - PAS le SNZB-06P24 (24 GHz) dont la doc fabricant indique une détection non fiable d'une personne endormie/immobile (CDC §5.2).

## Entités
| Entité | Rôle |
|:-------|:-----|
| `input_number.m02_seuil_alerte_min` | Seuil d'alerte en minutes (10-120, défaut 45) |
| `input_boolean.m02_alerte_active` | Alerte inactivité en cours (auto-reset) |
| `input_boolean.m02_absence_hors_horaires_nuit` | Absence nocturne anormale (auto-reset) |
| `sensor.m02_etat_temporel` | Période courante : `actif` / `sieste` / `nuit` / `transition` (template) |

## Automations
| ID | Alias | Déclencheur | Action |
|:---|:------|:------------|:-------|
| `m02_verifier_inactivite` | Vérification périodique | Toutes les 5 min (si module ON) | Cas 1 : alerte seuil ; Cas 2 : sieste+lit occupé = rien ; Cas 3 : absence nocturne après 23h |
| `m02_reset_alerte` | Reset au retour de présence | Présence → ON | Coupe les 2 alertes |

Mode `single` sur les deux automations (pas de cumul de déclenchements).

## Pièges connus / TODO avant déploiement
1. **`sim_snzb06p_presence` = placeholder** : remplacer par le vrai entity_id Z2M une fois le capteur pairé
2. **Notifications en `persistent_notification`** : à remplacer par `notify.mobile_app_<aidant>` avant mise en prod
3. **Couverture mono-zone** : ne couvre qu'une zone (salon) - dupliquer la logique par pièce si besoin
4. **Non testé en conditions réelles** : test de couverture obligatoire (CDC §7) - traverser la pièce 2 min, vérifier détection continue sans zone morte
5. ⚠️ Piège `initial:` : ne pas ajouter `initial:` sur les entités dont la valeur doit persister entre redémarrages (voir IA_CONTEXT_BASE_AI.md - Piège 1)

## Annotations
- 2026-08-05 : création du module complet (état temporel + vérif 5 min + reset auto)
