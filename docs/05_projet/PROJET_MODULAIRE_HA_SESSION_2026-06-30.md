# 🏠 PROJET MODULAIRE HOME ASSISTANT — AIDE À LA PERSONNE EN DIFFICULTÉ
*Session de travail — 2026-06-30*

---

## 🎯 VISION DU PROJET

Système domotique modulaire basé sur Home Assistant, conçu pour maintenir à domicile des personnes en difficulté (Alzheimer, fragilité physique, isolement, post-AVC).

Inspiré du projet de **Benjamin Code** pour sa mère atteinte d'Alzheimer, mais généralisé et structuré pour être reproductible par n'importe quel aidant.

**Principe fondamental :** Un questionnaire génère un profil JSON qui active uniquement les modules pertinents. On ne paye que ce qu'on utilise, on n'installe que ce dont on a besoin.

---

## 📦 CE QUE BENJAMIN A MIS EN PLACE (référence)

| # | Module | Déclencheur | Effet |
|---|--------|-------------|-------|
| 1 | Écran kiosque | Permanent | Heure, date, photos, messages |
| 2 | Messages agenda | Calendrier famille | "Paul vient demain" sur l'écran |
| 3 | Thérapie musicale | 11h quotidien | Playlist souvenir / classique |
| 4 | TV contrôle | Allumage TV | Chaîne calme + volume 17 forcé |
| 5 | Jitsi visio | Famille déclenche | Appel sur TV, 0 action côté patient |
| 6 | Suivi douche | Humidité SDB | Si pas de douche à 16h → message écran |
| 7 | Capteur porte | Sortie hors horaires | Alerte famille + vue caméra |
| 8 | YouTube/divertissement | Demande famille | Lecture ballet/opéra sur TV |
| 9 | iPhone simplifié | Manuel (iOS) | Accès Assisté — hors HA |
| 10 | 4G backup | Panne box | Continuité du système |

---

## 🖥️ HARDWARE

### Développement / Test
- **Raspberry Pi 4 4GB** (existant chez Eric)
- Limitations : YouTube cap 720p, Jitsi doit être sur VPS externe
- Réseau : Ethernet recommandé, WiFi dual-band 2.4/5GHz disponible

### Production (déploiement chez une personne)
- **NiPoGi Pinova P1** — AMD Ryzen R2544 (4C/8T, 3.7GHz) — 16GB RAM / 256GB SSD
- Prix : ~279€ (16Go) / ~249€ (8Go) — choisir le 16Go (+30€, vaut le coup)
- Windows 11 Pro préinstallé → à remplacer par HAOS
- Référence matérielle du projet : **même modèle que Benjamin**

### Réseau
- Mini PC → **Ethernet** (stable 24/7)
- Caméras → **WiFi 2.4GHz** (même réseau local, IP fixe via DHCP)
- **Dongle 4G USB** (~25€ — Huawei E3372 ou ZTE MF833) → backup automatique
  - SIM : **Lebara 50Go à ~5.99€/mois** (couverture nationale correcte)
  - Zone rurale → **Orange** recommandé (meilleure couverture)
  - Configuré en failover via NetworkManager sur le mini PC

### Caméras
- **Reolink E1** ou **Tapo C110** — ~27€ — WiFi — RTSP natif HA
- Flux RTSP → Frigate (local) ou directement LLM Vision

---

## 💰 BUDGET

### Hardware (coût unique)
```
Mini PC NiPoGi P1 16Go          279€
Dongle 4G                        25€
Clé Zigbee (Sonoff EFR32MG21)   25€
Caméra(s) Reolink E1 ~27€/u     27€+
Capteurs Zigbee (selon modules)
  ├── Capteur porte              20€
  ├── Motion sensors x2-3       50€
  ├── Humidité SDB               20€
  ├── Température                20€
  ├── Bouton SOS                 20€
  └── Capteur matelas (contact)  15€
Câbles, divers                   50€
────────────────────────────────────
Enveloppe affichée          800-1000€
```

### Récurrent annuel
```
SIM data (Lebara ~5.99€/mois)   ~72€/an
Nom de domaine (OVH/Cloudflare) ~10€/an
────────────────────────────────────────
Total affiché                  ~100€/an
```

---

## 🧰 STACK LOGICIELLE

| Composant | Solution | Coût |
|-----------|----------|------|
| OS | HAOS (Home Assistant OS) | Gratuit |
| Domotique | Home Assistant | Gratuit |
| Zigbee | Zigbee2MQTT | Gratuit |
| YouTube sans pub | **Invidious** (Docker, self-hosted) | Gratuit |
| Visio famille | **Jitsi** self-hosted sur VPS | ~5€/mois |
| Accès distant famille | **Cloudflare Tunnel** + domaine | ~10€/an |
| Vision AI caméra | **LLM Vision v1.7.0** (HACS) | Gratuit |
| Provider AI | **Gemini Flash** (free tier) | Gratuit |
| Dashboard mobile | **Mushroom Cards** + Browser Mod (HACS) | Gratuit |

### ⚠️ Décisions techniques actées

- **Tailscale → écarté** : VPN sur mobile perturbe les autres apps de la famille
- **Nabu Casa → écarté** : 90€/an vs 10€/an pour un domaine + Cloudflare Tunnel
- **SmartTube → écarté** : trop instable, Google casse régulièrement
- **Aqara FP2 → écarté** : WiFi (pas Zigbee), fall detection expérimentale
- **7B LLM local → écarté** : trop lent sur CPU sans GPU (30-60s/inférence)
- **Inactivité 4h flat → écarté** : trop lent, dangereux

---

## 📋 CATALOGUE DES MODULES

### 🔴 MODULES OBLIGATOIRES (toujours actifs, non négociables)

| Module | Description |
|--------|-------------|
| `temperature_monitor` | T° < 16°C → alerte froid / T° > 28°C → alerte chaleur + hydratation / Couplé vigilance Météo France canicule |
| `inactivity_monitor` | Logique temporelle (pas un timer plat) — voir section dédiée |
| `screen_messages` | Orientation minimale : heure, date, messages de base |

> **`temperature_monitor` : NON NÉGOCIABLE**
> Canicule 2003 = 15 000 morts, quasi exclusivement personnes âgées seules.
> Couvre les deux sens : froid dangereux ET chaleur mortelle.

### 🟠 MODULES FORTEMENT RECOMMANDÉS

| Module | Description | Matériel |
|--------|-------------|---------|
| `camera_monitoring` + `llm_vision` | Snapshot sur déclenchement inactivité → Gemini Flash analyse posture → alerte si "au sol" | Reolink E1 ~27€ |
| `sos_button` | Bouton Zigbee → notification famille immédiate | ~20€ |
| `mattress_sensor` | Capteur contact Aqara sous matelas → confirme sieste/sommeil | ~15€ |

### 🟡 MODULES OPTIONNELS (activés par le questionnaire)

| Module | Description | Profil concerné |
|--------|-------------|-----------------|
| `kiosk_screen` | Écran permanent : heure, date, photos, messages | Alzheimer |
| `kiosk_photos` | Diaporama photos famille — sync automatique via rclone (Google Drive partagé famille → local nuit) | Alzheimer, Isolement |
| `tv_control` | Chaîne calme automatique + volume fixe au démarrage | Alzheimer |
| `music_therapy` | Playlists souvenirs à heure fixe — **curatée à l'installation par l'aidant principal uniquement** (pas de sync famille) | Alzheimer |
| `youtube_invidious` | Invidious local, sans pub, 720p max | Tous |
| `visio_jitsi` | Jitsi sur VPS, déclenché par présence, 0 action patient | Tous |
| `shower_tracking` | Capteur humidité SDB → si pas de douche à 16h → message | Alzheimer |
| `medication_reminder` | Rappel médicaments écran + TTS | Post-AVC, Fragilité |
| `meal_reminder` | Activité cuisine surveillée → rappel si pas de repas | Post-AVC |
| `door_monitor` | Sortie hors horaires → alerte famille | Alzheimer |
| `night_lighting` | Éclairage progressif chambre→SDB la nuit | Fragilité physique |
| `family_dashboard` | Vue famille : statuts, dernière activité, alertes | Tous |
| `heating_control` | Contrôle chauffage (si pilotable) | Selon équipement |
| `screen_messages_family` | Famille envoie message → apparaît sur l'écran du proche | Isolement |
| `temperature_monitor_extended` | Rappels hydratation toutes les 2h si T° > 32°C | Tous (canicule) |

### 🔵 MODULE V2 (future itération)

| Module | Description |
|--------|-------------|
| `camera_zone_switching` | Multi-caméras couplées à capteurs présence par pièce — grand appartement |

---

## 🧠 LOGIQUE INACTIVITÉ (détail)

### Fenêtres temporelles par profil patient (depuis `patient.md`)

```
Heures actives (8h-12h, 15h-19h)
+ aucun mouvement cuisine / salon / SDB
+ aucun son ambiant
→ 45 min → alerte famille

Heure de sieste (12h-15h)
+ mattress_sensor = ON (personne au lit)
→ pas d'alerte

Heure de sieste
+ mattress_sensor = OFF
+ aucun mouvement 45 min
→ alerte douce

Nuit (22h-8h)
→ pas d'alerte (sommeil normal)

Nuit (22h-8h)
+ mattress_sensor = OFF après 23h
+ aucun mouvement
→ alerte (personne pas couchée)
```

### Capteur matelas
- **Aqara contact sensor (~15€)** entre sommier et matelas
- Poids → contact fermé = `binary_sensor.lit_occupe = ON`
- Natif Zigbee Z2M

---

## 🎥 CAMERA + LLM VISION (détection posture)

### Flow
```
Inactivité détectée (motion sensor)
        ↓
LLM Vision → snapshot caméra (pas de stream continu)
        ↓
Gemini Flash : "La personne est debout, assise ou allongée au sol ?"
        ↓
Data Analyzer → met à jour input_select.posture_patient
        ↓
"au sol" → alerte famille immédiate
"debout/assis" → faux positif, pas d'alerte
```

### YAML de base
```yaml
action: llmvision.data_analyzer
data:
  provider: [gemini_provider_id]
  message: "La personne est-elle debout, assise ou allongée au sol ?"
  image_entity:
    - camera.salon
  entity: input_select.posture_patient
```

### Choix provider AI

| Provider | Vitesse | Coût | Free tier |
|----------|---------|------|-----------|
| **Gemini Flash** ✅ | ⚡⚡ | 0€ | ✅ 1M tokens/jour |
| GPT-4o-mini | ⚡⚡ | ~0.002€/img | ❌ |
| Claude Haiku | ⚡⚡ | ~0.003€/img | ❌ |

**Gemini Flash = choix du projet** (free tier largement suffisant pour usage occasionnel)

---

## 📋 QUESTIONNAIRE (structure)

### Étape 1 — Profil de base
1. La personne vit-elle seule ? (oui/non)
2. Profil principal : Alzheimer/démence · Fragilité physique · Isolement · Post-AVC/maladie chronique
3. A-t-elle du mal à utiliser un téléphone ? (oui/non)

### Étape 2 — Questions par catégorie (oui/non)

| # | Question | Module activé |
|---|----------|---------------|
| **Orientation** |||
| 4 | Se perd-elle dans le temps (heure, jour) ? | `kiosk_screen` |
| 5 | Pose-t-elle des questions répétitives sur les visites ? | `screen_messages` |
| 6 | A-t-elle besoin de voir des photos famille ? | `kiosk_photos` |
| **Sécurité** |||
| 7 | Risque-t-elle de sortir à des heures inhabituelles ? | `door_monitor` |
| 8 | Risque de chute nocturne (chambre → SDB) ? | `night_lighting` |
| 9 | Besoin d'un bouton d'urgence ? | `sos_button` |
| 10 | Reste-t-elle immobile longtemps sans raison ? | `inactivity_monitor` (renforcé) |
| **Santé** |||
| 11 | Oublie-t-elle ses médicaments ? | `medication_reminder` |
| 12 | Oublie-t-elle de manger ? | `meal_reminder` |
| 13 | Oublie-t-elle de se laver ? | `shower_tracking` |
| 14 | Maison potentiellement trop froide / trop chaude ? | `temperature_monitor` (renforcé) |
| **Confort** |||
| 15 | Regarde-t-elle beaucoup la télé ? | `tv_control` |
| 16 | La musique lui fait-elle du bien ? | `music_therapy` |
| 17 | Regarderait-elle des vidéos si c'était simple ? | `youtube_invidious` |
| **Lien social** |||
| 18 | Famille éloignée ou peu disponible ? | `visio_jitsi` |
| 19 | Famille veut suivre son état à distance ? | `family_dashboard` |
| 20 | Famille veut lui envoyer des messages sur l'écran ? | `screen_messages_family` |

### Pré-sélection par profil

| Profil | Modules pré-activés |
|--------|---------------------|
| Alzheimer | `kiosk_screen` `screen_messages` `kiosk_photos` `door_monitor` `music_therapy` `tv_control` `shower_tracking` |
| Fragilité physique | `sos_button` `inactivity_monitor` `night_lighting` `temperature_monitor` `medication_reminder` |
| Isolement | `visio_jitsi` `screen_messages` `family_dashboard` `kiosk_photos` |
| Post-AVC | `medication_reminder` `meal_reminder` `sos_button` `visio_jitsi` |

---

## 📱 INTERFACE FAMILLE (mobile)

### Stack technique
- **Sections view** HA — grid natif mobile-first
- **Mushroom Cards** (HACS) — tiles modernes tap-friendly
- **Browser Mod** (HACS) — popup sur tap
- **Conditional card** — masque les modules inactifs

### Logique d'affichage
```yaml
# Chaque module → un input_boolean
input_boolean.tv_control_active: on/off

# Chaque tile → conditional card
type: conditional
conditions:
  - entity: input_boolean.tv_control_active
    state: "on"
card:
  type: custom:mushroom-template-card
  ...
```

### Layout mobile
```
┌─────────────────────────────┐
│  📹 APPELER MARIE           │  ← Jitsi, TOUJOURS visible
│  • Au salon · 14h32         │
└─────────────────────────────┘
┌──────────┐  ┌──────────┐
│ 🌡️ 24°C  │  │ ✅ Active │  ← Obligatoires, toujours là
└──────────┘  └──────────┘
┌──────────┐  ┌──────────┐
│ 💊 Médoc │  │ 🚿 Douche│  ← Conditionnels selon JSON
└──────────┘  └──────────┘
```

---

## 🏗️ CHAUFFAGE — VARIABLE IMPORTANTE

| Type | Monitoring T° | Contrôle HA |
|------|---------------|-------------|
| Collectif | ✅ Alerte seule | ❌ |
| Grille pain filaire | ✅ | ❌ |
| Grille pain sur prise | ✅ | ⚠️ Prise connectée (vérifier charge) |
| Clim réversible | ✅ | ✅ IR blaster ou natif |
| Radiateur inertie WiFi | ✅ | ✅ (Muller, Intuis, etc.) |

→ Question spécifique dans le questionnaire : **"Quel type de chauffage ?"**

---

## 🛒 APERÇU MATÉRIEL (GÉNÉRATEUR DE BOM)

### Principe

Le questionnaire génère un profil JSON → le site calcule en temps réel les matériels nécessaires et affiche un **aperçu matériel indicatif**.

**Termes retenus :**
- ~~Estimation~~ → **Aperçu matériel**
- ~~Devis~~ → **Ordre de grandeur**
- Toujours accompagné d'un renvoi vers le guide du module concerné

> ⚠️ Cet aperçu dépend de vos réponses. Il peut être incomplet ou inexact si certaines réponses ne correspondent pas exactement à votre situation. Lisez le guide de chaque module avant tout achat.

### Mapping modules → hardware

```json
{
  "module_hardware": {
    "temperature_monitor":  [{"item": "Aqara T°/Humidité", "price": 15}],
    "shower_tracking":      [],
    "door_monitor":         [{"item": "Aqara capteur porte", "price": 15}],
    "inactivity_monitor":   [{"item": "Motion sensor x2", "price": 40}],
    "mattress_sensor":      [{"item": "Aqara contact sensor", "price": 15}],
    "sos_button":           [{"item": "Bouton Zigbee", "price": 20}],
    "camera_monitoring":    [{"item": "Reolink E1", "price": 27}],
    "night_lighting":       [{"item": "Ampoule smart + motion", "price": 45}],
    "tv_control":           [{"item": "IR blaster ou Smart TV", "price": 25}],
    "visio_jitsi":          [{"item": "Capteur présence", "price": 20},
                             {"item": "VPS Jitsi", "price": 60, "type": "annual"}]
  }
}
```

**Règle de déduplication :** `shower_tracking` réutilise le capteur de `temperature_monitor` — pas de doublon dans le BOM.

### Rendu sur le site (temps réel pendant le questionnaire)

```
APERÇU MATÉRIEL — PROFIL MARIE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Basé sur vos réponses · Indicatif uniquement

INFRASTRUCTURE DE BASE
  Mini PC NiPoGi P1 16Go          279€
  Dongle 4G                        25€
  Clé Zigbee (Sonoff)              25€

CAPTEURS MODULES ACTIFS
  Aqara T°/Humidité x2             30€
  Aqara capteur porte              15€
  Motion sensor x2                 40€
  Aqara contact (matelas)          15€
  Bouton SOS Zigbee                20€
  Caméra Reolink E1                27€
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Ordre de grandeur unique          ~476€
Récurrent annuel                  ~100€
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ℹ️ Cet aperçu dépend de vos réponses.
   Lisez le guide de chaque module avant tout achat.
```

Chaque "oui" dans le questionnaire ajoute une ligne en temps réel. La famille voit le coût évoluer et peut ajuster ses choix.

---

## 🌐 VISION FINALE DU PROJET

### Roadmap

```
Phase 1 — Base
├── Docs + tuto par module (comment installer capteur X)
├── YAML par module (même conventions que projet HA Eric)
│   └── ASCII borders, headers, unique_id, slugs
└── GitHub repo public (structure claire, un dossier par module)

Phase 2 — Collaboration
└── Contacter Benjamin Code
    └── Présenter un GitHub avec 2-3 modules documentés AVANT de contacter
    └── Proposition : site internet du projet

Phase 3 — Site web
├── Questionnaire interactif
├── Preview dashboard temps réel (tiles apparaissent selon réponses)
└── Simulation "une journée type"
    ├── 9h → écran kiosque s'allume
    ├── 11h → musique démarre
    ├── 14h → sieste détectée, pas d'alerte
    ├── 16h → inactivité 45min → déclenchement
    ├── Snapshot → Gemini → "allongée au sol"
    └── Jitsi déclenché → famille alertée
```

### Structure GitHub (calquée sur le projet HA Eric)
```
projet-aide-domicile-ha/
├── README.md
├── docs/
│   ├── questionnaire.md
│   ├── hardware.md
│   └── modules/
│       ├── temperature_monitor.md
│       ├── camera_llmvision.md
│       └── ...
├── modules/
│   ├── temperature_monitor/
│   │   ├── sensors.yaml
│   │   ├── automations.yaml
│   │   └── dashboard_card.yaml
│   ├── camera_monitoring/
│   └── ...
└── profil.json (template)
```

---

## 🔗 RESSOURCES CLÉS

- [LLM Vision HACS](https://github.com/valentinfrlch/ha-llmvision) — intégration caméra + AI
- [LLM Vision docs](https://llmvision.org/) — documentation officielle
- [ChrisHansenTech — AI Camera Alerts](https://chrishansen.tech/posts/AI_camera_notification/) — tuto concret
- [Benjamin Code — Skill GitHub](https://gist.github.com/bdebon/2335c1315af44773e673effb25430189) — le prompt de référence

---

## 🖥️ LOGIQUE DASHBOARD TV (décisions UI)

### État par défaut — diaporama photos
- **Plage horaire à configurer dans `profil.json`** (ex: `kiosk_start: "08:00"`, `kiosk_end: "22:00"`)
- Pendant la plage : photos en plein écran en permanence (diaporama auto)
- Hors plage : écran éteint ou horloge seule (à définir par l'aidant)
- Date/heure toujours visible en haut en petit pendant le diaporama

### Photos + musique simultanés
- Diaporama en fond plein écran
- Musique joue en fond (son uniquement) — pas de grosse tuile, juste un bandeau discret en bas si musique active
- Transition propre entre les deux (pas de conflit)

### Visio — condition présence obligatoire
- **Qui peut appeler** : liste blanche famille/proches configurée dans `profil.json` (noms + lien Jitsi personnel)
- **Comment** : l'aidant déclenche depuis son téléphone via l'app HA famille
- **Condition impérative** : la visio ne s'ouvre sur la TV **QUE SI** la personne est détectée dans la même pièce que l'écran (SNZB-06P ou FP2 dans le salon)
- **Si absente de la pièce** → visio bloquée + notification à l'aidant : *"Prénom n'est pas dans le salon"*
- **Pourquoi** : arriver sur un écran de visio dans une autre pièce = désorientation garantie pour une personne Alzheimer
- **Logique HA** :
  ```
  Aidant déclenche appel →
    SI sensor.presence_salon = occupied → Jitsi s'ouvre auto sur TV (plein écran)
    SI sensor.presence_salon = clear → notification aidant "absente du salon" → pas d'ouverture
  ```
- Visio prend tout l'écran (date/heure reste en petit en haut)
- Fermeture visio → retour automatique au diaporama photos

---

## 📝 NOTES D'IMPLÉMENTATION (récupérées du Gist Benjamin + décisions projet)

### `kiosk_photos` — Sync famille via rclone
- **Mécanisme** : dossier Google Drive partagé (famille peut déposer photos librement) → `rclone sync` déclenché chaque nuit (cron) → dossier local `/config/www/photos/`
- **Résultat** : une photo déposée le soir par un petit-enfant apparaît le lendemain sur l'écran. Zéro action côté patient.
- **Outil** : `rclone` (open source, local, pas de cloud HA requis) — à documenter dans `modules/kiosk_photos/README.md`
- **Alternative** : Nextcloud auto-hébergé si la famille refuse Google Drive

### `music_therapy` — Curation stricte, pas de sync famille
- **Choix délibéré** : la musique n'est PAS alimentée par un dossier famille partagé.
- **Pourquoi** : la musique pour une personne âgée/Alzheimer doit être connue, de son époque, apaisante. Un proche qui dépose une mauvaise chanson au mauvais moment ne peut pas être corrigé "en live" → risque de détresse ou d'agitation.
- **Approche** : playlist curatée **une fois** à l'installation par l'aidant principal (genres, années, artistes renseignés dans `profil_template.json`). Modifiable uniquement par l'aidant principal via l'interface HA.
- **⭐ Recommandation forte** : avant d'ajouter un morceau à la playlist, l'aidant doit **l'écouter en entier** pour vérifier qu'il est adapté (tempo, paroles, souvenirs associés positifs ou douloureux). Un morceau non écouté au préalable = risque de réaction imprévue. À documenter comme bonne pratique dans `modules/music_therapy/README.md`.
- **Source musique** : Spotify local (Spotcast), dossier MP3 local, ou Invidious (YouTube sans pub) selon le module `youtube_invidious` activé.

### `kiosk_screen` — Pièges Chromium (retour terrain Benjamin)
- **⚠️ `--disable-gpu` obligatoire** : sans ce flag, l'accélération graphique fige l'écran — y compris l'horloge. L'heure s'arrête sous les yeux du patient. À ajouter dans la commande de lancement Chromium dès le départ.
- **⚠️ Watchdog obligatoire** : si la page plante (HA redémarre, réseau coupe), le kiosque doit se relancer automatiquement. Sans ça, un écran d'erreur peut rester des heures visible. Implémenter un script watchdog (heartbeat toutes les 60s → si page morte → `pkill chromium && relaunch`).
- Ces deux points sont **à documenter dans `modules/kiosk_screen/README.md`** comme prérequis installation.
- [Invidious](https://invidious.io/) — frontend YouTube self-hosted
- [Jitsi Meet](https://jitsi.org/) — visio self-hosted
- [Cloudflare Tunnel](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/) — accès distant sans VPN

---

*Document généré en session — 2026-06-30*
*Projet en cours de structuration — V1 non encore codée*
