# Récapitulatif des modifications — 2026-08-05

## Contexte
Séance de travail sur le module M04 (SOS & Aidants). Blocage identifié : les `person.*` sont fictifs et sans Companion app → `notify.send_message` échoue silencieusement.

## Modifications

### 1. `packages/m04_groupe_aidants.yaml`
- **Scripts `m04_envoyer_alerte_sos` et `m04_envoyer_alerte_moderee`** : `notify.send_message` commenté (lignes 30-39 et 49-56). Le code est conservé, prêt à être décommenté quand les aidants auront l'app Companion installée.

### 2. `dashboards/dashboard_modules.yaml`
- **Carte auto-entities « Aidants de proximité »** (ligne 183) : le filtre passe de `input_boolean.m04_prox_*` à `person.*` (sauf `person.eric`). Chaque ligne affiche le nom de la personne (depuis `person.*`) avec le toggle du helper `input_boolean.m04_prox_<id>` correspondant.
- Résultat : ajouter une personne dans HA → apparition immédiate dans la liste du dashboard. Le toggle fonctionne dès que le helper est créé.

## Comportement actuel du système M04
- Le dashboard liste toutes les `person.*` (sauf Eric) dynamiquement
- Chaque personne a un toggle (helper `input_boolean.m04_prox_<id>`)
- Toggle ON = cette personne recevra le SOS (dès que `notify.send_message` sera réactivé)
- La `persistent_notification` HA fonctionne toujours (alerte visible dans l'UI HA)

## Pour ajouter un nouvel aidant
```bash
# Après avoir créé la personne dans HA (UI > Paramètres > Personnes) :
hab helper input-boolean create m04_prox_<object_id> --icon mdi:account-heart
```

## À faire pour activer complètement M04
1. Créer les vrais comptes aidants dans HA
2. Installer l'app Companion sur chaque téléphone
3. Décommenter les blocs `notify.send_message` dans `m04_groupe_aidants.yaml`
4. Remplacer le trigger simulation (`sim_sos_bouton`) par le vrai bouton Zigbee WOOX R7052
