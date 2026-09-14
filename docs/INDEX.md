# INDEX — Projet Assistant au Personne
*Dernière mise à jour : 2026-09-14 (soirée — **BUG de suppression RDV/récurrences résolu** : le WebSocket de `aidant.html` s'authentifiait avec `ha_token` (souvent vide) au lieu de la session HA (`currentToken()`) — corrigé v14.4, validé en direct sur le navigateur de l'utilisateur ; **sauvegarde GitHub opérationnelle** (dépôt git sur `Z:\` + push auto H+10) ; également : automation des récurrences réparée, anti-doublon ×3, auto-mise à jour de l'interface) — Session précédente : 2026-08-15 (même jour, suite, DÉFINITIF) — les 3 pages dédiées `calendrier.html`/`video.html`/`photos.html` sont **confirmées fonctionnelles en direct** par l'utilisateur (PIN, galerie, suppression, upload). L'upload photo a nécessité un diagnostic complet : 401 persistant → cause réelle = route officielle HA réservée aux comptes admin (`local_source.py`) → contournement `shell_command.m31_photos_televerser_{debut,chunk,fin}` construit (upload par morceaux, écrit directement sur disque, fonctionne pour un compte non-admin) → confirmé en direct, y compris depuis le téléphone (app Companion Android). Voir `M31_photos.md` pour le détail complet du diagnostic. Session précédente (même jour, plus tôt) : bug `?return_response=true` corrigé ; 3 pages dédiées créées ; fiche M10_gestion_aidants.md créée (rattrapage M04→M10) ; Confo_M31 Photos rotation construite ; Confo_M33 Visio unifié. Session du 14/08 : Confo_M34 Télévision fiabilisée + oblig_M03 Écran Messages clos.*

---

## ⚡ ACCÈS RAPIDE

| Document | Rôle |
|:---------|:-----|
| [`DEPENDANCES_GLOBALES.md`](DEPENDANCES_GLOBALES.md) | Chaînes de dépendances, statuts, entités, table de correspondance ancien/nouveau numéro |
| [`PLAN_RENOMMAGE_MODULES.md`](PLAN_RENOMMAGE_MODULES.md) | Plan de renommage complet des entity_id Mxx → nouvelle numérotation (non exécuté) |
| [`RENOMMAGE_TABLE.md`](RENOMMAGE_TABLE.md) | Ledger 2 colonnes origine/nouveau, mis à jour au fur et à mesure de l'exécution |
| [`00_IA/IA_CONTEXT_BASE_AI.md`](00_IA/IA_CONTEXT_BASE_AI.md) | Contexte IA — à lire en premier |
| [`05_projet/CAHIER_DES_CHARGES.md`](05_projet/CAHIER_DES_CHARGES.md) | Référence fonctionnelle |
| [`05_projet/hardware.md`](05_projet/hardware.md) | Matériel + coûts |

---

## 🗂️ ÉTAT DES MODULES (numérotation par groupe, 2026-08-13)

> Voir [`DEPENDANCES_GLOBALES.md`](DEPENDANCES_GLOBALES.md) pour la table de correspondance
> complète ancien/nouveau numéro et les chaînes de dépendances détaillées.

### Obligatoires

| Module | Fiche doc | YAML local | Statut |
|:-------|:----------|:-----------|:-------|
| **oblig_M01** Temp & Hygro | [M01_temp_hygro.md](03_modules_packages/05_confort/M01_temp_hygro.md) | `raspi/packages/m01_temp_hygro.yaml` | ✅ Déployé |
| **oblig_M02** Détection Inactivité | [M02_inactivite.md](03_modules_packages/02_securite_alerte/M02_inactivite.md) | `raspi/packages/m02_inactivite.yaml` | ✅ Développé — non testé conditions réelles 🔴 |
| **oblig_M03** Écran Messages | [M03_ecran_msg.md](03_modules_packages/03_communication/M03_ecran_msg.md) | `raspi/packages/oblig_m03_ecran_msg/m03_ecran_msg.yaml` | ✅ Clos 14/08 — page dédiée `calendrier.html` ajoutée 15/08 ; **RDV & récurrences réparés et testés en direct les 13-14/09** (automation, anti-doublon, suppression WebSocket, fix token v14.4) |

### Secur (Sécurité)

| Module | Fiche doc | YAML local | Statut |
|:-------|:----------|:-----------|:-------|
| **Secur_M10** SOS | [M04_sos.md](03_modules_packages/02_securite_alerte/M04_sos.md) | `raspi/packages/m04_sos.yaml` | 🧪 Simulation, notif push manquante 🔴 |
| **Secur_M10** Gestion aidants (droits + PIN pages dédiées) | [M10_gestion_aidants.md](03_modules_packages/02_securite_alerte/M10_gestion_aidants.md) | `raspi/packages/secur_m10_sos/m10_gestion_aidants.yaml` | ✅ Ajout PIN 15/08 — fiche renommée M04→M10 (rattrapage, mirror docs stale) |
| **Secur_M11** Capteur Lit | [M05_capteur_lit.md](03_modules_packages/02_securite_alerte/M05_capteur_lit.md) | `raspi/packages/m05_capteur_lit.yaml` | 🧪 Simulation 🟡 |
| **Secur_M12** Caméra IA | — | — | ❌ À faire 🔴 |
| **Secur_M13** Porte Ext (S) | [M15_porte_ext.md](03_modules_packages/02_securite_alerte/M15_porte_ext.md) | `raspi/packages/m15_porte_ext.yaml` | ⚠️ 1 porte/plusieurs 🔴 |
| **Secur_M14** Fenêtres (S) | — | — | ❌ À faire 🟡 |
| **Secur_M15** Frigo | — | — | ❌ À faire, pas de toggle 🟡 |
| **Secur_M16** Congélateur | — | — | ❌ À faire, pas de toggle 🟡 |
| **Secur_M17** Veilleuse Nuit | — | — | ❌ À faire 🟡 |

### Santé

| Module | Fiche doc | YAML local | Statut |
|:-------|:----------|:-----------|:-------|
| **Santé_M20** Médicaments (affiché « M13 ») | [M13_medoc.md](03_modules_packages/02_securite_alerte/M13_medoc.md) | `raspi/packages/m20_medoc.yaml` | ✅ Rappel construit (4 zones, off par défaut) — 16/08 |
| ~~**Santé_M21** Repas~~ | — | — | 🚫 **Abandonné 16/08** (signal non fiable, voir CDC §8) |
| **Santé_M22** Douche | — | — | ❌ À faire 🟡 |

### Confo (Confort & Loisirs)

| Module | Fiche doc | YAML local | Statut |
|:-------|:----------|:-----------|:-------|
| **Confo_M30** Kiosk Écran | — | `raspi/dashboards/dashboard_kiosk.yaml` | ✅ Dashboard (pas de logique séparée) |
| **Confo_M31** Photos Famille | [M31_photos.md](03_modules_packages/04_divertissement/M31_photos.md) | `raspi/packages/m31_photos.yaml` | ✅ Rotation, galerie, suppression et upload (compte non-admin, contournement `shell_command`) **tous confirmés en direct** 15/08 |
| **Confo_M32** Musique | [M32_musique.md](03_modules_packages/04_divertissement/M32_musique.md) | `raspi/packages/confo_m32_musique/m32_musique.yaml` | ✅ Phase 1 construite 13/09 (4 créneaux, liens YouTube, règles de conflit TV) — phase 2 (lecture kiosk) à faire 🟢 |
| **Confo_M33** Visio | [M33_visio.md](03_modules_packages/03_communication/M33_visio.md) | `raspi/packages/m33_visio.yaml` | ✅ WebRTC maison uniquement — **Google Meet retiré le 13/09** (`input_text.m33_visio_url` supprimée) |
| **Confo_M34** Télévision | [M34_television.md](03_modules_packages/04_divertissement/M34_television.md) | `raspi/packages/confo_m34_television/` | ✅ Déployé et fiabilisé 14/08 — page dédiée `video.html` ajoutée 15/08, **confirmée fonctionnelle** |

*\* fiche M11_tv.md remplacée par [M34_television.md](03_modules_packages/04_divertissement/M34_television.md) le 14/08 (archivée en local, architecture navigateur/browser_mod abandonnée au profit de kiosk.html en HTML pur).*

### Envir (Environnement)

| Module | Fiche doc | YAML local | Statut |
|:-------|:----------|:-----------|:-------|
| **Envir_M40** Chauffage | — | — | ❌ Stand-by 🟢 |

---

## 🖥️ DASHBOARDS

| Dashboard | YAML local | Statut |
|:----------|:-----------|:-------|
| Kiosk (occupant) | `raspi/dashboards/dashboard_kiosk.yaml` | ✅ Actif |
| Interface Aidant | `raspi/dashboards/dashboard_aidant.yaml` | ✅ Actif — simplifié 13/08 (iframe → `aidant.html`, ancien en `.bak`) |
| ~~Configuration~~ | `raspi/dashboards/dashboard_modules.yaml` | ⛔ Retiré 13/08 — archivé en local, remplacé par `config.html` |
| Test / Simulation | `raspi/dashboards/dashboard_test_simulation.yaml` | ✅ Actif |

**Interface aidant — tranché le 13/08 :** `aidant.html` (HTML custom) retenu. Le dashboard natif v2 (`lovelace-aidant-v2`) a été retiré de `configuration.yaml`, archivé en local (`raspi/_archive/2026-08-13_nettoyage_bak/dashboards/`).

---

## 🔄 PROTOCOLE DE MISE À JOUR

**À chaque modification d'un YAML dans `raspi/` :**
1. Pousser vers `Z:\` (avec vérification MD5)
2. Mettre à jour la fiche `.md` correspondante dans `docs/03_modules_packages/`
3. Mettre à jour `docs/DEPENDANCES_GLOBALES.md` si les entités ou dépendances ont changé
4. Mettre à jour ce fichier si le statut du module a changé
5. Copier le YAML mis à jour dans `docs/03_modules_packages/<categorie>/`
6. Lancer `python sync_docs.py` (racine du projet) pour pousser `docs/` → `Z:\docs\`

**Rechargements HA selon le type de fichier :**
| Type | Rechargement requis |
|:-----|:--------------------|
| `template:` | Outils dev → YAML → Recharger les templates |
| `automation:` | Outils dev → YAML → Recharger les automations |
| `script:` | Outils dev → YAML → Recharger les scripts |
| `input_text/boolean/number/datetime/select:` | Redémarrage HA complet |
| `timer:` | Redémarrage HA complet |
| Dashboard YAML | Outils dev → YAML → Recharger la configuration Lovelace |
