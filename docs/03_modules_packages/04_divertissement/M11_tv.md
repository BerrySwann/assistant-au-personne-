# M11 — Télévision (3 Sessions Configurables)

> Fiche rédigée le 2026-08-11 à partir de `raspi/packages/m11_tv.yaml` (local).
> Source live : `Z:\packages\m11_tv.yaml`.

## Rôle
Basculer Photos (M08) ↔ TV sur l'unique écran (TV salon, mini-PC/RPi4 en HDMI, navigateur enregistré dans Browser Mod), selon jusqu'à **3 sessions TV indépendantes**, chacune avec son propre interrupteur on/off, ses horaires et son choix de chaîne (France 2 / Arte / France 5) ou YouTube. Pilotage par **redirection du navigateur** (`browser_mod.javascript`), **PAS par casting Chromecast** (abandonné le 2026-07-04, voir hardware.md).

Pour chaque session N (1 à 3) :
- `input_boolean.m11_sessionN_actif` → active/désactive cette session **sans effacer sa config**
- `input_datetime.m11_sessionN_debut/fin` → heures cibles (fallback si pas d'EPG, ou horaire fixe si YouTube)
- `input_select.m11_sessionN_chaine` → France 2 / Arte / France 5 / YouTube
- `input_text.m11_sessionN_youtube_url` → URL vidéo YouTube (si chaîne = YouTube)

⚠️ **Points non confirmés / à surveiller** (repris de l'en-tête du YAML) :
1. **SÉCURITÉ BROWSER_ID — CRITIQUE** : `input_text.m11_browser_id_tv` DOIT être rempli avec le Browser ID exact du mini-PC/TV avant d'activer `module_television` — sinon un appel non ciblé toucherait **TOUS** les navigateurs Browser Mod enregistrés (dont les téléphones famille).
2. **EPG** : confirmé le 2026-07-04 avec XMLTV EPG (HACS) + source xmltvfr.fr (`https://xmltvfr.fr/xmltv/xmltv_tnt.xml.gz`). Attributs réels : `start`/`end`. Ne s'applique qu'aux sessions réglées sur France 2/Arte/France 5 — les sessions YouTube utilisent toujours l'horaire fixe.
3. **Navigation via `browser_mod.javascript`** (`window.location.href`) : mécanisme JS standard **plausible, non testé en conditions réelles**.
4. **URLs « direct » France 2/Arte/France 5** : correctes au 2026-07-04, **peuvent changer sans préavis** (structure de site web).

## Dépendances
| Élément | Source | Statut |
|:--------|:-------|:-------|
| `input_boolean.module_television` | M00 (m00_modules.yaml) | Interrupteur de module — conditionne `m11_verifier_sessions` |
| `script.m08_lancer_diaporama` | Module M08 (m08_photos.yaml) | Retour photos : appelé en défaut de session et à la désactivation |
| `sensor.france2_fr_program_current`, `sensor.arte_fr_program_current`, `sensor.france5_fr_program_current` | XMLTV EPG (HACS) + xmltvfr.fr | Attributs `start`/`end` (et `title`) — fenêtres EPG des sessions TV |
| Browser Mod | Navigateur du kiosque enregistré (Browser ID) | `browser_mod.javascript` / `browser_mod.navigate` |
| Compte France TV gratuit (`erodi@free.fr`) | Profil Brave persistant du PC de test | Direct France 2/Arte/France 5 (politique diffuseur depuis 2023-2024) |
| `dashboard_kiosk.yaml` | Kiosk HA (Z:) | Cible `/lovelace-kiosk/kiosk` (retour photos) |

## Entités

### input_text
| Entité | Rôle |
|:-------|:-----|
| `m11_browser_id_tv` | « M11 Browser ID — Navigateur TV (SÉCURITÉ, vide = désactivé) » — cible des redirections |
| `m11_url_france2` | « M11 URL Direct — France 2 » |
| `m11_url_arte` | « M11 URL Direct — Arte » |
| `m11_url_france5` | « M11 URL Direct — France 5 » |
| `m11_session1_youtube_url` / `...2...` / `...3...` | « M11 Session N — URL YouTube (si chaîne = YouTube) » |
| `m11_session_affichee` | « M11 État interne — Session actuellement affichée » (évite de relancer la redirection chaque minute) |

### input_select
| Entité | Rôle |
|:-------|:-----|
| `m11_session1_chaine` / `...2...` / `...3...` | « M11 Session N — Chaîne » — options : France 2 / Arte / France 5 / YouTube |

### input_boolean
| Entité | Rôle |
|:-------|:-----|
| `m11_session1_actif` / `...2...` / `...3...` | « M11 Session N — Active » — active/désactive la session sans effacer sa config |

### input_datetime
| Entité | Rôle |
|:-------|:-----|
| `m11_session1_debut` / `...2...` / `...3...` | « M11 Session N — Heure cible début » (heure seule) |
| `m11_session1_fin` / `...2...` / `...3...` | « M11 Session N — Heure cible fin » (heure seule) |

### input_number
| Entité | Rôle |
|:-------|:-----|
| `m11_marge_recherche_min` | « M11 Marge Recherche EPG (min autour de l'heure cible) » (0-60, pas 5, défaut 30 via template) |
| `m11_marge_fin_min` | « M11 Marge Après Fin Programme (min) » (0-30, pas 1, défaut 5 via template) |

### Capteurs template
| Entité | Rôle |
|:-------|:-----|
| `sensor.m11_session1_fenetre` / `...2...` / `...3...` | « M11 Session N Fenêtre » — état `ok`, attributs `debut_reel`/`fin_reelle` : heure EPG du programme en cours si chaîne TV (à ± marge de l'heure cible), sinon heure cible (YouTube = horaire fixe) |
| `sensor.m11_etat_global` | « M11 État Global » — état : `desactive` (module TV off) / `session1` / `session2` / `session3` / `photos` (aucune session active) ; attribut `texte_affichage` (📺 chaîne — titre EPG, ou 📷 Photos famille) |

⚠️ `camera.m11_tv_flux` : **PAS configurable en YAML** (platform `generic` rejetée par HA — « does not support platform setup »). À configurer via l'UI (Paramètres > Appareils et services > Ajouter une intégration > Generic Camera) si l'approche caméra devait revenir — approche **abandonnée définitivement** (v4).

## Automations
| ID | Alias | Déclencheur | Action |
|:---|:------|:------------|:-------|
| `m11_verifier_sessions` | M11 — Vérifier les sessions TV (toutes les minutes) | `time_pattern` minutes `/1`, condition : `module_television` = on | Si `sensor.m11_etat_global` ≠ `m11_session_affichee` : met à jour `m11_session_affichee` puis `choose` — session1/2/3 → `script.m11_lancer_session` (num = N) ; défaut (photos) → `script.turn_on` `script.m08_lancer_diaporama` |
| `m11_reset_desactivation` | M11 — Retour photos si module TV désactivé | `input_boolean.module_television` → off | `m11_session_affichee` = « aucune » + `script.turn_on` `script.m08_lancer_diaporama` |

Mode `single` sur les deux automations.

### Script
| Script | Rôle |
|:-------|:-----|
| `script.m11_lancer_session` | « M11 — Lancer la chaîne/vidéo d'une session » — champ `num` (1, 2 ou 3) ; condition : `m11_browser_id_tv` non vide ; URL selon la chaîne (m11_url_france2 / m11_url_arte / m11_url_france5 / m11_sessionN_youtube_url) ; condition : URL non vide ; `browser_mod.javascript` `window.location.href = '<url>'` |

## Pièges connus / TODO avant déploiement
1. ⚠️ **CRITIQUE SÉCURITÉ — Browser ID** : `m11_browser_id_tv` doit contenir le Browser ID **exact** du navigateur du kiosque avant d'activer `module_television`, sinon les redirections toucheraient **tous** les navigateurs Browser Mod (dont les téléphones famille). Vide = désactivé.
2. **TODO : kiosque final** : refaire la procédure « Register Browser ID » (via `/browser-mod`, toggle « Register » ON) + connexion France TV (`erodi@free.fr`) sur le vrai appareil kiosque (mini-PC/RPi4) — chaque navigateur a son propre Browser ID (fait uniquement sur le PC de test : `browser_mod_e7c11348_360592ea`). Ne pas confondre avec l'`entry_id` de l'intégration Browser Mod (`01KWPA620GM5RQTG2ZR4V3FAJE`) — bug v4 corrigé.
3. **TODO : dashboard_kiosk.yaml (Z:)** référence toujours `camera.m11_tv_flux` (carte webrtc-camera cassée, « Camera not found ») — revenir à une version sans dépendance caméra, **non fait à ce stade**.
4. **`camera.m11_tv_flux` non configurable en YAML** : platform `generic` rejetée (« does not support platform setup », confirmé dans /config/logs le 2026-07-05 17:52) — via l'UI uniquement ; approche caméra abandonnée définitivement (v4).
5. **URLs directes France 2/Arte/France 5** : correctes au 2026-07-04, peuvent changer sans préavis.
6. **`browser_mod.javascript`** (`window.location.href`) : non testé en conditions réelles.
7. **EPG** : dépend de XMLTV EPG (HACS) + source xmltvfr.fr ; attributs réels `start`/`end` ; sessions YouTube = horaire fixe (pas d'EPG).
8. **Piège `initial:`** (correctif v5, 2026-08-05) : ne pas ajouter `initial:` — ça réinitialisait chaînes, horaires, Browser ID et URLs à CHAQUE redémarrage (voir IA_CONTEXT_BASE_AI.md - Piège 1). Sans `initial:`, HA restaure le dernier état connu.
9. **Priorité de session** : si plusieurs sessions actives en même temps, l'ordre du template fait gagner session1 > session2 > session3.
10. **Compte France TV obligatoire** pour le direct (politique du diffuseur depuis 2023-2024, pas un bug HA) — session conservée sur le profil Brave persistant du PC de test.

## Annotations
- 2026-07-04 : création du module M11.
- v1 : 2 créneaux fixes (créneau1 EPG + chaîne, créneau2 YouTube fixe).
- v2 (2026-07-04, même jour) : généralisé à 3 sessions identiques et indépendamment activables, avec dérivation automatique de l'entité EPG depuis la chaîne choisie (fin de la config manuelle fragile `m11_epg_entity_creneau1`).
- v3 (2026-07-05) : tentative `camera.m11_tv_flux` (platform generic YAML, HLS Arte) — **ÉCHEC** (« does not support platform setup ») ; retiré du package ; script + redirection navigateur déclarés provisoirement obsolètes, pas encore nettoyés.
- v4 (2026-07-07) : **approche caméra abandonnée définitivement**, retour à 100 % sur `script.m11_lancer_session` + `browser_mod.javascript` (redevient le mécanisme actif). Deux bugs corrigés : (1) `m11_browser_id_tv` contenait l'entry_id de l'intégration au lieu d'un Browser ID — corrigé avec le vrai Browser ID du PC de test ; (2) France 2/Arte/France 5 exigent un compte France TV gratuit — compte créé et connecté sur le profil Brave persistant, testé de bout en bout le 2026-07-07. ⚠️ Reste à faire sur le vrai kiosque final (voir Pièges n°2 et n°3).
- v5 (2026-08-05) : suppression de tous les `initial:` (piège HA : réinitialisation à chaque redémarrage).
