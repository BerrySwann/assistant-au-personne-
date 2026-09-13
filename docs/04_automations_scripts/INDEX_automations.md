# INDEX Automations & Scripts

> Rédigé le 2026-08-11 à partir des packages de `raspi/packages/` (et Z: pour les modules non locaux).
> Les automations vivent **dans les packages** (un module = ses automations). `automations.yaml` racine est quasi vide.

## Automations (par module)

| Module | Automation | Rôle |
|:-------|:-----------|:-----|
| M00 simulation | SIMU - Reset auto bouton SOS après appui | Réarme le bouton SOS simulé après déclenchement |
| M02 | M02 - Vérification inactivité périodique | Toutes les 5 min : alerte si inactivité anormale (3 cas) |
| M02 | M02 - Reset alerte au retour de présence | Coupe les alertes dès que la présence revient |
| M03 | M03 - Horodater automatiquement à l'envoi d'un nouveau message | Ajoute date/heure aux messages envoyés |
| M04 SOS | M04 - SOS bouton appuyé | Déclenche l'alerte SOS (simulation ou WOOX R7052) |
| M04 SOS | M04 - SOS reset manuel | Réinitialise l'état SOS |
| M04 aidants | M04 - Envoyer alerte SOS aux aidants de proximité cochés | Notifie les `person.x` cochés (⚠️ `notify.send_message` commenté - person fictifs) |
| M04 aidants | M04 - Envoyer alerte modérée à tous les aidants | Alerte modérée (⚠️ idem, commenté) |
| M08 | M08 - Retour à l'écran photos (dashboard kiosk) | Renavigation kiosk après fin de session |
| M11 | M11 - Lancer la chaîne/vidéo d'une session | Bascule le navigateur TV (browser_mod.javascript) |
| M11 | M11 - Vérifier les sessions TV (toutes les minutes) | Gestion des créneaux/sessions selon horaires |
| M11 | M11 - Retour photos si module TV désactivé | Retour kiosk si M11 désactivé |

## Scripts

| Module | Script | Rôle |
|:-------|:-------|:-----|
| M04 | `m04_envoyer_alerte_sos` (et `_moderee`) | Envoi des notifications aidants (⚠️ notify commenté en attendant les vrais comptes) |
| M08 | `m08_lancer_diaporama` | Lance le diaporama photos |
| M11 | `m11_lancer_session` | Lance une session TV (chaîne ou YouTube) avec rotation M16 |

## Modules SANS automation
- **M00** (helpers/interrupteurs), **M01** (capteurs/templates), **M05** (capteur lit), **M15** (capteur porte) : pas d'automation - purement des entités/templates consommés par d'autres modules (ex. M02 consomme M05)

## Notes de déploiement
- Les alertes utilisent encore `notify.persistent_notification` et `notify.send_message` commenté - **à remplacer par `notify.mobile_app_<aidant>`** avant mise en prod (voir histo 2026-08-05)
- Les IDs d'automation sont préfixés par module (`m02_`, `m04_`, `m11_`) - convention stable
