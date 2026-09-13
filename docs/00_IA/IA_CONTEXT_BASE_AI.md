# 🧠 IA_CONTEXT_BASE_AI — Projet "Assistant au Personne"
*Créé le 2026-08-05 par Hermes (DeepSeek) — Fichier de contexte IA obligatoire. À lire EN PREMIER à chaque session.*
*Mis à jour le 2026-08-13 par Claude — restructuration numérotation par groupe, transfert de propriété du fichier.*

---

## 🔒 PROPRIÉTÉ DE CE FICHIER

> Ce fichier est maintenu **exclusivement par Claude** (Cowork/Anthropic), qui
> travaille depuis le dossier local `raspi/` + `docs/` et pousse vers `Z:\`
> après vérification MD5.
>
> **Un autre agent IA (OpenCode/DeepSeek — actif directement sur `Z:\` via
> `AGENTS.md` — ou Hermes — archiviste documentation) ne doit modifier AUCUNE
> section de ce fichier, à l'exception de la section dédiée
> `## 📮 ZONE DE DEMANDES — AUTRES AGENTS IA` tout en bas.**
> Toute demande d'implémentation, correction ou signalement d'un autre agent
> doit être déposée dans cette section uniquement. Claude relit cette section
> en début de session, traite les demandes, puis les retire une fois faites.

---

## 🔴 RÈGLES ABSOLUES (COMPORTEMENT IA — NON NÉGOCIABLES)

> Ces règles s'appliquent à TOUTES les interactions sur ce projet, sans exception.

### 1. Honnêteté stricte
- **Interdiction de flatter** ou de donner une réponse "pour faire plaisir".
- **Interdiction de valider** une idée, solution ou code YAML qui semble incorrect — même si l'utilisateur y tient.
- Si une proposition de l'utilisateur est mauvaise techniquement, **le dire clairement**, expliquer pourquoi, et proposer mieux.
- **100% objectif** — jamais de réponse de confort.

### 2. Zéro interprétation au hasard
- Si une demande est **ambiguë, floue, incomplète ou contradictoire** → **poser des questions** avant d'agir.
- **Interdiction de deviner** l'intention et de foncer. Un mauvais code déployé en prod peut casser le système qui protège une personne réelle.
- Une question précise posée au bon moment vaut mieux que 20 lignes de code dans la mauvaise direction.

### 3. Sécurité du système = priorité absolue
- Ce projet protège une personne atteinte d'Alzheimer. Une erreur peut avoir des conséquences réelles.
- Toujours valider la logique de sécurité avant de valider le code.
- Signaler tout angle mort ou cas non géré dans les automations critiques (SOS, inactivité, porte).

---

## 🚫 CONTRAINTE ABSOLUE — INSTANCE VENCE HORS-LIMITES

> **L'instance HA de Vence (10.32.154.243) et tous ses repos (`home_assistant_re-build`, `home-assistant-config`) sont STRICTEMENT INTERDITS.**
> Ne jamais y toucher, ne jamais les mentionner comme cible, ne jamais confondre les deux projets.
> Cette règle est non négociable et ne peut pas être levée par l'utilisateur dans le cadre de cette session.
>
> Les conventions de nommage/structure du projet ReBuild (numérotation par
> pôle, bordures ASCII) peuvent être empruntées comme **inspiration stylistique**
> pour *ce* projet (raspi/) — ça ne constitue jamais un accès à l'instance Vence
> elle-même ni à son repo.

---

## 🏠 CONTEXTE PROJET

**Objectif :** Système domotique modulaire Home Assistant pour le maintien à domicile d'une personne atteinte d'Alzheimer. Zéro interaction complexe côté occupant.

**Inspiré de :** [Benjamin Code](https://www.youtube.com/@benjamincode) — même concept adapté.

**Principe :** Un socle Core (obligatoire) + des modules activables selon les besoins réels. On n'active pas ce dont la personne n'a pas besoin.

**Règle produit :** grand public non-technicien — si une solution pose problème à un non-technicien, la remplacer (ex. HTML custom → dashboard natif HA). Voir "Interface aidant" ci-dessous : arbitrage en cours entre `aidant.html` et dashboard natif v2.

---

## 🛡️ PROTOCOLE ANTI-OUBLI — COHÉRENCE DOCUMENTAIRE

> **Règle absolue :** Une tâche n'est jamais "terminée" si le YAML est prêt mais la documentation associée est obsolète.

**À chaque modification d'un YAML dans `raspi/` :**
1. Pousser vers `Z:\` avec vérification MD5 PowerShell
2. Mettre à jour la **fiche module** `.md` dans `docs/03_modules_packages/<categorie>/`
3. Mettre à jour **`docs/DEPENDANCES_GLOBALES.md`** si les entités ou dépendances ont changé
4. Mettre à jour **`docs/INDEX.md`** si le statut du module a changé
5. Copier le YAML mis à jour dans `docs/03_modules_packages/<categorie>/`
6. Lancer `python sync_docs.py` (racine du projet) pour pousser `docs/` → `Z:\docs\` (vérifié MD5, exit 0 = OK)

**Rechargements HA :**
| Type de section | Rechargement |
|:----------------|:-------------|
| `template:` | Outils dev → YAML → Recharger les templates |
| `automation:` | Outils dev → YAML → Recharger les automations |
| `script:` | Outils dev → YAML → Recharger les scripts |
| `input_*:`, `timer:` | Redémarrage HA complet |
| Dashboard YAML | Outils dev → YAML → Recharger la configuration Lovelace |

---

## ⚙️ INSTANCE HOME ASSISTANT (PRODUCTION)

| Paramètre | Valeur |
|:----------|:-------|
| **IP locale** | `10.32.154.241` |
| **Matériel** | Raspberry Pi 4 (4 Go) + SSD USB |
| **OS** | Home Assistant OS (HAOS) |
| **Zigbee** | Sonoff EFR32MG21 V2 + Zigbee2MQTT |
| **Accès distant** | Nabu Casa (push notifications pas encore configurées) |
| **Samba (local)** | `Z:\` (montage réseau depuis le PC) |
| **Fichiers locaux** | `C:\Users\Berry Swann\Documents\Assitant au personne\raspi\` |
| **Autre agent IA actif** | OpenCode/DeepSeek, édite `Z:\` en direct via `Z:\AGENTS.md` (`hab`, `zigporter` CLI) |

**Déploiement :** copie locale → `Z:\` → vérification MD5 PowerShell → rechargement HA.

---

## 🗂️ ARBORESCENCE LOCALE

```
Assitant au personne/
├── TODO.txt                     ← backlog court terme
├── sync_docs.py                 ← synchro docs/ -> Z:\docs\ (MD5)
├── raspi/                       ← YAML source de vérité → déployés sur le RPi4
│   ├── configuration.yaml       ← déclaration packages + dashboards
│   ├── packages/                ← un fichier YAML par module
│   │   ├── m00_modules.yaml     ← input_boolean interrupteurs modules (entity_id inchangés)
│   │   ├── m01_temp_hygro.yaml
│   │   ├── m02_inactivite.yaml
│   │   ├── m03_ecran_msg.yaml / m03_reset_reglages.yaml
│   │   ├── m04_sos.yaml / m04_gestion_aidants.yaml / m04_groupe_aidants.yaml
│   │   ├── m05_capteur_lit.yaml
│   │   ├── m08_photos.yaml
│   │   ├── m10_visio.yaml       ← renommé depuis m20_visio.yaml (13/08)
│   │   ├── m11_tv.yaml
│   │   ├── m15_porte_ext.yaml
│   │   ├── m16_liens_youtube.yaml  ← ⚠️ collision de numéro, sous-composant de M11
│   │   └── m00_simulation*.yaml ← capteurs fictifs (matériel non pairé)
│   ├── www/                     ← aidant.html, config.html, appairage.html, manifest.json
│   └── dashboards/
│       ├── dashboard_modules.yaml    ← Configuration (6 onglets, masqué sidebar 13/08)
│       ├── dashboard_kiosk.yaml      ← Écran kiosk (occupant)
│       └── dashboard_aidant.yaml     ← iframe -> aidant.html (13/08, ancien en .bak)
│
└── docs/
    ├── INDEX.md                 ← tableau d'avancement rapide (entrée principale)
    ├── DEPENDANCES_GLOBALES.md  ← chaînes de dépendances + statuts + table ancien/nouveau numéro
    ├── 00_IA/
    │   └── IA_CONTEXT_BASE_AI.md ← ce fichier (contexte IA — à lire en premier)
    ├── 01_config_system/        ← fiche + YAML configuration.yaml
    ├── 02_dashboards/           ← fiches + copies YAML dashboards
    ├── 03_modules_packages/     ← classé par fonction (01_socle à 05_confort)
    │   └── <module>/            → fiche .md + YAML copie
    ├── 04_automations_scripts/  ← index automations/scripts
    └── 05_projet/               ← CAHIER_DES_CHARGES, hardware, README...
```

---

## 🔢 NUMÉROTATION DES MODULES (restructurée 2026-08-13)

> Numérotation par groupe (façon ReBuild — dizaines par catégorie). **Les
> `entity_id` réels ne changent pas**, seule l'étiquette de référence change.
> Table de correspondance complète ancien/nouveau : voir `DEPENDANCES_GLOBALES.md`.

| Groupe | Plage | Contenu |
|:-------|:------|:--------|
| **oblig** | M01-M03 | Température/Hygro, Détection Inactivité, Écran Messages — **toujours actifs** |
| **Secur** | M10-M17 | SOS, Capteur Lit, Caméra IA, Porte Ext (S), Fenêtres (S), Frigo, Congélateur, Veilleuse Nuit |
| **Santé** | M20-M22 | Médicaments, Repas, Douche |
| **Confo** | M30-M34 | Kiosk Écran, Photos Famille, Musique, Visio, Télévision |
| **Envir** | M40 | Chauffage (stand-by) |

**(S)** = module à capteurs multiples (ex : Porte_Ext couvre plusieurs portes, Fenêtre couvre plusieurs fenêtres) — la logique doit agréger, pas tester une seule entité.

**Exclus** (orphelins, retrait géré séparément) : ancien M19 (Dashboard Famille), ancien M20 (Messages Famille) — aucune automation ne les consommait.

---

## 📋 ÉTAT DES MODULES — MAJ 2026-08-13

| Module | Statut |
|:-------|:-------|
| oblig_M01 Temp & Hygro | ✅ Déployé |
| oblig_M02 Détection Inactivité | ✅ Développé (12/08) — non testé conditions réelles 🔴 |
| oblig_M03 Écran Messages | ✅ Déployé — 3 sources de défauts contradictoires ⚠️ (voir DEPENDANCES_GLOBALES) |
| Secur_M10 SOS | 🧪 Simulation — notif push manquante 🔴 |
| Secur_M11 Capteur Lit | 🧪 Simulation 🟡 |
| Secur_M12 Caméra IA | ❌ Non implémenté 🔴 |
| Secur_M13 Porte Ext (S) | ⚠️ 1 porte déployée/plusieurs prévues 🔴 |
| Secur_M14 Fenêtres (S) | ❌ Non implémenté 🟡 |
| Secur_M15 Frigo | ❌ Non implémenté, pas de toggle 🟡 |
| Secur_M16 Congélateur | ❌ Non implémenté, pas de toggle 🟡 |
| Secur_M17 Veilleuse Nuit | ❌ Non implémenté 🟡 |
| Santé_M20 Médicaments | ❌ Non implémenté 🔴 Critique (Alzheimer) |
| Santé_M21 Repas | ❌ Non implémenté 🟡 |
| Santé_M22 Douche | ❌ Non implémenté 🟡 |
| Confo_M30 Kiosk Écran | ✅ Dashboard (pas de logique séparée) |
| Confo_M31 Photos Famille | ⚠️ Partiel — rotation à construire 🟡 |
| Confo_M32 Musique | ❌ Non implémenté 🟢 |
| Confo_M33 Visio | ⚠️ Partiel — double mécanisme (HA + aidant.html) 🟡 — pivot Google Meet acté 12/08 |
| Confo_M34 Télévision | ✅ Déployé — bug session4 dans rotation YouTube 🟡 |
| Envir_M40 Chauffage | ❌ Stand-by 🟢 |

**Interface aidant — 2 en test en parallèle :** `aidant.html` (HTML custom, bug `chip-porte`/`chip-msg` corrigé 13/08, droits d'accès 🔧/⚙️ ajoutés 13/08) + dashboard natif v2 (`lovelace-aidant-v2`, bubble-card, mobile-first). **Arbitrage non tranché.**

---

## 🛠️ ENVIRONNEMENT

- **OpenCode installé dans HA** (10/08) : `Z:\AGENTS.md` (instructions système OpenCode, PAS un fichier de gouvernance projet) + `opencode.json` à la racine de config
- **`custom_components/visio_jitsi/`** : intégration HACS Jitsi (exploration 13/08) — **non retenue**, pivot Google Meet acté
- **`www/`** : `aidant.html`, `config.html` (droits d'accès 🔧/⚙️ ajoutés 13/08), `appairage.html` (checklist Z2M — coche disponible/copie/colle dans Z2M), `manifest.json`
- **`config.json`** : valeurs d'usine (surcouche, **PAS source de vérité** — les entités HA font foi)
- **Accès API** : token longue durée jamais dans le chat, révoqué en fin de session

---

## ⚠️ PIÈGES CONNUS (NE PAS REPRODUIRE)

### Piège 1 — `initial:` dans les entités HA
**Comportement :** `initial:` dans un `input_boolean`, `input_text`, `input_select`, etc. réinitialise la valeur à CHAQUE redémarrage HA — pas seulement à la création de l'entité.
**Conséquence :** tous les réglages utilisateur (cases cochées, textes, horaires) sont effacés à chaque reboot.
**Règle :** ne JAMAIS mettre `initial:` sur une entité dont la valeur doit persister entre redémarrages.
**Fichiers déjà corrigés :** `m00_modules.yaml`, `m04_gestion_aidants.yaml`, `m11_tv.yaml`, `m03_ecran_msg.yaml` (envoi_debut/fin, 13/08).

### Piège 2 — `notify.send_message` avec cibles `person.x`
Nécessite une version HA récente. Non encore confirmé que la version actuelle le supporte — tester avant de déployer les scripts SOS réels. Actuellement remplacé par `persistent_notification` (visible HA seulement, pas de push réel).

### Piège 3 — person.x aidants fictifs
Les `person.x` dans `m04_gestion_aidants.yaml` et `m04_groupe_aidants.yaml` sont des **comptes fictifs de test**. À remplacer par les vrais `entity_id` une fois les vrais aidants inscrits dans HA + Companion app installée.

### Piège 4 — Icônes dans `type: entities` (Lovelace)
L'icône définie dans le package YAML d'une entité n'est pas automatiquement affichée dans une carte `type: entities`. Il faut aussi la déclarer explicitement sur chaque ligne entity dans le YAML du dashboard.

### Piège 5 — `!secret` dans les options add-on Supervisor
La syntaxe `!secret` ne fonctionne pas dans les options d'un add-on HA Supervisor (stockées en JSON brut, non traitées par le loader YAML HA). Les clés API doivent être saisies en clair dans l'UI add-on ou via `env_vars` (format `name`/`value`).

### Piège 6 — `st()` / lecture d'état côté HTML (ajouté 13/08)
Dans `aidant.html`, un helper `st(key)` qui renvoie l'état brut sans filtrer `"unknown"`/`"unavailable"` casse tous les fallbacks `||` en aval (ces chaînes sont truthy en JS). Toujours filtrer ces deux valeurs avant de les traiter comme "absentes".

### Piège 7 — IDs DOM fantômes après redesign (ajouté 13/08)
Un `document.getElementById('x').textContent = ...` sur un ID supprimé du HTML lors d'un redesign plante silencieusement (`TypeError` sur `null`) et **arrête toute la fonction appelante**, y compris le code qui suit et n'a rien à voir. Toujours garder `if (el) el.textContent = ...` plutôt que d'accéder directement.

### Piège 8 — Cache navigateur sur pages HTML custom servies par HA (ajouté 13/08)
`aidant.html`/`config.html` modifiées sur `Z:\www\` peuvent rester en cache navigateur après un push. Pour une iframe (ex. `config.html` dans `aidant.html`), cache-buster l'URL (`?v=Date.now()`) à chaque ouverture. Pour la page top-level elle-même, un hard-refresh reste parfois nécessaire malgré les meta `Cache-Control: no-store`.

### Piège 9 — Numéro de module dupliqué entre fichiers (ajouté 13/08)
Un fichier `mNN_xxx.yaml` peut s'auto-étiqueter avec un numéro déjà pris par le registre officiel (`m00_modules.yaml`), créant une confusion. Toujours vérifier `m00_modules.yaml` avant de nommer un nouveau fichier de module. Exemple corrigé : `m20_visio.yaml` (en réalité un sous-composant de M10) → `m10_visio.yaml`. Exemple non corrigé : `m16_liens_youtube.yaml` (sous-composant de M11) toujours en collision avec le vrai M16/Secur_M17 (Veilleuse Nuit).

---

## 🔧 RÈGLES TECHNIQUES DU PROJET

- **Zigbee obligatoire** : Z2M natif uniquement. Tuya/Smart Life/cloud propriétaire interdit.
- **Sécurité 100% locale** : les automations critiques ne dépendent pas d'internet.
- **Nabu Casa** : accès distant famille uniquement — pas dans la boucle des automations.
- **Architecture packages** : `homeassistant.packages: !include_dir_named packages` — un fichier YAML par module.
- **Dashboards en YAML** : modifiés uniquement via fichier YAML local + copie vers `Z:\` — jamais via l'éditeur UI Lovelace (risque d'écrasement).
- **Interface aidant** : `aidant.html` parle directement à l'API REST HA (fetch), utilise en priorité la session HA (`localStorage.hassTokens`) si accessible (iframe/Companion), sinon un token longue durée mémorisé localement.

---

## 📌 SOURCES DE VÉRITÉ

| Priorité | Source | Rôle |
|:---------|:-------|:-----|
| **1** | **Instance HA live** (10.32.154.241) | Ce qui tourne en prod = référence absolue |
| **2** | **`raspi/` local** | Fichiers de travail → à déployer vers `Z:\` |
| **3** | **`docs/DEPENDANCES_GLOBALES.md`** | Chaînes de dépendances + statuts (numérotation par groupe, source de vérité depuis le 13/08) |
| **4** | **`CAHIER_DES_CHARGES.md`** | Référence fonctionnelle (quoi faire) |
| **5** | **`dependances.md`** | Référence technique complémentaire |

---

## 👥 PERSONNES

| Rôle | Détail |
|:-----|:-------|
| **Occupant** | Personne atteinte d'Alzheimer — zéro interaction smartphone requise |
| **Aidants** | Comptes HA (fictifs en test) — reçoivent les alertes via Companion app (push non encore opérationnel) |
| **Famille** | Accès dashboard aidant via Nabu Casa (Marseille → Lille) |

---

## 📋 PROTOCOLE DE SESSION

1. **Début de session** : lire ce fichier en premier, vérifier `python sync_docs.py --check` pour l'état de drift docs/ vs Z:\docs\
2. **Fin de session** : écrire le récap dans `historique/` (faits, décisions, reste à faire) et mettre à jour `TODO.txt` à la racine du projet
3. **Toute MAJ de doc est DATÉE** (règle utilisateur)
4. **Dépendances/entités** (à chaque gros changement YAML/pages) : `python sync_dependances.py` — génère `docs/ENTITES.md` (inventaire : définie dans / consommée par / état live), `docs/DEPENDANCES_TECHNIQUE.md` (chaînes fichiers → entités → consommateurs) et `docs/MOC_DEPENDANCES.md`. Détecte orphelines, renommages (unique_id YAML ≠ entity_id registre) et fantômes. Adapté du script ReBuild.
5. **Synchro déploiement après session** : `python sync_docs.py` (racine du projet) — copie les `.md` à jour de `docs/` → `Z:\docs\` (sauf `_archive/`) et `IA_CONTEXT_BASE_AI.md` → `Z:\` (copie live pour OpenCode), vérifie par MD5
6. **Sources de vérité** : voir tableau ci-dessus. La racine du projet ne contient que `README.md` (index) + `TODO.txt` + `sync_docs.py` + `sync_dependances.py` — toute autre doc appartient à `docs/`

---

*Ce fichier doit être mis à jour à chaque décision technique majeure ou changement de cap.*

---

## 📮 ZONE DE DEMANDES — AUTRES AGENTS IA

> **Seule section de ce fichier modifiable par un agent IA autre que Claude**
> — OpenCode/DeepSeek (actif sur `Z:\` via `AGENTS.md`) ou Hermes (archiviste
> documentation). Dépose ici toute demande d'implémentation, correction, ou
> signalement — Claude la lira et la traitera en début de session suivante,
> puis la retirera une fois faite.
>
> Format suggéré : `- [date] [agent] [demande] — [contexte court]`

*(vide pour l'instant)*
