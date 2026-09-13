# M04 — Bouton SOS

> Fiche rédigée le 2026-08-11 à partir de `raspi/packages/m04_sos.yaml` (local).
> Source live : `Z:\packages\m04_sos.yaml`.

## Rôle
Déclencher l'alerte d'urgence quand l'occupant appuie sur le bouton SOS (WOOX R7052, bouton Zigbee Z2M reconnu comme TS0215A) : activation du flag `m04_sos_declenche`, envoi de l'alerte aux aidants via le script M04-groupe, et trace visible dans HA. Un reset manuel (repasse le flag sur `off`) efface la notification.
- ⚠️ **Mode simulation actif** (2026-08-05, voir `m00_simulation.yaml`) : le déclencheur utilise `input_boolean.sim_sos_bouton` (impulsion 2s) à la place du vrai bouton Zigbee.
- L'automation n'agit que si `input_boolean.module_sos` est sur `on` (interrupteur de module).

## Dépendances
| Élément | Source | Statut |
|:--------|:-------|:-------|
| `input_boolean.sim_sos_bouton` | Simulation M00 (m00_simulation.yaml) | ⚠️ Placeholder de simulation - à remplacer par ce qu'expose réellement Z2M une fois le bouton pairé |
| `input_boolean.module_sos` | M00 (interrupteur de module) | Conditionne l'automation |
| `script.m04_envoyer_alerte_sos` | Module M04-groupe (m04_groupe_aidants.yaml) | Envoi de l'alerte SOS aux aidants de proximité cochés |
| WOOX R7052 (TS0215A) | Bouton Zigbee Z2M | À pairer - ⚠️ nécessite Z2M à jour (versions anciennes peuvent ne pas reconnaître le modèle) |

## Entités
| Entité | Rôle |
|:-------|:-----|
| `input_boolean.m04_sos_declenche` | Flag « M04 SOS Déclenché » (`initial: false` → remise à zéro au redémarrage) ; sa descente sur `off` déclenche le reset manuel |

## Automations
| ID | Alias | Déclencheur | Action |
|:---|:------|:------------|:-------|
| `m04_sos_appui` | M04 - SOS bouton appuyé | `input_boolean.sim_sos_bouton` → `on` (si `module_sos` = on) | Allume `m04_sos_declenche` ; lance `script.m04_envoyer_alerte_sos` ; notification « 🚨 SOS déclenché » |
| `m04_sos_reset` | M04 - SOS reset manuel | `input_boolean.m04_sos_declenche` → `off` | `persistent_notification.dismiss_all` |

Mode `single` sur les deux automations (pas de cumul de déclenchements).

## Pièges connus / TODO avant déploiement réel
1. **Simulation active** : le trigger pointe vers `input_boolean.sim_sos_bouton` — remplacer par ce qu'expose réellement Z2M une fois le bouton pairé (en général `sensor.xxx_action` avec valeurs `single` / `double` / `hold`)
2. **Vérifier le nom du device dans Z2M** (Paramètres > Appareils > « woox »)
3. **Notification en `persistent_notification`** : visible dans HA mais l'alerte SOS ne sort jamais du serveur HA — à remplacer par `notify.mobile_app_<aidant>` réel avant mise en prod
4. **Z2M à jour requis** : les versions anciennes peuvent ne pas reconnaître le modèle WOOX R7052

## Annotations
- 2026-08-05 : création module. Notification actuellement en persistent_notification (visible dans HA) — à remplacer par notify.mobile_app_<aidant> réel avant mise en prod, sinon l'alerte SOS ne sort jamais du serveur HA.
