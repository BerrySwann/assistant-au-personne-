# Procédure d'Ajout de Matériel — Assistant au Personne
*Créé le 2026-08-11*

---

## 🧠 Principe général — La couche d'abstraction

Le système utilise des noms d'entités FIXES dans tout le code (automations, templates, dashboards).
Ex : `sensor.temperature_salon`, `binary_sensor.capteur_lit`, `media_player.tv_salon`

Quand tu branches un vrai appareil, HA lui génère un nom bizarre :
`sensor.sonoff_snzb02_a4c138_temperature` → inutilisable directement.

**La solution : des fichiers SETUP qui font le pont.**

Chaque fichier SETUP contient des **entités "wrapper"** (template) qui :
- En attente → retournent `"non_configuré"` sans faire planter HA
- Une fois l'appareil pairé → pointent vers le vrai entity_id de l'appareil

```
Vrai appareil HA           Wrapper (fichier SETUP)         Reste du système
─────────────────          ──────────────────────          ─────────────────
sensor.sonoff_a4c_temp  →  sensor.temperature_salon    →   M01, dashboards,
                           (template, entity fixe)          automations...
```

> ℹ️ Les wrappers peuvent rester définitivement — c'est une bonne pratique.
> Tu commentes uniquement le bloc PLACEHOLDER (état "non_configuré").

---

## 📁 Fichiers SETUP disponibles

| Fichier | Contenu |
|:--------|:--------|
| `setup_01_capteurs_zigbee.yaml` | T°/Hygro salon+chambre, capteur lit, porte ext. |
| `setup_02_media_camera.yaml` | TV salon, caméra chambre |
| `setup_03_presence_integrations.yaml` | Occupant/présence, Linky, Ecojoko, Calendar |

**Emplacement :** `raspi/packages/SETUP/`

**Pour activer les SETUP files sur une nouvelle install :**
Dans `configuration.yaml`, ajouter temporairement :
```yaml
homeassistant:
  packages: !include_dir_named packages/SETUP
```
→ Retirer cette ligne une fois tous les appareils configurés (les wrappers restent dans les fichiers SETUP).

---

## ⚡ Workflow par appareil (à répéter pour chaque device)

```
1. Ouvrir le fichier SETUP concerné
2. Lire la section de l'appareil à configurer
3. Ajouter l'appareil dans HA (selon type ci-dessous)
4. Trouver l'entity_id généré par HA
5. Dans le fichier SETUP : mettre # devant le bloc PLACEHOLDER
6. Décommenter le bloc RÉEL + remplacer ENTITY_ID_ICI
7. Redémarrer HA (Paramètres → Système → Redémarrer)
8. Vérifier que l'entité retourne une vraie valeur
```

---

## 🔵 TYPE A — Appareils Zigbee (capteurs T°, porte, lit, ampoules, prises)

### Pré-requis
- Clé Zigbee Sonoff EFR32MG21 V2 branchée en USB
- Add-on Zigbee2MQTT démarré

### Ajouter un appareil Zigbee

1. **Ouvrir Z2M** → `http://[IP_HA]:8099` (ou via add-on HA)
2. **Activer le pairing** → bouton "Permit join (All)" en haut
3. **Mettre l'appareil en mode pairing** (selon modèle) :
   - Sonoff SNZB-02 (T°) : maintenir bouton 5 sec jusqu'au clignotement
   - Sonoff SNZB-04 (porte) : maintenir bouton 5 sec
   - IKEA Dirigera / ampoule : 6 allumages/extinctions rapides
   - NOUS SP3 (prise) : maintenir bouton 5 sec
4. **Attendre** que Z2M affiche le nouvel appareil (10-30 sec)
5. **Renommer l'appareil** dans Z2M avec un nom lisible (ex: `snzb02_salon`)
6. Dans HA → **Paramètres → Appareils** → trouver le nouvel appareil → noter l'entity_id

### Trouver l'entity_id
- Paramètres → Appareils et services → Appareils → chercher le nom
- Cliquer sur l'appareil → voir la liste des entités générées
- Ex: `sensor.snzb02_salon_temperature`, `sensor.snzb02_salon_humidity`

---

## 🟢 TYPE B — Philips Hue

1. **Paramètres → Appareils et services → Ajouter une intégration**
2. Chercher "Philips Hue" → suivre l'assistant
3. Appuyer sur le bouton du Hue Bridge quand demandé
4. Toutes les ampoules apparaissent automatiquement

> ℹ️ Les ampoules Hue sont gérées via le Hue Bridge, pas via Zigbee direct.
> Leurs entity_ids sont du type `light.hue_white_lamp_salon_1` etc.
> Dans ce projet les noms sont déjà normalisés → pas de wrapper nécessaire si les noms correspondent.

---

## 🟡 TYPE C — Android TV / Chromecast (TV salon)

1. La TV doit être allumée et sur le même réseau Wi-Fi
2. **Paramètres → Appareils et services → Ajouter une intégration**
3. Chercher "Android TV" ou "Google Cast"
4. HA détecte automatiquement les appareils sur le réseau
5. Autoriser la connexion sur la TV si demandé
6. Entity générée : `media_player.nom_de_la_tv`

---

## 🔴 TYPE D — Caméra IP (chambre)

### Caméra Reolink (recommandée)
1. Brancher la caméra au réseau
2. **Paramètres → Ajouter une intégration → Reolink**
3. Entrer l'IP de la caméra + identifiants admin
4. Entity générée : `camera.reolink_[nom]`

### Caméra générique RTSP
1. **Paramètres → Ajouter une intégration → Caméra générique**
2. URL flux : `rtsp://user:pass@IP_CAMERA:554/stream`
3. Entity générée : `camera.camera_generique`

---

## 🔌 TYPE E — Linky (MyElectricalData)

1. **Paramètres → Ajouter une intégration → MyElectricalData**
2. Entrer le numéro PDL (14 chiffres, sur la facture EDF)
3. Entrer le token d'accès (créer un compte sur `myelectricaldata.fr`)
4. Les entités HP/HC apparaissent automatiquement

---

## 📱 TYPE F — Présence (téléphone de l'occupant)

### Option 1 — HA Companion (app téléphone)
1. Installer l'app "Home Assistant" sur le téléphone de l'occupant/aidant
2. Se connecter avec le compte HA correspondant
3. Autoriser la localisation
4. Entity générée : `person.nom_personne` + device tracker

### Option 2 — Détection Wi-Fi (NMAP)
1. **Paramètres → Ajouter → Nmap Tracker**
2. Entrer la plage réseau (ex: `192.168.1.0/24`)
3. HA détecte les appareils connectés au Wi-Fi
4. Entity générée : `device_tracker.telephone_xxx`

---

## ✅ Checklist de mise en service complète

| Appareil | Fichier SETUP | Module | OK ? |
|:---------|:-------------|:-------|:-----|
| Clé Zigbee (Z2M démarré) | — | Tous | ☐ |
| Capteur T°/Hygro Salon | `setup_01_capteurs_zigbee.yaml` | M01 | ☐ |
| Capteur T°/Hygro Chambre | `setup_01_capteurs_zigbee.yaml` | M01 | ☐ |
| Capteur Lit | `setup_01_capteurs_zigbee.yaml` | M05 | ☐ |
| Capteur Porte Ext. | `setup_01_capteurs_zigbee.yaml` | M15 | ☐ |
| TV Salon | `setup_02_media_camera.yaml` | M11 | ☐ |
| Caméra Chambre | `setup_02_media_camera.yaml` | M06 | ☐ |
| Présence occupant | `setup_03_presence_integrations.yaml` | M04 | ☐ |
| Linky (MyElectricalData) | `setup_03_presence_integrations.yaml` | M00 | ☐ |
| Ecojoko | `setup_03_presence_integrations.yaml` | M00 | ☐ |
| Hue Bridge | TYPE B (UI direct) | M03 éclairage | ☐ |
| Comptes aidants (x5) | Paramètres → Personnes | M03 messages | ☐ |
| Nabu Casa | Paramètres → Cloud | Accès distant | ☐ |
