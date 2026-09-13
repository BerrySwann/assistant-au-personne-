# 🏠 Assistant au Personne — Domotique Modulaire pour le Maintien à Domicile

> Mettre la technologie au service de ceux qui en ont besoin.
> Home Assistant modulaire, capteurs Zigbee, IA locale — pour garder un proche à domicile le plus longtemps possible.

---

## 🎯 C'est quoi ce projet ?

Un système domotique open source basé sur **Home Assistant**, conçu pour aider les aidants familiaux à maintenir un proche en difficulté à domicile dans les meilleures conditions.

**Principe :** Un questionnaire génère un profil personnalisé qui active uniquement les modules dont votre proche a besoin. Pas de sur-équipement, pas de complexité inutile.

**Inspiré du projet de [Benjamin Code](https://www.youtube.com/@benjamincode)** pour sa mère atteinte d'Alzheimer.

---

## 👥 Pour qui ?

| Profil | Besoins principaux |
|--------|-------------------|
| **Alzheimer / Démence** | Orientation, musique, TV douce, suivi sorties |
| **Fragilité physique** | SOS, détection inactivité, éclairage nocturne |
| **Isolement** | Visio famille, photos, messages |
| **Post-AVC / Maladie chronique** | Rappels médicaments, repas, lien social |

---

## 🧱 Modules disponibles

### 🔴 Obligatoires (toujours actifs)
- `temperature_monitor` — Alerte chaleur (canicule) ET froid dangereux
- `inactivity_monitor` — Détection d'inactivité anormale avec logique temporelle
- `screen_messages` — Affichage heure, date, messages de base

### 🟠 Fortement recommandés
- `camera_monitoring` + `llm_vision` — Détection de chute via IA (snapshot uniquement)
- `sos_button` — Bouton d'urgence Zigbee
- `mattress_sensor` — Capteur de présence au lit

### 🟡 Optionnels (selon profil)
- `kiosk_screen` / `kiosk_photos` — Écran permanent + diaporama famille
- `tv_control` — Chaîne calme automatique + volume fixe
- `music_therapy` — Playlists souvenirs à heure fixe
- `youtube_invidious` — Vidéos sans publicité (Invidious self-hosted)
- `visio_jitsi` — Appel vidéo sans action côté patient
- `shower_tracking` — Suivi hygiène (capteur humidité)
- `medication_reminder` / `meal_reminder` — Rappels santé
- `door_monitor` — Alerte sortie hors horaires
- `night_lighting` — Éclairage nocturne automatique
- `family_dashboard` — Vue famille à distance

---

## 💰 Budget

| | Coût |
|--|------|
| **Hardware (unique)** | 800 — 1 000 € |
| **Récurrent annuel** | ~100 €/an |

*Voir [docs/hardware.md](docs/hardware.md) pour le détail complet.*

---

## 🖥️ Stack technique

| Composant | Solution |
|-----------|----------|
| OS | HAOS (Home Assistant OS) |
| Zigbee | Zigbee2MQTT |
| YouTube | Invidious (Docker, self-hosted) |
| Visio | Jitsi (VPS) |
| Accès famille | Cloudflare Tunnel |
| Vision IA | LLM Vision (HACS) + Gemini Flash |
| Dashboard | Mushroom Cards + Browser Mod |

---

## 🚀 Par où commencer ?

1. **[Questionnaire](docs/questionnaire.md)** — Identifiez les besoins de votre proche
2. **[Hardware](docs/hardware.md)** — Liste du matériel selon votre profil
3. **[Installation](docs/installation.md)** — Guide pas à pas
4. **[Modules](modules/)** — Un dossier par module, avec YAML + doc

---

## 🤝 Contribuer

Ce projet est ouvert à tous. Voir [CONTRIBUTING.md](CONTRIBUTING.md).

---

## ⚠️ Avertissement

Ce système est un outil d'aide, pas un dispositif médical certifié.
Il ne remplace pas une téléassistance professionnelle ni un suivi médical.
Pour les risques de chute élevés, consultez les services de téléassistance dédiés.

---

*Projet open source — Licence MIT*
