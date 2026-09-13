# Pages web custom (www/)

> Fiche rédigée le 2026-08-11 à partir de `Z:\www\` - pages ajoutées par Claude (session du 11/08).

## Contenu du dossier
| Fichier | Taille | Rôle |
|:--------|:-------|:-----|
| `aidant.html` | 53 Ko | Interface Aidant autonome (HTML/JS custom) |
| `config.html` | 27 Ko | Configuration modules (chargée en iframe depuis aidant.html, icône 🔧) |
| `appairage.html` | 7,4 Ko | Assistant d'appairage Zigbee2MQTT |
| `launch.html` | 403 o | Cache-buster : redirige vers `aidant.html?v=<timestamp>` |
| `config.json` | 858 o | Valeurs d'usine (`ha_user_name`, `visio_url`, `defauts_m03`) — surcouche, PAS source de vérité |
| `manifest.json` | 427 o | Manifest PWA |
| `liens_youtube.txt` | variable | Liste des vidéos YouTube (générée par M16) |

## `aidant.html` - Interface Aidant (53 Ko)
Page web autonome (accès via `http://10.32.154.241:8123/local/aidant.html`) qui parle **directement à l'API REST HA** (pas de dashboard Lovelace) :
- **API utilisées** : `/api/states/`, `/api/services/input_text/set_value`, `input_datetime/set_datetime`, `input_number/set_value`, `input_select/select_option`, `script/*`, `/api/camera_proxy/`, `/api/profile`
- **Fonctions identifiées** : envoi de message à l'occupant (`input_text.m03_message_famille`), réglages d'affichage M03 (`m03_affichage_duree`, `m03_queue_max`, `m03_rl_max`, `m03_rl_fenetre`), scripts, aperçu caméra
- Style : thème sombre (#0f172a), mobile-first, `mobile-web-app-capable`

### ⚠️ Piège corrigé le 13/08 — `getElementById` orphelins
Les éléments `chip-porte` et `chip-msg` avaient été **supprimés du HTML lors d'un redesign** mais le JS les ciblait toujours (lignes ~961/966) → `TypeError: Cannot set properties of null` → **updateUI() mourait** → toutes les valeurs suivantes restaient figées sur les défauts statiques du HTML (symptôme : « 5 », « — », « 2 » malgré de bonnes valeurs HA — confondu avec le cache 31j). Correctif : protections `if (elPorte)` / `if (elMsg)`. Diagnostic trouvé par Claude Opus 5, vérifié indépendamment (scan des 35 getElementById : 2 orphelins, aucun autre).

## `config.html` - Configuration modules (27 Ko)
Page de configuration des modules, ouverte en iframe depuis aidant.html (icône 🔧 en haut à droite).

## `appairage.html` - Assistant Appairage Z2M (7,4 Ko)
Page d'aide à l'appairage des capteurs Zigbee : liste des devices, guidage appairage Zigbee2MQTT.
- Accès : `http://10.32.154.241:8123/local/appairage.html`
- Contenu : liste (id `list`), notifications (id `toast`), thème sombre

## `liens_youtube.txt`
Fichier de données généré par le module M16 (liste `aaaa-mm-jj|chaine|Titre|URL|déjà_vu`), lisible via `/local/liens_youtube.txt`.

## Notes
- Ces pages sont **dans le dossier www/** (fichiers statiques servis par HA) - elles ne passent pas par le moteur Lovelace
- **Authentification** : token long-lived HA stocké en **localStorage** (saisi une fois, réutilisé par la page) - confirmé par l'utilisateur le 11/08
- Le module M03 et le dashboard aidant les complètent (interface Lovelace + page autonome)
