# M00 — Interrupteurs Modules + Utilitaires Système

> Fiche rédigée le 2026-08-11 à partir de `raspi/packages/m00_modules.yaml` (local).
> Source live : `Z:\packages\m00_modules.yaml`.

## Rôle
Module **socle** : déclare les interrupteurs de module (`input_boolean.module_*`) pour chaque module M01-M20 + l'utilitaire système de date/heure. Chaque package métier référence son interrupteur pour conditionner ses automations.

- Convention : `entity_id` max **20 caractères après « module_ »**.
- ⚠️ **Correctif 2026-08-05** : suppression de tous les `initial:`. Piège HA : `initial:` réinitialise la valeur à CHAQUE redémarrage (pas juste à la création), ce qui écrasait les choix de l'utilisateur sur le dashboard Configuration après chaque reboot. Sans `initial:`, HA restaure le dernier état connu de chaque interrupteur.

## Dépendances
| Élément | Source | Statut |
|:--------|:-------|:-------|
| `sensor.time` / `sensor.date` / `sensor.date_time` | Plateforme `time_date` (intégration standard HA) | Générés par ce package |
| `input_boolean.module_*` | Ce package | Consommés par les packages M01-M20 (condition de leurs automations) |

## Entités
| Entité | Rôle |
|:-------|:-----|
| `sensor.time` / `sensor.date` / `sensor.date_time` | Utilitaires système (display_options : time, date, date_time) |
| `module_temp_hygro` | **M01 Température & Hygro** (mdi:thermometer) — OBLIGATOIRE |
| `module_inactivite` | **M02 Détection Inactivité** (mdi:motion-sensor) — OBLIGATOIRE |
| `module_ecran_msg` | **M03 Écran Messages** (mdi:message-text-outline) — OBLIGATOIRE |
| `module_sos` | **M04 Bouton SOS** (mdi:alarm-light-outline) — OPTIONNEL |
| `module_capteur_lit` | **M05 Capteur Lit** (mdi:bed-outline) — OPTIONNEL |
| `module_cam_ia` | **M06 Caméra IA** (mdi:eye-outline) — OPTIONNEL |
| `module_kiosk_ecran` | **M07 Kiosk Écran** (mdi:monitor) — OPTIONNEL |
| `module_kiosk_foto` | **M08 Photos Famille** (mdi:image-multiple-outline) — OPTIONNEL |
| `module_kiosk_zic` | **M09 Musique** (mdi:music-note-outline) — OPTIONNEL |
| `module_visio` | **M10 Visioconférence** (mdi:video-outline) — OPTIONNEL |
| `module_television` | **M11 Télévision** (mdi:television-play) — OPTIONNEL |
| `module_douche` | **M12 Douche** (mdi:shower-head) — OPTIONNEL |
| `module_m20_medoc` | **M13 Médicaments** (mdi:pill-multiple) — OPTIONNEL — ✅ rappel construit 16/08 (voir M13_medoc.md) |
| ~~`module_m21_repas`~~ | ~~**M14 Repas**~~ — 🚫 **abandonné 16/08** (signal non fiable, entité retirée de m00_modules.yaml) |
| `module_porte_ext` | **M15 Porte Extérieure** (mdi:door-open) — OPTIONNEL |
| `module_lumiere_nuit` | **M16 Veilleuse Nuit** (mdi:weather-night) — OPTIONNEL |
| `module_chauffage` | **M17 Chauffage** (mdi:radiator) — OPTIONNEL |
| `module_fenetre` | **M18 Fenêtres** (mdi:window-open-variant) — OPTIONNEL |
| `module_dashboard_fam` | **M19 Dashboard Famille** (mdi:home-heart) — OPTIONNEL |
| `module_msg_famille` | **M20 Messages Famille** (mdi:message-outline) — OPTIONNEL |

## Automations
| ID | Alias | Déclencheur | Action |
|:---|:------|:------------|:-------|
| — | Aucune dans ce package | — | Fichier purement déclaratif (helpers + sensor time_date) |

## Pièges connus / TODO avant déploiement
1. **Piège `initial:`** (correctif 2026-08-05) : ne pas ajouter `initial:` sur ces entités — ça réinitialise la valeur à CHAQUE redémarrage et écrasait les choix du dashboard Configuration (voir IA_CONTEXT_BASE_AI.md - Piège 1). Sans `initial:`, HA restaure le dernier état connu.
2. **Convention de nommage** : `entity_id` max 20 caractères après « module_ ».
3. **Ne pas redéclarer un `input_boolean.module_*` dans un autre package** (conflit `unique_id` si dupliqué entre packages) — cf. note dans m08_photos.yaml pour `module_kiosk_foto`. Exception constatée : `module_liens_youtube` (M16 divertissement) est déclaré dans son propre package m16_liens_youtube.yaml.
4. ⚠️ **Divergence de numérotation M16** : ce fichier associe « M16 » à `module_lumiere_nuit` (Veilleuse Nuit), alors que le package `04_divertissement/m16_liens_youtube.yaml` est intitulé « M16 Liens YouTube » — deux modules différents sous le même numéro, à clarifier dans la numérotation du projet.

## Annotations
- 2026-08-05 : correctif — suppression de tous les `initial:` (piège HA : réinitialisation à chaque redémarrage).
