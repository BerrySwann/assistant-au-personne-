# DÉPENDANCES GLOBALES — Système Aidant HA
*Dernière mise à jour : 2026-07-04*

---

## 📐 STRUCTURE DU PROJET

```
Assitant au personne/
├── dependances.md          ← ce fichier
├── hardware.md             ← matériel + coûts
├── raspi/                  ← YAML déployés sur le RPi4 (source de vérité)
│   ├── configuration.yaml
│   ├── packages/           ← un fichier par module
│   └── dashboards/         ← dashboards Lovelace YAML
└── Docs/                   ← documentation par module
    ├── packages/           ← fiche technique de chaque package
    └── dashboards/         ← fiche technique de chaque dashboard
```

---

## 🔗 CHAÎNE DE DÉPENDANCES GLOBALE

### M00 — Interrupteurs Modules

| FICHIER | ENTITÉ PRODUITE | CONSOMMÉE PAR |
|:--------|:----------------|:--------------|
| raspi/packages/m00_modules.yaml | `input_boolean.module_temp_hygro` | packages/m01, dashboards/modules |
| raspi/packages/m00_modules.yaml | `input_boolean.module_inactivite` | dashboards/modules |
| raspi/packages/m00_modules.yaml | `input_boolean.module_ecran_msg` | packages/m03, dashboards/modules |
| raspi/packages/m00_modules.yaml | `input_boolean.module_porte_ext` | packages/m15, dashboards/modules |
| raspi/packages/m00_modules.yaml | `input_boolean.module_*` (×20) | dashboards/modules |
| raspi/packages/m00_modules.yaml | `sensor.time` / `sensor.date_time` | dashboards/kiosk (horloge) |

---

### M01 — Température & Hygrométrie

| MATÉRIEL | CAPTEUR BRUT (source) | ENTITÉ PRODUITE (unique_id) | AVAL |
|:---------|:----------------------|:----------------------------|:-----|
| SONOFF SNZB-02D (Z2M) | `sensor.snzb02d_salon_temperature` | `m01_temp_salon_min_24h` | templates M01 → aidant |
| SONOFF SNZB-02D (Z2M) | `sensor.snzb02d_salon_temperature` | `m01_temp_salon_max_24h` | templates M01 → aidant |
| SONOFF SNZB-02D (Z2M) | `sensor.snzb02d_salon_humidity` | `m01_hygro_salon_avg_24h` | templates M01 → aidant |
| SONOFF SNZB-02D (Z2M) | `sensor.snzb02d_chambre_temperature` | `m01_temp_chambre_min_24h` | templates M01 (aucun aval kiosk depuis 2026-07-04) |
| SONOFF SNZB-02D (Z2M) | `sensor.snzb02d_chambre_temperature` | `m01_temp_chambre_max_24h` | templates M01 (aucun aval kiosk depuis 2026-07-04) |
| [calculé] | `sensor.m01_temp_salon_min/max_24h` | `m01_alerte_temperature` | dashboards/aidant (chips) |
| [calculé] | `sensor.snzb02d_salon_humidity` | `m01_alerte_humidite` | dashboards/aidant |
| [calculé] | `sensor.m01_temp_salon_min/max_24h` | `m01_resume_temp_salon` | dashboards/aidant |
| [calculé] | `sensor.m01_temp_chambre_min/max_24h` | `m01_resume_temp_chambre` | dashboards/aidant |

**⚠️ Changement 2026-07-04 :** le bloc Température/Hygro a été retiré de `dashboard_kiosk.yaml` (demande utilisateur). Ces entités ne sont plus consommées que par `dashboard_aidant.yaml`.

**Fichier source :** `raspi/packages/m01_temp_hygro.yaml`
**Statut :** ✅ Déployé

---

### M03 — Écran Messages

| SOURCE | ENTITÉ | RÔLE | AVAL |
|:-------|:-------|:-----|:-----|
| Saisie famille (app HA) | `input_text.m03_message_famille` | Texto entrant | template m03_texto_formate |
| Saisie famille (app HA) | `input_text.m03_message_auteur` | Auteur du texto | template m03_texto_formate |
| Auto (automation) | `input_datetime.m03_message_envoi` | Horodatage envoi | template m03_texto_formate |
| Config admin | `input_number.m03_message_duree_h` | Durée affichage (48h) | template m03_texto_formate |
| Google Calendar | `calendar.google_agenda_famille` | Événements agenda | template m03_agenda_formate |
| [calculé] | `sensor.m03_agenda_formate` | Délai formaté (demain/dans 2h…) | m03_bandeau_principal, dashboards/kiosk (bloc 2 — Rappels) |
| [calculé] | `sensor.m03_texto_formate` | Message famille formaté | m03_bandeau_principal, dashboards/kiosk (bloc 3 — Messages texto) |
| [calculé] | `sensor.m03_bandeau_principal` | Texte final à afficher | dashboards/aidant (chip statut) |

**Fichier source :** `raspi/packages/m03_ecran_msg.yaml`
**Automations** : 3 (à saisir dans UI HA — voir [`Docs/packages/M03_automations.md`](Docs/packages/M03_automations.md))
**Statut :** ✅ Déployé (sans Google Calendar — intégration à configurer)

**⚠️ Changement 2026-07-04 :** `dashboard_kiosk.yaml` consomme désormais directement `sensor.m03_agenda_formate` et `sensor.m03_texto_formate` (au lieu de `m03_bandeau_principal`). `m03_bandeau_principal` reste utilisé uniquement par `dashboard_aidant.yaml`.

---

### M08 — Photos Famille

| SOURCE | ENTITÉ | RÔLE | AVAL |
|:-------|:-------|:-----|:-----|
| M00 (existant) | `input_boolean.module_kiosk_foto` | Marche/arrêt module (déclaré dans m00_modules.yaml, PAS redéclaré ici) | ⚠️ orphelin depuis 2026-07-04 — plus consommé par le kiosk (remplacé par sensor.m11_etat_global), ni par le script M08 |
| Config admin | `input_text.m08_photos_dossier` | Dossier photos (media_source, réservé future rotation) | — pas encore consommé |
| Config admin | `input_number.m08_photos_intervalle_s` | Intervalle diaporama (réservé future rotation) | — pas encore consommé |
| — | `script.m08_lancer_diaporama` | Retour navigateur TV → dashboard kiosk (`browser_mod.navigate`) | appelé par m11_tv.yaml (fin de créneau TV) |

**Fichier source :** `raspi/packages/m08_photos.yaml`
**Statut :** ✅ Déployé (2026-07-04, Z:\packages\m08_photos.yaml, MD5 vérifié) — mécanisme Browser Mod confirmé ; la vraie rotation d'images dans le bloc 4.1 du kiosk reste un placeholder statique à construire.

**⚠️ Révision 2026-07-04 :** Chromecast et PhotoFrameCast abandonnés — remplacés par `browser_mod.navigate` (confirmé, doc officielle Browser Mod).

---

### M11 — Télévision (3 sessions configurables)

**⚠️ Révision 2026-07-04 (v2) :** structure créneau1(EPG)/créneau2(fixe) **entièrement remplacée** par 3 sessions identiques et indépendamment activables, à la demande de l'utilisateur ("calendrier" TV, 3 max, chacune on/off).

| SOURCE | ENTITÉ | RÔLE | AVAL |
|:-------|:-------|:-----|:-----|
| M00 (existant) | `input_boolean.module_television` | Marche/arrêt module | conditionne les 2 automations |
| **Config admin — SÉCURITÉ** | `input_text.m11_browser_id_tv` | Browser ID du navigateur TV — **vide = tout désactivé** (sinon un appel non ciblé toucherait TOUS les navigateurs Browser Mod enregistrés, y compris les téléphones famille) | conditionne script.m11_lancer_session et script.m08_lancer_diaporama |
| Config admin | `input_boolean.m11_session{1,2,3}_actif` | Active/désactive chaque session indépendamment | sensor.m11_etat_global |
| Config admin | `input_datetime.m11_session{1,2,3}_debut/fin` | Heures cibles par session (fallback si pas d'EPG, ou horaire fixe si YouTube) | sensor.m11_session{N}_fenetre |
| Config admin | `input_select.m11_session{1,2,3}_chaine` | Chaîne par session (France 2/Arte/France 5/YouTube) | script.m11_lancer_session + détermine l'entité EPG utilisée |
| Config admin | `input_text.m11_session{1,2,3}_youtube_url` | URL vidéo YouTube propre à chaque session (si chaîne = YouTube) | script.m11_lancer_session |
| Config admin | `input_text.m11_url_france2/arte/france5` | URLs "direct" des chaînes, **partagées entre les 3 sessions** (à vérifier, structure site web) | script.m11_lancer_session |
| Config admin | `input_number.m11_marge_recherche_min` / `m11_marge_fin_min` | Marges de tolérance EPG, partagées entre les 3 sessions | sensor.m11_session{N}_fenetre |
| [calculé] | `sensor.m11_session{1,2,3}_fenetre` | `debut_reel`/`fin_reelle` par session — EPG si chaîne TV, horaire fixe si YouTube | sensor.m11_etat_global |
| [calculé] | `sensor.m11_etat_global` | État courant (`desactive`/`session1`/`session2`/`session3`/`photos`) + attribut `texte_affichage` | dashboards/kiosk (bloc 4 — état écran) |
| — (interne) | `input_text.m11_session_affichee` | Mémorise la session actuellement affichée pour ne déclencher qu'au **changement** d'état (remplace les anciens `_en_cours` booléens ×2) | automation m11_verifier_sessions |

**Fichier source :** `raspi/packages/m11_tv.yaml`
**Automations** : 2 (au lieu de 4) — `m11_verifier_sessions` (poll 1×/min, ne relance un script qu'au changement d'état) et `m11_reset_desactivation` (retour photos si module coupé). Actuellement **dans le package YAML** (`automation:` block), pas saisies manuellement dans l'UI — ⚠️ **rupture de convention par rapport à M03**, toujours pas tranchée avec l'utilisateur.
**Statut :** ✅ Déployé et **testé en conditions réelles** (2026-07-04, Z:\packages\m11_tv.yaml, MD5 vérifié) — `sensor.m11_etat_global` confirmé fonctionnel sur le kiosk après correction d'un bug bloquant (voir `Docs/packages/M11_tv.md` § "Bug corrigé").

1. `input_text.m11_browser_id_tv` pré-rempli avec le Browser ID réel. Reste à renseigner les URLs YouTube par session (`input_text.m11_session{1,2,3}_youtube_url`) depuis l'UI selon les besoins.
2. **Choix technique fait sans confirmation explicite de l'utilisateur, à valider** : plutôt que d'abandonner l'EPG pour un horaire fixe uniforme sur les 3 sessions (ce qui réintroduirait le risque de "couper un programme en cours" que l'EPG était censé résoudre), j'ai généralisé la logique EPG à chaque session — l'entité EPG est désormais **dérivée automatiquement** de la chaîne choisie dans `input_select.m11_sessionN_chaine` (fini le champ manuel `m11_epg_entity_creneau1` qui pouvait désynchroniser). Seules les sessions réglées sur YouTube utilisent un horaire strictement fixe (logique inchangée, car durée vidéo connue). **À confirmer avec l'utilisateur** : c'est bien ce qui était voulu par "3 créneaux identiques", ou une logique 100% horaire fixe (plus simple, mais réintroduisant le risque de coupure) était attendue ?
3. Valeurs par défaut des 3 sessions (à ajuster) : Session 1 = France 2, 13h-15h, active ; Session 2 = YouTube, 19h-19h20, active ; Session 3 = France 2, 10h-10h30, **inactive** (désactivée par défaut, sert d'exemple/gabarit).
4. EPG : XMLTV EPG installée, source `https://xmltvfr.fr/xmltv/xmltv_tnt.xml.gz`. Entités vérifiées : `sensor.france2_fr_program_current`, `sensor.arte_fr_program_current`, `sensor.france5_fr_program_current`, attributs `start`/`end` (ISO 8601). Garde-fou fenêtre `[cible ± marge_recherche]` conservé (sans lui, l'automation se caler sur n'importe quel programme en cours de diffusion, pas nécessairement celui visé).
5. Navigation par `browser_mod.javascript` (`window.location.href`) vers une URL externe — mécanisme JS standard plausible, **non testé en conditions réelles**.
6. URLs "direct" France 2/Arte/France 5 : correctes au 2026-07-04 mais peuvent changer sans préavis.

**⚠️ Révision 2026-07-04 :** Chromecast/Google Cast abandonné (aucun app_id confirmé trouvé) — remplacé par navigation navigateur (Browser Mod) sur le mini-PC/RPi4 en HDMI. EPG XMLTV installée et validée pour caler le créneau 1 sur le vrai horaire de programme.

---

### M15 — Porte Extérieure

| MATÉRIEL | CAPTEUR BRUT | ENTITÉ PRODUITE | AVAL |
|:---------|:-------------|:----------------|:-----|
| SONOFF SNZB-04P (Z2M) | `binary_sensor.snzb04p_porte_ext_contact` | `m15_porte_ext_duree_ouverture` | dashboards/aidant |
| Reolink E1 Pro (WiFi) | `camera.reolink_e1_pro` | (natif HA) | dashboards/aidant (WebRTC) |

**⚠️ Logique inversée :** `state: off` = porte **ouverte**, `state: on` = porte **fermée**
**Fichier source :** `raspi/packages/m15_porte_ext.yaml`
**Statut :** ✅ Sensor déployé — templates + automations à faire

---

## 🖥️ DASHBOARDS

| FICHIER | TITRE | TYPE | ENTITÉS CONSOMMÉES |
|:--------|:------|:-----|:-------------------|
| `raspi/dashboards/dashboard_kiosk.yaml` | Kiosk TV | panel + vertical-stack (1 colonne) | sensor.date_time, sensor.m03_agenda_formate, sensor.m03_texto_formate, sensor.m11_etat_global |
| `raspi/dashboards/dashboard_aidant.yaml` | Interface Aidant | panel | m01_alerte_*, m03_*, snzb04p_porte_ext, media_player.chromecast_salon |
| `raspi/dashboards/dashboard_modules.yaml` | Configuration | panel | input_boolean.module_* (×20) + réglages M11 (input_boolean.m11_session{1,2,3}_actif, input_select.m11_session{1,2,3}_chaine, input_datetime.m11_session{1,2,3}_debut/fin, input_text.m11_session{1,2,3}_youtube_url, input_text.m11_browser_id_tv/m11_url_france2/arte/france5, input_number.m11_marge_recherche_min/m11_marge_fin_min) |

---

## 📦 HACS INSTALLÉ

| Carte | Usage |
|:------|:------|
| Mushroom | Cartes modernes (entity, template, chips, title) |
| Button Card | Boutons custom CSS (kiosk horloge, actions rapides) |
| card-mod | CSS override (`background: none !important`) |
| Browser Mod | Plein écran TV (`browser_mod.toggle_fullscreen`, kiosk bloc 4.2) + navigation/JS pour M08/M11 (`browser_mod.navigate`, `browser_mod.javascript`) — confirmé installé le 2026-07-04 |

---

## 📦 HACS INSTALLÉ (suite)

| Intégration | Usage | Statut |
|:-------------|:------|:-------|
| [XMLTV EPG](https://github.com/shadow578/homeassistant_xmltv-epg) (dépôt custom) | Calage créneau 1 (M11) sur le vrai horaire de programme. Source : `https://xmltvfr.fr/xmltv/xmltv_tnt.xml.gz` | ✅ Installée et vérifiée le 2026-07-04 (France 2/Arte/France 5) |

---

## 🚧 MODULES EN ATTENTE (non déployés)

| Module | Statut | Priorité |
|:-------|:-------|:---------|
| M02 Inactivité | ⚠️ Draft écrit (2026-08-05), non pairé, non testé — voir raspi/packages/m02_inactivite.yaml | 🔴 Critique |
| M04 SOS | ⚠️ Draft écrit (2026-08-05), non pairé, non testé — voir raspi/packages/m04_sos.yaml | 🔴 Critique |
| M05 Capteur Lit | ⚠️ Draft écrit (2026-08-05), non pairé, non testé — voir raspi/packages/m05_capteur_lit.yaml | 🟡 Important |
| M06 Caméra IA | ❌ À faire | 🔴 Critique |
| M07 Kiosk Écran | ❌ À faire | 🟡 Important |
| M08 Photos Famille | ⚠️ Partiel — retour kiosk OK, vraie rotation photos à construire | 🟡 Important |
| M09 Musique | ❌ À faire | 🟢 Optionnel |
| M10 Visio | ❌ À faire | 🟡 Important |
| M11 Télévision | ⚠️ Partiel — EPG confirmée, navigation Browser Mod à tester | 🟡 Important |
| M12 Douche | ❌ À faire | 🟡 Important |
| M13 Médoc | ❌ À faire | 🔴 Critique (Alzheimer) |
| M14 Repas | ❌ À faire | 🟡 Important |
| M15 templates+automations | ⚠️ Partiel | 🔴 Critique |
| M16 Veilleuse Nuit | ❌ À faire | 🟡 Important |
| M17 Chauffage | ❌ Stand-by | 🟢 Optionnel |
| M18 Fenêtres | ❌ Stand-by | 🟢 Optionnel |
| M19 Dashboard Famille | ❌ À faire | 🔴 Critique |
| M20 Messages Famille | ❌ À faire | 🟡 Important |
