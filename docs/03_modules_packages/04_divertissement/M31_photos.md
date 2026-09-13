# M31 — Photos Famille

> Fiche réécrite le 2026-08-15 (remplace `M08_photos.md`, jamais renommée
> depuis le passage M08 → M31). Source : `raspi/packages/m31_photos.yaml`.
> Source live : `Z:\packages\m31_photos.yaml`.

## Rôle
Afficher un diaporama photos par défaut sur la TV du salon (mini-PC/RPi4 en HDMI, navigateur enregistré dans Browser Mod), actif hors des créneaux TV (M34) et hors visio (M33) :
- `www/kiosk.html` (zone principale, bloc 4) affiche une photo en fond de carte quand `sensor.confo_m34_etat_global` = `photos` ou `desactive`.
- Les photos viennent de DEUX dossiers possibles (voir révision upload ci-dessous) : `/config/www/photos_famille/` (Samba, non authentifié, servi sous `/local/photos_famille/`) et `/media/photos_famille/` (upload depuis `photos.html`, authentifié HA, servi sous `/media/local/photos_famille/`).
- « Retour photos » = redirection du navigateur TV vers le dashboard kiosk (`/lovelace-kiosk/kiosk`) via `browser_mod.navigate` (`script.m31_lancer_diaporama`), appelé par `m34_television.yaml` en fin de créneau/désactivation.

## Révision 2026-08-15 — vraie rotation multi-photos
Jusqu'ici, une seule photo statique (`photo_actuelle.jpg`) était affichée. Le doute technique bloquant (utilitaires shell disponibles ou non dans le conteneur Core HA) est levé : `shell_command` + `python3` fonctionne déjà ailleurs dans le projet (M34 liens YouTube, M03 RDV récurrents). Même pattern repris ici :

- `shell_command.m31_photos_liste` → exécute `shell_scripts/m31_photos_liste.py`, qui liste tous les fichiers `.jpg/.jpeg/.png/.gif` des dossiers photos (ordre alphabétique, insensible à la casse).
- `www/kiosk.html` interroge ce `shell_command` (`POST /api/services/shell_command/m31_photos_liste?return_response` — **sans** `=true`, voir correctif ci-dessous) et fait tourner les photos trouvées, une image à la fois, au rythme d'`input_number.m31_photos_intervalle_s`.
- Garde-fou anti-reset (`photoListKey`) : la liste n'est comparée qu'à la précédente — si elle n'a pas changé, le timer de rotation n'est pas relancé (même logique que le carrousel calendrier et l'anti-reset vidéo `lastMainKey`).
- `photo_actuelle.jpg`, si encore présent dans le dossier `www`, est listé comme les autres fichiers — pas de traitement spécial, compatibilité conservée.

## Révision 2026-08-15 (même jour) — upload simple depuis config.html (déplacé depuis dans photos.html, voir plus bas)
Le dépôt manuel via Samba restait trop technique pour la famille (« comment les mettre dans le bouzin avec un simple ouvrir/chercher/sélectionner/envoyer »). Ajout d'un vrai bouton d'upload :

- **`config.html`** (onglet Confort → « 📷 M31 — Photos ») : bouton « Choisir des photos… » → sélecteur de fichiers natif du navigateur (multi-sélection), exactement comme joindre un fichier à un mail. **Déplacé le même jour, plus tard, dans `photos.html`** — voir section dédiée ci-dessous.
- Envoi vers `POST /api/media_source/local_source/upload` (form-data `media_content_id` + `file`) — l'endpoint **interne** que l'écran Média natif de HA (Paramètres → Système → Stockage) utilise lui-même depuis des années. Stable, mais **non documenté dans la REST API publique** de HA — confirmé en lisant le code source du frontend HA (`hass-frontend/src/data/media_source.ts`, fonction `uploadLocalMedia`), pas testé en direct sur cette instance.
- Les fichiers atterrissent dans `/media/photos_famille/` — `/media` est un point de montage **distinct** de `/config` (donc de `/config/www`), et protégé par l'authentification HA (contrairement à `/config/www`, public).
- `m31_photos_liste.py` scanne désormais LES DEUX dossiers et préfixe chaque ligne par sa source (`www|nom.jpg` ou `media|nom.jpg`).
- `kiosk.html` affiche les photos `www` en `<img src>` direct (comme avant) et les photos `media` via un `fetch()` authentifié (`Authorization: Bearer`) + conversion en Object URL (`URL.createObjectURL`), la seule façon d'afficher une ressource protégée par HA dans une balise `<img>`.

✅ **Rotation + upload confirmés en direct par l'utilisateur** (2026-08-15, message "sa fonctionne !!!") — après correctif du bug `?return_response=true` → `?return_response` (voir section suivante). L'affichage authentifié des photos `media` sur le kiosk fonctionne également.

## Correctif 2026-08-15 (même jour) — bug `?return_response=true`
Bug réel, confirmé en direct par l'utilisateur (test `fetch()` brut retournant `{}`) puis par la doc officielle HA (`https://developers.home-assistant.io/docs/api/rest/`) : le paramètre REST pour récupérer la réponse d'un `shell_command` est un flag **sans valeur** — `?return_response`, PAS `?return_response=true`. Avec `=true`, HA renvoie un objet vide au lieu de `{changed_states, service_response}`. Corrigé dans `kiosk.html` (`refreshPhotoList`) et, par le même bug repéré ailleurs, dans `aidant.html` (`refreshRdvRecurrentsList`, M03).

## Révision 2026-08-15 (même jour, suite) — page dédiée `photos.html` + suppression
Nouveau bouton « 📷 Photos » dans `aidant.html` (zone « 🔗 Pages dédiées »), protégé par un code PIN partagé (`input_text.m10_pin_pages_dediees`, réglable dans `config.html` → Sécurité, voir `m10_gestion_aidants.yaml`). Construction neuve (pas d'iframe, contrairement à `calendrier.html`/`video.html`) car aucune galerie visuelle n'existait à réutiliser.

- Galerie complète (sources `www` + `media`), même logique d'affichage authentifié que `kiosk.html` pour la source `media`.
- **Suppression réelle** : `shell_command.m31_photos_supprimer` → `shell_scripts/m31_photos_supprimer.py`, qui supprime le fichier directement sur disque. Contourne la limitation WebSocket-only du service natif HA (`media_source/local_source/remove`) sans avoir à implémenter de client WS côté navigateur — même pattern shell_command + python déjà éprouvé pour la liste. Nom de fichier validé côté script (`os.path.basename`, rejet si chemin ou `..`).

## Correctif 2026-08-15 (même jour, suite) — bouton corbeille sans effet
✅ **Confirmé en direct par l'utilisateur** que la suppression ne faisait rien. Cause trouvée : le bouton était construit avec `onclick="askDelete('${p.source}', ${JSON.stringify(p.nom)})"` — `JSON.stringify()` entoure le nom de fichier de **guillemets doubles**, qui cassent l'attribut HTML `onclick="..."` (lui-même en guillemets doubles) : l'attribut devenait invalide et le clic ne déclenchait plus rien. Corrigé en remplaçant l'`onclick` inline par un `data-idx` + un seul écouteur délégué sur `#gallery-grid` (plus aucune interpolation de nom de fichier dans du HTML). Au passage, ajout d'un cache-bust (`?v=Date.now()`) sur la navigation vers/depuis les 3 pages dédiées, pour éviter qu'une ancienne version reste en cache sur l'appareil. ✅ **Suppression re-testée et confirmée fonctionnelle par l'utilisateur** après ces deux correctifs.

## Révision 2026-08-15 (même jour, suite) — upload déplacé de config.html vers photos.html
À la demande de l'utilisateur : le bouton d'upload (« 📷 M31 — Photos », section Confort de `config.html`) est retiré de `config.html` et reconstruit dans `photos.html`, pour regrouper upload + galerie + suppression au même endroit. `PHOTOS_MEDIA_CONTENT_ID`, la logique d'envoi (`onPhotosSelected`) et le bouton « 📷 Ajouter des photos… » vivent désormais uniquement dans `photos.html` ; la galerie se rafraîchit automatiquement après un envoi réussi. Conséquence : l'upload est maintenant protégé par le même PIN partagé que la galerie/suppression (auparavant, `config.html` n'était protégé par aucun PIN).
⚠️ **Non retesté en direct depuis le déplacement** (l'upload avait été confirmé fonctionnel dans `config.html` avant le déplacement, pas encore re-vérifié dans `photos.html`).

## Correctif 2026-08-15 (même jour, suite) — 401 sur l'upload (téléphone ET PC)
Après déplacement, l'upload échouait systématiquement avec `HTTP 401 Unauthorized`, y compris sur PC. Diagnostic :
- Testé côté serveur avec le token longue durée (curl direct, petit fichier ET 2 Mo) : succès à chaque fois → ni l'endpoint, ni la taille de fichier, ni une URL externe (aucune configurée) n'étaient en cause.
- **Preuve décisive** : log HA fourni par l'utilisateur — `Login attempt failed... invalid authentication` depuis l'appareil réel (même réseau local, donc pas un problème de proxy/Cloudflare).
- **Cause probable identifiée** : `currentToken()` préfère le token de session HA (`hassTokens`, courte durée ~30 min) au token longue durée (`ha_token`) s'il est présent, et notre test d'expiration (`t.expires`) peut ne rien détecter si ce champ n'est pas fourni/au format attendu dans le contexte de ces pages autonomes (qui ne bénéficient pas du rafraîchissement automatique de token du frontend HA complet). Résultat : un token de session invalide était utilisé en boucle sans jamais retomber sur le token longue durée valide.
- **Fix** : nouvelle fonction `fetchAuth()` (remplace tous les usages directs de `currentToken()` dans les appels `fetch`) — en cas de `401`, retente automatiquement une fois avec l'**autre** source de token disponible, sans avoir à deviner laquelle est bonne. Appliqué dans `photos.html` (upload, liste, suppression, affichage authentifié, PIN) et par précaution dans `calendrier.html`/`video.html` (vérification PIN).
✅ **Étendu le même jour, à la demande de l'utilisateur, à `aidant.html`, `config.html` et `kiosk.html`** : mêmes usages de `currentToken()` remplacés par `fetchAuth()` (haGet/haPost, camera_proxy, apiGet/apiService/apiGetAllStates, apiGet/apiPost du kiosk, affichage photo authentifié). Laissé intentionnellement de côté : `fetchProfile()` dans `aidant.html` (teste explicitement le token candidat pendant la connexion — un retry automatique n'a pas de sens à cet endroit). `dashboard_kiosk.yaml` cache-bust `?v=20` → `?v=21`.
⚠️ **Non re-testé en direct après ce correctif** (config HA validée via `check_config` : aucune erreur).

## Révision 2026-08-15 (même jour, suite) — 401 persistant : navigation plein écran → iframe-overlay
Le 401 persistait sur téléphone ET PC même après `fetchAuth()` et avec un token fraîchement régénéré et vérifié valide côté serveur (curl direct : succès). Nouvelle preuve fournie par l'utilisateur (log HA) :
- Le téléphone accède au tableau de bord via l'**app native Home Assistant Companion Android** (`User-Agent: Home Assistant/2026.7.5-23688`), pas un navigateur classique — information nouvelle, pas connue avant.
- Le PC échouait aussi, mais sur des endpoints sans rapport (`sensor.confo_m34_etat_global`, calendrier, `input_text.m33_visio_url`) — probablement un onglet `kiosk.html` ouvert seul, sans session HA authentifiée en parent (à confirmer, pas vérifié).
- **Hypothèse retenue** : `config.html` n'a jamais eu ce bug parce qu'il est **toujours** chargé en iframe dans `aidant.html`, jamais en navigation plein écran (`window.location.href`). L'app Companion injecte probablement le contexte de session authentifiée dans la WebView de premier niveau ; une navigation plein écran vers une autre page casserait ce contexte, contrairement à un iframe qui reste dans la même WebView.
- **Fix appliqué** : les 3 boutons « Pages dédiées » dans `aidant.html` n'utilisent plus `window.location.href` mais un système d'overlay iframe identique à `config.html` (`openCalendrier()`/`closeCalendrier()`, `openVideo()`/`closeVideo()`, `openPhotos()`/`closePhotos()` — nouveaux `<div id="screen-calendrier|video|photos">` contenant chacun un `<iframe>`). Les boutons « Retour » de `calendrier.html`/`video.html`/`photos.html` appellent désormais `window.parent.closeCalendrier()` (etc.) quand disponible, avec repli sur l'ancienne navigation plein écran si la page est ouverte hors iframe (ex. test direct par URL).
- **Déployé et vérifié en direct** (`curl` : présence confirmée de `openCalendrier`/`closeVideo`/`closePhotos` etc. sur les 4 fichiers servis par HA).
- ⚠️ **Théorie infirmée par les tests suivants** — l'iframe-overlay n'a pas résolu le 401 (voir section suivante). Gardé en place car sans effet négatif et cohérent avec `config.html`, mais **ce n'était pas la vraie cause**.

## Correctif 2026-08-15 (même jour, suite, DÉFINITIF) — vraie cause : upload HA réservé aux comptes admin
L'iframe-overlay n'a rien changé : 401 identique. Diagnostic final, par élimination méthodique avec l'utilisateur :
- La **galerie** (liste des photos) et la **suppression** fonctionnent parfaitement sur le téléphone, avec le même `currentToken()` que l'upload → ce n'était donc pas un problème de token invalide/périmé, ni de session/navigation.
- Recherche dans le code source officiel de Home Assistant (`homeassistant/components/media_source/local_source.py`, confirmée via l'advisory de sécurité elttam sur l'upload media_source) : la vue d'upload contient explicitement `if not request["hass_user"].is_admin: raise Unauthorized()`. **L'upload media est réservé aux comptes administrateur HA**, contrairement à l'exécution de `shell_command` (liste/suppression), qui ne demande pas ce droit.
- **Confirmé par l'utilisateur** : le compte HA utilisé sur le téléphone n'était pas administrateur. Après passage de ce compte en administrateur (Paramètres → Personnes), l'upload fonctionne. ✅ **Résolu et confirmé en direct par l'utilisateur** ("donc je vien de le passer admin et la j'ai pu dl").
- ⚠️ **Compromis initialement accepté, puis revu** : ce compte a d'abord été passé admin complet (config, utilisateurs, intégrations — pas seulement l'upload photo). L'utilisateur a ensuite fait remarquer, à raison, que ça ne passe pas à l'échelle (tout autre compte "aidant" non-admin resterait bloqué, et le rendre admin à chaque fois est disproportionné) — voir correctif suivant.

## Correctif 2026-08-15 (même jour, suite, DÉFINITIF x2) — contournement shell_command construit
Construction de l'alternative évoquée ci-dessus : un mécanisme qui permet l'upload à **n'importe quel compte non-admin protégé par le PIN partagé**, sans jamais passer par la route officielle HA réservée aux admins.
- **Nouveau** `shell_command.m31_photos_televerser_{debut,chunk,fin}` (`m31_photos.yaml`) + `shell_scripts/m31_photos_televerser.py` : écrit le fichier directement sur disque dans `/media/photos_famille/`, même logique que `m31_photos_supprimer.py` (pas besoin de droits admin, juste d'appeler un service — déjà prouvé fonctionnel pour la galerie/suppression).
- **Découpage en morceaux obligatoire** : `shell_command` exécute une vraie ligne de commande système (Jinja → argv), limitée en taille (ARG_MAX). Une photo de téléphone (souvent plusieurs Mo, donc plusieurs Mo une fois en base64) dépasserait cette limite en un seul appel. `photos.html` lit le fichier en base64 (`FileReader`), le découpe, et envoie chaque morceau par un appel `debut` → `chunk` (répété) → `fin`.
- **Correctif de taille de morceau** (retour utilisateur "HTTP 500 sur l'upload") : la taille initiale (300 000 caractères/appel) dépassait la limite réelle du serveur. **Mesuré en direct par curl** : 100 000 caractères passe (200), 150 000 échoue (500, "Server got itself in trouble"). Ramené à **50 000 caractères/appel** avec marge de sécurité. Validé par un envoi de test complet (2 Mo, 56 morceaux, tous réussis) avant de redemander un test à l'utilisateur.
- ✅ **Confirmé fonctionnel en direct par l'utilisateur**, y compris depuis un compte non-admin sur le téléphone (app Companion Android) : "fonvtionnel \0/". Remarque de l'utilisateur : **plus lent** que l'ancienne méthode (normal — dizaines d'appels réseau séquentiels au lieu d'un seul upload direct), mais accepté comme compromis ("l'important c'est de pouvoir dl une tof").
- Le compte téléphone qui avait été passé admin temporairement peut être repassé non-admin si souhaité (non fait automatiquement — à la discrétion de l'utilisateur).

## Ce qui n'est toujours PAS fait
- **Réception automatique par email** des photos.

## Dépendances
| Élément | Source | Statut |
|:--------|:-------|:-------|
| ~~`input_text.m34_browser_id_tv`~~ | Module M34 | 🚫 **Supprimé 18/08** — `script.m31_lancer_diaporama` vidé de son contenu (voir Entités ci-dessous) |
| `sensor.confo_m34_etat_global` | Module M34 | État `photos`/`desactive` → affichage du diaporama (kiosk.html) |
| `input_boolean.module_kiosk_foto` | M00 (`m00_modules.yaml`) | Interrupteur de module — ⚠️ orphelin, plus consommé par le kiosk actuel — **NE PAS le redéclarer ici** |
| `www/kiosk.html` | Kiosk HA (Z:) | Zone principale (bloc 4) : affichage + rotation JS des photos ; cible de redirection `/lovelace-kiosk/kiosk` |
| Fichiers images (source `www`) | Partage Samba `\\10.32.154.241\config\www\photos_famille\` | Déposés/remplacés manuellement — extensions acceptées : jpg/jpeg/png/gif |
| Fichiers images (source `media`) | Upload via `photos.html` → `/media/photos_famille/` (par `shell_command.m31_photos_televerser_*`, pas la route admin-only) | Extensions acceptées : jpg/jpeg/png/gif |

## Entités
| Entité | Rôle |
|:-------|:-----|
| `input_text.m31_photos_dossier` | « M31 Dossier Photos (chemin local media_source) » — **toujours réservé, non consommé** : les dossiers réellement scannés sont en dur dans `shell_scripts/m31_photos_liste.py`, pas pilotés par cette entité |
| `input_number.m31_photos_intervalle_s` | « M31 Intervalle Diaporama (secondes) » (5-300, défaut 20) — ✅ **utilisé depuis le 15/08**, confirmé en direct par `kiosk.html` pour cadencer la rotation |
| `shell_command.m31_photos_liste` | Liste les photos des deux dossiers (`source\|nom_fichier` par ligne) | Appelé par `kiosk.html` et `photos.html` |
| `shell_command.m31_photos_supprimer` | Supprime un fichier photo (data : `source`, `nom`) — voir `m10_pages_dediees` | Appelé uniquement par `photos.html` (PIN requis) |
| `shell_command.m31_photos_televerser_debut/chunk/fin` | Upload par morceaux, écrit directement sur disque (contourne la restriction admin-only de l'upload média HA natif) | Appelés uniquement par `photos.html` (PIN requis) — ✅ **confirmé en direct**, y compris compte non-admin |
| `input_text.m10_pin_pages_dediees` | Code PIN partagé protégeant `calendrier.html`/`video.html`/`photos.html` (déclaré dans `m10_gestion_aidants.yaml`, réglable dans `config.html` → Sécurité) | Lu par les 3 pages dédiées |
| `script.m31_lancer_diaporama` | 🚫 **Vidé le 18/08** — coquille vide, ne fait plus rien (faisait avant un `browser_mod.navigate`, devenu inutile depuis kiosk.html en HTML pur, voir M34_television.md). Gardé car encore appelé par 2 automations `m34_television.yaml` | Appelé par `m34_television.yaml` |

## Automations
Aucune automation n'est déclarée dans ce package : la bascule vers/depuis le mode photos est pilotée par M34 (`m34_verifier_sessions` défaut + `m34_reset_desactivation`, tous deux dans `confo_m34_television/m34_television.yaml`).

## Pièges connus / TODO avant déploiement
1. ✅ **Rotation + upload confirmés en direct** (2026-08-15) — plus un risque, mais garder en tête que le rechargement à chaud des `shell_command` n'est pas garanti (redémarrage HA recommandé après toute modif de `shell_command:`).
2. ✅ **Upload confirmé en direct dans `photos.html`, y compris depuis un compte non-admin sur l'app Companion Android** (2026-08-15) — via le contournement `shell_command.m31_photos_televerser_*` (n'utilise plus la route admin-only de HA).
3. ✅ **Suppression confirmée en direct** (2026-08-15) après correctif du bug `onclick`/`JSON.stringify` (voir Annotations).
4. **Upload plus lent que l'ancienne méthode** (dizaines d'appels réseau séquentiels au lieu d'un seul) — accepté par l'utilisateur, l'important étant que ça fonctionne. Optimisation possible plus tard si besoin (augmenter la taille des morceaux nécessiterait de re-mesurer la limite réelle du serveur, actuellement mesurée entre 100 000 = OK et 150 000 = HTTP 500).
5. **Taille de morceau (`UPLOAD_CHUNK_SIZE` dans photos.html) dépend du serveur HA** : 50 000 caractères validé sur cette instance (2026-08-15), pas une constante universelle — à re-tester si le comportement change après une mise à jour HA.
6. **Compte HA du téléphone, passé admin temporairement pendant le diagnostic** — n'est plus nécessaire depuis le contournement shell_command ; peut être repassé non-admin (à la discrétion de l'utilisateur, non fait automatiquement).
7. **Pas de réception automatique par email**.
8. **`input_text.m31_photos_dossier` reste un placeholder réservé** : ne pilote rien, les dossiers scannés sont en dur dans le script Python.
9. **Ne pas redéclarer `input_boolean.module_kiosk_foto`** (déjà dans `m00_modules.yaml`) — conflit `unique_id` entre packages.
10. 🚫 **[Résolu 18/08 en le rendant sans objet]** `script.m31_lancer_diaporama` a été vidé (`sequence: []`) — il ne dépend plus de rien, ne fait plus rien. `kiosk.html` gère déjà seul le retour aux photos par sondage d'état.
11. **Chromecast abandonné** (2026-07-04, voir hardware.md) — ne pas réintroduire PhotoFrameCast.
12. **Ordre de rotation** : alphabétique par nom de fichier (pas aléatoire) — à discuter si un tri différent (ex. date, aléatoire) est souhaité plus tard.
13. **PIN pages dédiées = frein, pas une vraie sécurité** : le code est stocké et lu en clair via l'API HA (`input_text.m10_pin_pages_dediees`), lisible par quiconque a le token — sert juste à éviter une ouverture accidentelle.

## Fichiers impliqués
| Fichier | Rôle |
|:--------|:-----|
| `raspi/packages/m31_photos.yaml` | Entités + script + shell_command (liste + suppression + upload par morceaux) |
| `raspi/packages/secur_m10_sos/m10_gestion_aidants.yaml` | `input_text.m10_pin_pages_dediees` (PIN partagé des 3 pages dédiées) |
| `raspi/shell_scripts/m31_photos_liste.py` | Liste les photos des deux dossiers (`www` + `media`) |
| `raspi/shell_scripts/m31_photos_supprimer.py` | Supprime un fichier photo (validation nom + source) |
| `raspi/shell_scripts/m31_photos_televerser.py` | Upload par morceaux (debut/chunk/fin) — écrit directement sur disque, contourne la restriction admin-only HA |
| `raspi/www/kiosk.html` | Affichage + rotation JS (fonctions `refreshPhotoList`, `renderPhoto`, `refreshPhotoInterval`) |
| `raspi/www/config.html` | Champ PIN (Sécurité) — le bouton d'upload en a été **retiré** le 15/08 (déplacé) |
| `raspi/www/photos.html` | Page dédiée galerie + upload (`onPhotosSelected`, déplacé depuis `config.html`) + suppression (PIN requis) |
| `raspi/www/aidant.html` | Bouton « 📷 Photos » (zone « 🔗 Pages dédiées ») + overlay iframe (`screen-photos`/`openPhotos`/`closePhotos`) |
| `raspi/dashboards/dashboard_kiosk.yaml` | Hébergeur iframe du kiosk (cache-bust `?v=20`) |

## Annotations
- 2026-07-04 : création du module M08 (renommé M31 depuis, sans que cette fiche ait suivi jusqu'ici).
- Révision 2026-07-04 (même jour) : suppression PhotoFrameCast/Chromecast, remplacé par `browser_mod.navigate` vers le dashboard kiosk.
- Révision 2026-07-04 (soir) : ajout d'une vraie image statique (`photo_actuelle.jpg`, remplacement manuel Samba) dans le bloc 4 du kiosk.
- 2026-08-15 : fiche réécrite et renommée `M08_photos.md` → `M31_photos.md` (rattrapage — noms restés stale depuis la renumérotation) ; vraie rotation multi-photos construite (`shell_command.m31_photos_liste` + rotation JS dans `kiosk.html`) ; vérifié que `script.m31_lancer_diaporama` n'est PAS orphelin (appelé par `m34_television.yaml`).
- 2026-08-15 (même jour, suite) : bouton d'upload ajouté dans `config.html` (dépôt Samba jugé trop technique par l'utilisateur) — `POST /api/media_source/local_source/upload`, dossier `/media/photos_famille/`, affichage kiosk authentifié pour cette source.
- 2026-08-15 (même jour, correctif) : bug `?return_response=true` → `?return_response` identifié et corrigé (confirmé en direct par l'utilisateur, "sa fonctionne !!!"). Même correctif appliqué par analogie dans `aidant.html` (M03 RDV récurrents).
- 2026-08-15 (même jour, suite) : page dédiée `photos.html` (galerie + suppression), protégée par un nouveau PIN partagé (`input_text.m10_pin_pages_dediees`) ; nouveau `shell_command.m31_photos_supprimer` (contourne la limitation WebSocket-only du service natif HA de suppression média) ; bouton d'accès ajouté dans `aidant.html`.
- 2026-08-15 (même jour, correctif) : suppression sans effet — bug `onclick="askDelete('${p.source}', ${JSON.stringify(p.nom)})"` (guillemets doubles de `JSON.stringify` cassant l'attribut HTML). Corrigé via `data-idx` + écouteur délégué. Cache-bust ajouté sur la navigation vers/depuis les 3 pages dédiées. **Confirmé fonctionnel en direct par l'utilisateur.**
- 2026-08-15 (même jour, suite) : upload déplacé de `config.html` vers `photos.html` à la demande de l'utilisateur — upload + galerie + suppression regroupés au même endroit, tous protégés par le PIN partagé.
- 2026-08-15 (même jour, suite) : bloc « Prendre un rendez-vous » retiré de l'écran principal d'`aidant.html` (voir `M03_ecran_msg.md`) — sans rapport direct avec M31, mais même session/même logique de nettoyage des pages désormais redondantes avec les pages dédiées.
- 2026-08-15 (même jour, suite) : 401 persistant sur l'upload malgré `fetchAuth()` et un token vérifié valide — log HA a révélé que le téléphone utilise l'app Companion Android (WebView), pas un navigateur. Les 3 pages dédiées passent de la navigation plein écran à un système d'overlay iframe (identique à `config.html`), sur l'hypothèse que la navigation plein écran casse le contexte de session injecté par l'app Companion.
- 2026-08-15 (même jour, suite, DÉFINITIF) : hypothèse iframe infirmée (401 identique après déploiement). Vraie cause trouvée par élimination (galerie/suppression OK avec le même token, seul l'upload échoue) puis confirmée dans le code source HA (`local_source.py` : `if not request["hass_user"].is_admin: raise Unauthorized()`) — l'upload media HA est **réservé aux comptes admin**. Le compte HA du téléphone n'était pas admin. **Résolu temporairement** : l'utilisateur a passé ce compte en admin, upload confirmé fonctionnel en direct. Compromis noté : ce compte a maintenant les droits admin complets sur HA, pas seulement l'accès photo.
- 2026-08-15 (même jour, suite, DÉFINITIF x2) : l'utilisateur a fait remarquer, à raison, que la solution "passer admin" ne passe pas à l'échelle (tout autre compte non-admin resterait bloqué). Construction du contournement propre : `shell_command.m31_photos_televerser_{debut,chunk,fin}` + `shell_scripts/m31_photos_televerser.py`, upload par morceaux base64 écrit directement sur disque (même logique que la suppression). Taille de morceau corrigée après un retour "HTTP 500" (300 000 caractères trop gros, mesuré en direct entre 100 000 = OK et 150 000 = échec ; ramené à 50 000 avec marge). **Confirmé fonctionnel en direct par l'utilisateur**, y compris compte non-admin sur téléphone (app Companion) : "fonvtionnel \0/". Plus lent que l'ancienne méthode (accepté, l'important étant que ça marche).
- 2026-08-18 : `script.m31_lancer_diaporama` vidé de son contenu (`sequence: []`) — dépendait de `input_text.m34_browser_id_tv`, supprimé ce jour (plus utilisé nulle part, ni pour la TV ni pour la visio — voir `M34_television.md`). Le retour aux photos fonctionne toujours : `kiosk.html` le gère déjà seul par sondage d'état, sans jamais avoir eu besoin de ce script pour ça en pratique.
