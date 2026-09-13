# M34 — Télévision (4 Sessions Configurables)

> Fiche réécrite le 2026-08-14 après le renommage M11→M34 (13/08) et la
> refonte complète du kiosk en HTML pur. **Remplace `M11_tv.md` (obsolète —
> décrivait l'ancienne architecture navigateur/browser_mod, abandonnée).**
> Source live : `Z:\packages\confo_m34_television\m34_television.yaml` et
> `Z:\packages\confo_m34_television\m34_liens_youtube.yaml`.

## ⚠️ Piège n°1 à connaître avant tout dépannage

**Les `entity_id` réels ne correspondent PAS aux `unique_id`/noms "propres" du YAML.**

Le 13/08, tout le module a été renommé M11→M34 (fichiers, `unique_id`, texte
des `name:`). Mais pour les capteurs **template** et les **automations**,
HA dérive `entity_id` du texte `name:`/`alias:` **au moment de la création**,
pas du `unique_id`. Certains de ces entités avaient un texte `name:`
transitoire commençant par "Confo_M34" (première tentative de renommage,
corrigée depuis dans le texte) — mais l'`entity_id` déjà attribué **ne
change jamais tout seul** après coup, même si le texte `name:` redevient
propre. Résultat : la moitié des entités du module ont un `entity_id` avec
prefixe `confo_` que rien dans le YAML ne laisse deviner.

**Toujours vérifier l'`entity_id` réel dans `.storage/core.entity_registry`
avant de référencer une entité de ce module ailleurs** (dashboard, autre
package, kiosk.html) — ne jamais supposer que `entity_id` = `unique_id`.

## Table de correspondance RÉELLE (vérifiée 2026-08-14)

| unique_id (YAML) | entity_id RÉEL (registre HA) |
|:---|:---|
| `m34_etat_global` | `sensor.confo_m34_etat_global` |
| `m34_video_embed` | `sensor.confo_m34_video_en_cours_embed` |
| `m34_session1_fenetre` | `sensor.confo_m34_session_1_fenetre` |
| `m34_session2_fenetre` | `sensor.confo_m34_session_fenetre` ⚠️ **sans le "2"** |
| `m34_session3_fenetre` | `sensor.confo_m34_session_3_fenetre` |
| `m34_session4_fenetre` | `sensor.confo_m34_session_4_fenetre` |
| `m34_verifier_sessions` (automation) | `automation.confo_m34_verifier_les_sessions_tv_toutes_les_minutes` |
| `m34_reset_desactivation` (automation) | `automation.confo_m34_retour_photos_si_module_tv_desactive` |
| `m34_bouton_ok_session` (automation) | `automation.confo_m34_bouton_ok_relancer_la_session_avec_la_chaine_choisie` |
| `m34_maj_liens_hebdo` (automation) | `automation.confo_m34_mise_a_jour_hebdo_des_liens_youtube` |
| `m34_chaine_changee_en_session_active` (automation, créée 14/08 — pas de bug de prefixe) | `automation.m34_rechargement_immediat_si_chaine_changee_en_session_active` |
| `m34_marquer_vu_apres_visionnage` (automation, créée 14/08) | `automation.m34_marquer_video_vue_5_min_avant_sa_fin_reelle` |
| `m34_seed_horaires_defaut` (automation, créée 14/08) | `automation.m34_horaires_par_defaut_une_seule_fois_demarrage_ha` |

Tous les `input_boolean`/`input_text`/`input_select`/`input_datetime`/
`input_button`/`script` gardent un `entity_id` propre et prévisible (dérivé
de la **clé YAML**, pas du texte `name:`) : `input_datetime.m34_session2_debut`,
`input_select.m34_session2_chaine`, `script.m34_lancer_session`, etc.

## Rôle

Bascule Photos (M31) ↔ Visio (M33) ↔ TV sur l'unique écran du kiosk, selon
**4 sessions TV indépendantes**, chacune avec son horaire, sa chaîne et son
interrupteur actif/inactif. Affichage 100% en HTML pur (`www/kiosk.html`),
plus de Lovelace/`custom:button-card` pour le kiosk depuis le 14/08.

**Mécanisme vidéo actuel : iframe YouTube embed (`youtube-nocookie.com`),
PAS de redirection navigateur ni de casting.** L'ancienne approche
(`browser_mod.javascript` + URLs directes France 2/Arte/France 5, Browser ID
à sécuriser) a été **abandonnée** avec la bascule kiosk.html.

⚠️ **Mise à jour 2026-08-18** : la phrase ci-dessus disait à l'origine que
`browser_mod` restait utilisé « pour la visio (M33), à vérifier séparément »
— ce n'est plus vrai non plus depuis le 16/08 (M33 est passé en WebRTC
maison, plus aucun rapport avec `browser_mod`, voir `M33_visio.md`).
`input_text.m34_browser_id_tv` a été **supprimé** ce jour (plus utilisé nulle
part, ni pour la TV ni pour la visio — vérifié) ; le seul appel
`browser_mod.navigate` restant (`script.m31_lancer_diaporama`, appelé par
les automations de ce module pour forcer le retour du navigateur TV sur le
dashboard kiosk) a été vidé de son contenu : `kiosk.html` gère déjà ce retour
tout seul par sondage d'état, sans avoir besoin d'être « navigué » nulle
part. `browser_mod` n'a donc plus AUCUN usage actif dans le projet.

## Chaîne de dépendances complète (comment ça s'enchaîne)

```
1. www/kiosk.html (navigateur du kiosk, poll toutes les 20s)
   └─> lit sensor.confo_m34_etat_global (état + attribut texte_affichage)
        └─> si état = session1/2/3/4 : lit sensor.confo_m34_video_en_cours_embed
             └─> affiche <iframe src="...' referrerpolicy="strict-origin-when-cross-origin">
        └─> sinon (photos/desactive) : affiche /local/photos_famille/photo_actuelle.jpg

2. sensor.confo_m34_etat_global (template, recalcul réactif)
   └─> lit input_boolean.module_m34_television (interrupteur maître)
   └─> lit sensor.confo_m34_session_{1,fenetre,3,4}_fenetre (debut_reel/fin_reelle)
   └─> lit input_boolean.m34_sessionN_actif
   └─> compare à l'heure actuelle → décide session1/2/3/4 ou "photos"

3. sensor.confo_m34_session_N_fenetre (template, 1 par session)
   └─> lit input_select.m34_sessionN_chaine + input_datetime.m34_sessionN_debut/fin
   └─> si chaîne = France 2/Arte/France 5 (EPG) : ajuste sur le programme réel
       (mais AUCUNE des 4 chaînes actuelles n'est dans ce cas — voir plus bas)
   └─> sinon : renvoie simplement l'horaire fixe saisi

4. sensor.confo_m34_video_en_cours_embed (template)
   └─> lit input_text.m34_sessionN_youtube_url (N = session active)
   └─> construit l'URL embed youtube-nocookie.com

5. script.m34_lancer_session (déclenché par les automations ci-dessous)
   └─> si module_m34_liens_youtube ON : shell_command "next" → nouvelle URL
   └─> écrit input_text.m34_sessionN_youtube_url
   └─> récupère la durée réelle (shell_command "duration", via yt-dlp)
   └─> programme input_datetime.m34_sessionN_marquer_vu_a = maintenant + durée - 5 min

6. shell_command.m34_liens_youtube → shell_scripts/m34_liens_youtube.py
   └─> lit/écrit www/liens_youtube.txt (1 ligne par vidéo, colonne "chaîne")
```

## Automations (qui déclenche quoi)

| Automation (unique_id) | Déclencheur | Rôle |
|:---|:---|:---|
| `m34_verifier_sessions` | toutes les minutes, si module ON | Détecte un changement de session (photos↔TV↔TV) → appelle `script.m34_lancer_session` |
| `m34_reset_desactivation` | `module_m34_television` → off | Retour photos |
| `m34_bouton_ok_session` | bouton "OK" manuel d'une session | Relance `script.m34_lancer_session` pour cette session |
| `m34_chaine_changee_en_session_active` (14/08) | changement de `input_select.m34_sessionN_chaine` | Si la session N est ACTIVE en ce moment → relance `script.m34_lancer_session` (corrige le bug "changer de chaîne ne faisait rien tant que la session ne changeait pas") |
| `m34_marquer_vu_apres_visionnage` (14/08, dans `m34_liens_youtube.yaml`) | `input_datetime.m34_sessionN_marquer_vu_a` atteint | Marque la vidéo en cours "déjà_vu" — 5 min avant sa fin réelle, pas au hasard d'un re-déclenchement |
| `m34_seed_horaires_defaut` (14/08) | démarrage HA, une seule fois (`m34_horaires_initialises`) | Seed unique des horaires/chaînes/Browser ID/URLs par défaut (perdus par le renommage) |
| `m34_maj_liens_hebdo` (`m34_liens_youtube.yaml`) | tous les lundis 09:00 | `shell_command` action `update` — récupère les nouvelles vidéos RSS |

## Système "déjà_vu" (anti-répétition)

- Chaque vidéo jouée doit être marquée "déjà_vu" dans `www/liens_youtube.txt`
  **seulement si elle a été regardée pour de vrai** (pas juste sélectionnée).
- Depuis le 14/08 : le marquage se fait **5 minutes avant la fin réelle** de
  la vidéo (durée récupérée via `yt-dlp`), pas au moment où le script tourne
  — avant, un simple changement de chaîne en cours de session marquait la
  vidéo "vue" même à peine commencée.
- Si TOUTES les vidéos d'une chaîne sont "déjà_vu" (chaîne épuisée) :
  `m34_liens_youtube.py` action `next` **réinitialise tout le cycle** pour
  cette chaîne (retire tous les "déjà_vu") plutôt que de rejouer en boucle
  toujours la même vidéo (bug corrigé le 14/08).
- Le rotation ne fonctionne QUE si `input_boolean.module_m34_liens_youtube`
  est **ON**. Si OFF : l'URL de chaque session reste 100% manuelle (à saisir
  soi-même dans `input_text.m34_sessionN_youtube_url`), aucune rotation.

## Chaînes disponibles et leurs vraies sources

| Chaîne (menu déroulant) | Source de rotation réelle | Notes |
|:---|:---|:---|
| **france tv** | Flux RSS chaîne YouTube officielle france tv + alias "France 2" (anciennes vidéos) | Couvre les documentaires des chaînes France 2/3/4/5 (contenu agrégé sur la chaîne france tv) |
| **Arte** | Flux RSS chaîne YouTube officielle Arte | |
| **TV5 Monde** | Playlist YouTube "Destination Francophonie" | |
| **Nat Geo** | Playlist YouTube officielle | |
| ~~France 5~~ | — | N'a jamais été une option du menu (seul "YouTube" générique y était) |
| ~~YouTube~~ (générique) | — | **Retiré le 14/08** : aucune source de rotation derrière, à la demande utilisateur |

Aucune des 4 chaînes actuelles n'utilise l'EPG XMLTV (ce mécanisme existe
encore dans le code des capteurs "Fenêtre" pour France 2/Arte/France 5 mais
n'est plus jamais déclenché — dead code inoffensif, pas nettoyé).

## Fichiers impliqués

| Fichier | Rôle |
|:---|:---|
| `packages/confo_m34_television/m34_television.yaml` | Sessions, horaires, chaînes, scripts, automations de session |
| `packages/confo_m34_television/m34_liens_youtube.yaml` | Rotation vidéo, capteur embed, automation MAJ hebdo + marquage vu |
| `shell_scripts/m34_liens_youtube.py` | Logique Python : RSS/playlists, marquage, sélection, durée (yt-dlp) |
| `www/liens_youtube.txt` | Base de données plate des vidéos connues (1 ligne par vidéo) |
| `www/kiosk.html` | Affichage final — horloge/temp, agenda, messages, **vidéo/photo/visio**, bandeau méta |
| `dashboards/dashboard_kiosk.yaml` | Coquille Lovelace minimale — juste une iframe plein écran vers `kiosk.html?v=N` |
| `www/config.html` | Réglages des 4 sessions TV **+ plage horaire des appels visio depuis le 18/08** (onglet Confort → « 📺 Vidésio — Sessions TV & Visio ») ; zone encadrée par `#only-tv-block` depuis le 15/08 |
| `www/video.html` | **Renommé « Vidésio » le 18/08** (était « Vidéo ») — page dédiée (bouton dans `aidant.html`, droit 📺 requis) qui embarque `config.html?only=tv` en iframe pour afficher Sessions TV + plage horaire visio (M33) au même endroit — voir `M10_gestion_aidants.md` pour le mécanisme de droits |

## Pièges connus / notes de dépannage

1. **`entity_id` ≠ `unique_id`** — voir tableau de correspondance en haut de
   cette fiche. Cause n°1 de bugs "ça ne marche pas alors que le YAML a l'air
   bon".
2. **Capteurs template figés (ne se recalculent pas)** — rare mais déjà vu :
   si un capteur `template:` reste bloqué sur une vieille valeur malgré des
   changements de ses entités sources, `Outils de développement → YAML →
   Recharger les modèles` force le recalcul. Un redémarrage complet le fait
   aussi.
3. **Erreur "153" YouTube ("Erreur de configuration du lecteur vidéo")** —
   causée par l'en-tête HTTP `Referrer-Policy: no-referrer` que HA envoie par
   défaut sur tout `/local/`. Corrigé par `<meta name="referrer" content=
   "strict-origin-when-cross-origin">` dans `kiosk.html`. Si ça revient après
   une modification de `kiosk.html`, vérifier que cette balise est toujours
   présente en haut du `<head>`.
4. **"Vidéo non disponible" (pas erreur 153)** — plus difficile : peut venir
   de l'origine HTTP + IP privée (`http://10.32.154.241:8123`) que YouTube
   n'apprécie pas toujours pour l'embedding. Pas résolu de façon garantie à
   ce jour — tester via l'URL Nabu Casa (HTTPS) si ça persiste.
5. **La vidéo redémarre en boucle toutes les 20s** — `kiosk.html` recréait
   l'iframe à chaque cycle de rafraîchissement. Corrigé le 14/08
   (`lastMainKey` : ne touche au DOM que si le contenu affiché change
   vraiment).
6. **`dashboard_kiosk.yaml` iframe cache l'ancienne version** — la carte
   Lovelace `iframe` ne supporte pas de cache-bust dynamique. Convention :
   incrémenter manuellement `?v=N` dans `url:` à CHAQUE modification de
   `kiosk.html`, sinon le navigateur du kiosk peut servir une version en
   cache indéfiniment.
7. **`shell_command.m34_liens_youtube` pointait vers un fichier inexistant**
   — le fichier physique `shell_scripts/m16_liens_youtube.py` n'avait jamais
   été renommé lors du renommage général du 13/08. Corrigé le 14/08 (renommé
   en `m34_liens_youtube.py`). Si `update`/`mark`/`next`/`duration` semblent
   ne rien faire, vérifier en premier que ce fichier existe bien sous ce nom.
8. **Piège `initial:`** (hérité, toujours valable) : ne jamais ajouter
   `initial:` sur les helpers de ce module — ça écrase chaînes/horaires/URLs
   à CHAQUE redémarrage, pas juste à la création.
9. **Modifier le YAML directement dans `.storage/core.entity_registry` en
   live est peu fiable** — HA peut écraser les éditions fichier avec son état
   mémoire. Pour un vrai renommage d'entité, préférer l'UI HA (Paramètres →
   Appareils et entités → renommer) plutôt qu'éditer le registre à la main.

## Annotations (historique)

- 2026-07-04 → 2026-08-05 : voir `_archive`/historique — architecture
  d'origine (3 sessions, redirection navigateur, camera.m11_tv_flux
  abandonnée). Détails conservés dans l'ancienne fiche `M11_tv.md` (Z: uniquement, obsolète).
- 2026-08-13 : renommage général M11→M34 (voir `docs/RENOMMAGE_TABLE.md`).
  Bug de fond découvert le lendemain : `sensor.confo_m34_etat_global`
  référençait des `sensor.m34_session_N_fenetre` inexistants (sans le
  préfixe `confo_`) → aucune session jamais détectée active.
- 2026-08-14 : bascule complète vers `kiosk.html` (HTML pur, iframe YouTube
  embed direct, plus de redirection navigateur pour la TV). 4ème session
  ajoutée. Système "déjà_vu" refondu (marquage différé 5 min avant la fin
  réelle + réinitialisation de cycle si chaîne épuisée). Fix
  `shell_scripts/m16_liens_youtube.py` → `m34_liens_youtube.py`. Option
  "YouTube" générique retirée du menu (aucune source de rotation).
  Référentiel complet des `entity_id` réels vérifié et documenté (cette fiche).
- 2026-08-15 : page dédiée `video.html` — bouton dans `aidant.html` (zone
  « 🔗 Pages dédiées »), protégé par un code PIN partagé
  (`input_text.m10_pin_pages_dediees`, voir `M10_gestion_aidants.md`). La
  zone Sessions TV de `config.html` a été encadrée par `#only-tv-block` ;
  `video.html` embarque `config.html?only=tv` en iframe plutôt que de
  dupliquer la logique des 4 sessions — une seule source de vérité. Non
  vérifié en direct cette session.
- 2026-08-15 (suite) : `video.html` s'ouvre désormais en **overlay iframe**
  depuis `aidant.html` (`openVideo()`/`closeVideo()`) au lieu d'une
  navigation plein écran — même correctif et même hypothèse (app Companion
  Android perdant le contexte de session) que `calendrier.html`/`photos.html`,
  voir `M31_photos.md` pour le détail du diagnostic 401. Bouton retour
  appelle `window.parent.closeVideo()` avec repli si ouvert hors iframe.
  Poussé et vérifié en direct ; **non confirmé par l'utilisateur**.
- 2026-08-18 (**suppression `input_text.m34_browser_id_tv`**) : retour
  utilisateur (« ça sert oui ou non ? ») suite à une vérification de code —
  confirmé mort depuis la bascule du 14/08 (kiosk.html en HTML pur), y
  compris son dernier usage réel (`script.m31_lancer_diaporama`, forçait un
  retour navigateur devenu inutile puisque kiosk.html se remet déjà tout seul
  sur photos par sondage). Champ + section "⚙️ Réglages avancés TV" retirés
  de `config.html`, entité + seed retirés de `m34_television.yaml`, script
  `m31_lancer_diaporama` vidé de son contenu (gardé en coquille vide car
  encore appelé par 2 automations de ce module — `m34_verifier_sessions`,
  `m34_reset_desactivation` — retrait de ces 2 appels non fait, hors
  périmètre de la demande). `browser_mod` n'a plus AUCUN usage actif dans le
  projet (voir note plus haut).
- 2026-08-18 (suite, **renommage « Vidésio »**) : demande utilisateur — la
  section « 📺 M11 — Sessions TV » devient « 📺 Vidésio — Sessions TV & Visio »,
  et la plage horaire des appels visio (M33, ajoutée plus tôt le même jour
  dans l'onglet Aidants) est **déplacée ici**, regroupée avec les horaires
  TV. Un seul écran (`video.html`, renommé « Vidésio », `config.html?only=tv`)
  couvre désormais TV + Visio. Renommage propagé partout où « 📺 Vidéo »
  apparaissait comme libellé : bouton dans `aidant.html`, titre de
  `video.html`, message d'accès refusé (corrigé au passage : pointait encore
  vers « Sécurité → Droits d'accès », onglet renommé « Aidants » depuis le
  16/08), texte des droits d'accès dans `config.html`. Le bit de droit
  (`DROIT_BIT.video`, bit 8) et les entity_id (`input_datetime.
  m33_horaire_debut`/`_fin`) ne changent pas — seuls les libellés affichés
  changent.
