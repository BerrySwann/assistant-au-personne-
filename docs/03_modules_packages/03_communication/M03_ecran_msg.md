# M03 — Écran Messages (2 canaux : Agenda + Texto famille)

> Fiche réécrite le 2026-08-14 (clôture de la session messages : file qui ne
> se vidait plus, ordre des vérifications du bouton Envoyer, seuil de
> caractères 3 couleurs, bouton reset ajouté, boîte "en cours d'affichage"
> dédupliquée, incohérence `queue_max` corrigée), mise à jour le 2026-08-15
> (calendrier local + RDV + récurrence, bandeau kiosk repensé en 1 ligne).
> Source live : `Z:\packages\oblig_m03_ecran_msg\m03_ecran_msg.yaml`.
> Consommateurs : `www/aidant.html` (saisie + réglages), `www/kiosk.html`
> (bandeau `msg-box`).

## Rôle

Bandeau d'information avec **2 canaux** arbitrés par priorité :

- **Canal 1 — Agenda** : prochain événement `calendar.calendrier_local`,
  formaté selon le délai restant (`sensor.m03_agenda_formate`).
- **Canal 2 — Texto** : messages courts envoyés depuis `aidant.html`, stockés
  dans une **file de rotation** pipe-séparée (`sensor.m03_texto_formate`).

Un troisième capteur (`sensor.m03_bandeau_principal`) arbitre les deux et
fournit le texte final affiché.

## Calendrier — `calendar.calendrier_local` (14/08)

Google Calendar a été abandonné (confidentialité — refus des aidants de
connecter un compte Google chez la personne aidée). Remplacé par
l'intégration native HA **Local Calendar** (Paramètres → Appareils et
services → Ajouter une intégration → Local Calendar), créée le 14/08 sous
le nom "Calendrier local" → `calendar.calendrier_local`. Fichier `.ics`
stocké localement dans `/config`, aucun compte externe requis.

**Création de rendez-vous depuis `aidant.html`** (section "📅 Prendre un
rendez-vous", sous le bloc messages) : formulaire date + heure + note (max
60 caractères, même convention que le champ message). Appelle directement
le service générique HA `calendar.create_event` (aucun package/script HA
nécessaire — ce service est natif à toute intégration calendrier qui le
supporte, dont `local_calendar`) :
- `entity_id: calendar.calendrier_local`
- `summary: <note>`
- `start_date_time` / `end_date_time` : durée par défaut fixée à **30 min**
  (l'utilisateur ne saisit qu'une heure de début, pas de fin — non demandé)

Bouton 3 couleurs (même logique que le bouton Envoyer) : gris (rien saisi)
→ bleu (partiellement rempli) → vert (date + heure + note prêtes).

**Récurrence (14/08, popup) :** au clic sur "Créer le rendez-vous" (une fois
date/heure/note prêts), une popup demande **"Ce rendez-vous est-il
récurrent ?" NON/OUI** (`askConfirm()`, réutilisée) :
- **NON** → RDV unique à la date/heure saisies (comportement normal).
- **OUI** → une 2ᵉ popup (`askRdvDays()`) affiche 7 cases à cocher
  (Lun…Dim), **toutes décochées par défaut** — la personne coche elle-même
  ses jours, ou utilise les boutons raccourcis "5 jours" (Lun-Ven) / "7
  jours" (Lun-Dim). **Une seule heure pour tous les jours cochés** (pas de
  saisie par jour — le formulaire n'a qu'un seul champ HEURE). Annuler ou
  valider sans aucun jour coché → création abandonnée (toast "Création
  annulée").

⚠️ **Piège découvert le 14/08 — la récurrence n'est PAS un vrai `rrule` :**
un premier essai envoyait `rrule: "FREQ=WEEKLY;BYDAY=..."` au service
`calendar.create_event`. Vérifié sur la doc officielle HA (re-vérifié le 2026-09-13 sur HA 2026.9.2,
https://www.home-assistant.io/actions/calendar.create_event/) :
**ce service ne supporte QUE** `summary`, `description`, `start_date_time`/
`end_date_time`, `start_date`/`end_date`, `in`, `location` — **pas de champ
`rrule`**. C'est une demande d'évolution encore ouverte côté HA (voir
[discussion communautaire](https://community.home-assistant.io/t/add-recurrence-id-and-rrule-into-service-create-event/885799)),
pas un bug de ce projet. Le `rrule` envoyé était silencieusement ignoré —
le RDV se créait, mais jamais récurrent.

**Solution retenue (validée par l'utilisateur) — voir
`packages/oblig_m03_ecran_msg/m03_rdv_recurrents.yaml` :**
1. La 1ʳᵉ occurrence (date/heure saisies dans le formulaire) est créée
   normalement via `calendar.create_event`, exactement comme un RDV unique.
2. Si récurrent, la règle (jours cochés + heure + note) est en plus
   envoyée à `shell_command.m03_rdv_recurrents` (action `add`), qui
   l'ajoute à `www/rdv_recurrents.txt` (1 ligne par règle :
   `id|joursCSV|HH:MM|note`, script `shell_scripts/m03_rdv_recurrents.py`).
3. Une **automation quotidienne** (`m03_rdv_recurrents_creer_du_jour`,
   trigger `time: "00:05:00"`) calcule le jour de la semaine du jour même
   (`['MO','TU',...][now().weekday()]`, indépendant de la locale du
   serveur — évite le piège de `now().strftime('%a')` qui dépend de la
   locale système), appelle `shell_command.m03_rdv_recurrents` (action
   `today`) pour récupérer les règles du jour, puis crée l'événement
   correspondant via `calendar.create_event` — un par un (`repeat: for_each`).
   Récurrence indéfinie, tant que la règle n'est pas supprimée.

**Conséquence pour le dédoublonnage kiosk/liste (voir plus bas) :**
chaque occurrence quotidienne est un **événement distinct avec son propre
`uid`** (pas une série RRULE avec un `uid` partagé) — l'automation ne crée
QUE l'occurrence du jour, jamais plusieurs jours à l'avance. Il n'y a donc
normalement **jamais deux occurrences simultanées** du même RDV récurrent
dans le calendrier ; le badge 🔁 (dédoublonnage par `uid`, décrit plus bas)
ne se déclenchera donc quasiment jamais avec cette implémentation — ce
n'est pas un bug, juste un mécanisme devenu inutile pour ce cas précis (il
reste utile si `local_calendar` supporte un jour un vrai `rrule` créé par
un autre moyen, ex. directement dans l'UI HA).

**Révision 2026-09-13/14 — bugs RDV/récurrences corrigés :**
1. ⚠️ **L'automation quotidienne ne créait RIEN depuis sa mise en place** :
   elle plantait à chaque exécution — `TypeError: can only concatenate str
   (not "datetime.timedelta") to str` au calcul de l'heure de fin. Corrigé
   (calcul en une seule expression `| as_datetime` + `timedelta`, dans les
   blocs jour ET lendemain).
2. **Suppression d'un RDV inopérante** : la page appelait le service REST
   `calendar/delete_event` **qui n'existe pas** (HTTP 400 — HA n'expose en
   REST que `create_event`/`get_events`) → remplacé par la commande
   **WebSocket** `calendar/event/delete` (`haDeleteEventWebSocket`).
3. **Empilement de doublons** à chaque création → **anti-doublon aux 3
   endroits** : formulaire `creerRdv()`, script `m03_rdv_recurrents.py::do_add`,
   automation (via `calendar.get_events` + condition).
4. **v14.4 — suppression refusée silencieusement chez l'utilisateur** (mais
   OK sur navigateur de test) : le WebSocket s'authentifiait avec `token`
   (= `ha_token` longue durée, **vide** en usage normal) au lieu de
   `currentToken()` (= session HA `hassTokens` en priorité). Diagnostiqué via
   la page `www/wsdiag.html` et le contrôle direct du navigateur de
   l'utilisateur ; corrigé et validé en direct.
5. `aidant.html` : **auto-mise à jour** (`APP_VERSION` + rechargement auto,
   contre le cache HTTP de 31 jours des fichiers `/local/`).

**Liste "🔁 RENDEZ-VOUS RÉCURRENTS" (sous la liste des RDV, 14/08) :**
seul endroit où gérer les RÈGLES elles-mêmes (pas les occurrences déjà
créées). `refreshRdvRecurrentsList()` appelle
`POST /api/services/shell_command/m03_rdv_recurrents?return_response=true`
(action `list`), affiche jours + heure + note, bouton 🗑️ → action `delete`
(arrête les créations futures **ET supprime les occurrences À VENIR au
même intitulé + même heure** — comportement demandé par l'utilisateur,
ajouté le 2026-09-13).
✅ **Vérifié en live les 13-14/09** : la liste et les actions
(`list`/`add`/`remove`) fonctionnent via l'API REST avec `return_response`
(le mécanisme supposé ci-dessus est confirmé).

**Liste "📋 RENDEZ-VOUS À VENIR" (sous le bouton de création, 14/08) :**
`refreshRdvList()` lit `GET /api/calendars/calendar.calendrier_local?start=...&end=...`
(60 jours), affiche chaque événement (date/heure + note) avec un bouton 🗑️.
Suppression : modale de confirmation custom (`askConfirm()`, boutons NON/OUI —
pas le `confirm()` natif du navigateur) puis `calendar.delete_event` avec
l'`uid` de l'événement.
⚠️ **Non vérifié en live cette session (pas d'accès API)** : la suppression
suppose que l'API `/api/calendars/...` renvoie bien un champ `uid` par
événement pour `local_calendar` (c'est le comportement standard documenté de
l'entité `CalendarEvent` de HA, mais pas testé ici). Si le bouton 🗑️ échoue
avec "Impossible d'identifier ce rendez-vous", vérifier la présence du champ
`uid` dans la réponse de l'API calendrier.

## Affichage kiosk (`kiosk.html`, section calendrier) — reprécisé le 15/08

**Une seule ligne affichée : le rendez-vous le plus proche.** Pas de liste
de plusieurs RDV en parallèle (contrairement à une première version du
14/08, corrigée le 15/08 après retour utilisateur — la 1ʳᵉ implémentation
montrait jusqu'à 3 lignes en rotation par page, ce n'était pas ce qui était
demandé).

Fenêtre de recherche glissante **7 jours** (`CAL_WINDOW_DAYS`), dédoublonnage
des récurrents par `uid` (garde la 1ʳᵉ occurrence). Le "créneau le plus
proche" = la date+heure exacte du 1ᵉʳ événement restant après tri.

**S'il y a plusieurs RDV EXACTEMENT au même créneau** (double réservation) :
carrousel lent entre eux, **max 3** (`CAL_MAX_SAME_SLOT`), **chaque RDV reste
affiché 1 minute** (`CAL_SLOT_MS = 60000`) avant de passer au suivant
(compteur "(2/3)" affiché). S'il n'y en a qu'un seul au créneau le plus
proche (cas normal), ligne fixe, pas de rotation.

⚠️ **Garde-fou important :** `refreshCalendar()` est rappelée toutes les 20 s
(`REFRESH`, poll global du kiosk) — bien plus souvent que le délai d'1 min
par RDV. Sans protection, le carrousel repartirait de zéro à chaque poll et
n'afficherait jamais un RDV plus de 20 s. Comme pour `lastMainKey` (section
vidéo), le code compare le groupe de RDV du créneau le plus proche à celui
déjà affiché (par liste d'`uid`) et ne touche au DOM / ne redémarre le
minuteur QUE si le groupe a réellement changé.

Un RDV récurrent (infirmière tous les matins, etc.) n'est en pratique
**jamais en conflit avec lui-même** — l'automation quotidienne ne crée
qu'une seule occurrence à la fois (voir section Récurrence ci-dessus), donc
le carrousel "même créneau" ne se déclenche que pour de vraies coïncidences
(plusieurs RDV différents pris au même moment).

**"Interdire plus de 3 RDV à la même heure" :** couvert côté AFFICHAGE
(`CAL_MAX_SAME_SLOT = 3`, les RDV au-delà du 3ᵉ sur un même créneau ne sont
simplement jamais montrés au kiosk). **Toujours pas de limite à la
création** dans `aidant.html` — n'importe quel nombre de RDV peut être créé
sur le même créneau, seul l'affichage est plafonné. Pas redemandé depuis, à
faire séparément si besoin.

## Vérification `entity_id`

Contrairement à Confo_M34 (voir `M34_television.md`), ce module **n'a pas
été renommé** lors du passage à la numérotation par groupe — seul le label
"oblig_M03" a changé, pas les `unique_id`/`name:` du YAML. Les `entity_id`
des 3 capteurs template (`sensor.m03_agenda_formate`, `sensor.m03_texto_formate`,
`sensor.m03_bandeau_principal`) correspondent bien à leur `unique_id`,
confirmé par leur usage fonctionnel direct dans `aidant.html` et
`kiosk.html`. Les `entity_id` des 3 automations (dérivés du texte `alias:`,
pas de `id:`) n'ont pas été vérifiés dans `.storage/core.entity_registry`
cette session (pas d'usage direct par `entity_id` ailleurs dans le code —
seulement des triggers `event`/`platform: time`, donc pas de risque de bug
silencieux comme sur M34, mais à vérifier si un jour une autre entité doit
les référencer).

## Chaîne de dépendances complète

```
1. www/aidant.html (bouton "Envoyer le message")
   └─> script.m03_envoyer (champ auteur = hass.user.name)
        └─> conditions : message valide / file pas pleine (m03_queue_max)
            / plage horaire (m03_envoi_debut→fin) / rate limit
            (m03_rl_max msgs / m03_rl_fenetre min, par auteur)
        └─> shell_command.m03_log_message → /config/m03_historique.txt
        └─> ajoute message+auteur+heure aux 3 files (queue_msg/_auteur/_timestamps)
        └─> met à jour input_text.m03_rate_limit (purge des entrées expirées)
        └─> vide input_text.m03_message_famille (feedback champ immédiat)
        └─> si rien affiché → script.m03_afficher_suivant (immédiat)
            sinon si timer idle → timer.start (durée = m03_affichage_duree)

2. script.m03_afficher_suivant (déclenché par timer.finished / reboot / envoi)
   └─> pop le 1er message de la file → input_text.m03_affiche_msg/_auteur
   └─> horodate input_datetime.m03_affiche_depuis
   └─> retire DÉFINITIVEMENT le message de la file (fix 14/08 — voir Pièges §6)
   └─> relance timer.m03_rotation SEULEMENT s'il reste des messages en file

3. sensor.m03_texto_formate (trigger /1 min + state m03_affiche_*)
   └─> texte formaté "💬 auteur : message" + âge (à l'instant / il y a Xmin)

4. sensor.m03_agenda_formate (trigger /1 min + state calendar.calendrier_local)
   └─> texte formaté "📅 titre — délai"

5. sensor.m03_bandeau_principal (trigger /1 min + state des 2 précédents)
   └─> arbitre : agenda urgent/en_cours > proche > texto actif > agenda futur
   └─> consommé par aidant.html (BANDEAU KIOSK LIVE) et kiosk.html (msg-box)
```

## Automations

| ID | Alias | Déclencheur | Action |
|:---|:------|:------------|:-------|
| `m03_rotation_timer_finished` | M03 — Rotation : afficher message suivant | Event `timer.finished` sur `timer.m03_rotation` | Appelle `script.m03_afficher_suivant` |
| `m03_reprise_timer_apres_reboot` | M03 — Reprendre rotation après redémarrage HA | `homeassistant` start (+ delay 30 s) | Si rien affiché + file non vide → affichage immédiat ; sinon si file non vide → `timer.start` (durée `m03_affichage_duree`) |
| `m03_clear_queue_minuit` | M03 — Vider la file à minuit | `time` à `00:00:00` | Vide `m03_queue_msg`, `m03_queue_auteur`, `m03_queue_timestamps`, `m03_rate_limit` |

## Scripts

| ID | Mode | Rôle |
|:---|:-----|:-----|
| `m03_envoyer` | queued (max 10) | Envoi d'un message — 4 conditions (voir chaîne de dépendances), log, ajout aux files, affichage/relance timer |
| `m03_afficher_suivant` | single | Pop + affiche le prochain message de la file, ne le remet plus en fin (fix 14/08) |

`script.m03_reset_reglages` (fichier `m03_reset_reglages.yaml`) **supprimé le
14/08** — orphelin depuis le 13/08, valeurs codées en dur obsolètes (voir
Annotations). Le bouton reset actuel est une réimplémentation indépendante,
voir ci-dessous.

## Interface (`aidant.html`) — écran Paramètres messages

| Réglage | Entité HA | Défaut (`config.json` → `defauts_m03`) |
|:--------|:----------|:----------------------------------------|
| Taille max file | `input_number.m03_queue_max` | **5** |
| Durée d'affichage | `input_number.m03_affichage_duree` | 15 min |
| Limite d'envoi (nb msgs) | `input_number.m03_rl_max` | 1 |
| Limite d'envoi (fenêtre) | `input_select.m03_rl_fenetre` | 30 min |
| Plage horaire début | `input_datetime.m03_envoi_debut` | 08:00 |
| Plage horaire fin | `input_datetime.m03_envoi_fin` | 19:00 |

Bouton **"Remettre les valeurs par défaut"** (ajouté 14/08) : fonction
`resetReglagesDefaut()` dans `aidant.html`, appelle directement les 6
services HA (`input_number.set_value`, `input_select.select_option`,
`input_datetime.set_datetime`) avec les valeurs lues via `usineM03()` →
`config.json`. C'est désormais la **seule** implémentation du reset —
`script.m03_reset_reglages` (orphelin, valeurs obsolètes) a été supprimé
le 14/08.

## Pièges connus / notes de dépannage

1. **`initial:` retiré des réglages** (13/08) — `m03_rl_max`,
   `m03_affichage_duree`, `m03_queue_max`, `m03_rl_fenetre`,
   `m03_envoi_debut`, `m03_envoi_fin` n'ont plus de `initial:` dans le YAML
   (sinon HA réinitialise à chaque redémarrage). Reste `m03_message_auteur`
   (`initial: "La famille"`), voulu.
2. **File limitée à 255 caractères** — `m03_queue_msg`/`m03_queue_auteur`
   max 255 : troncature possible si beaucoup de messages simultanés ; la
   condition "file pas pleine" de `m03_envoyer` protège en amont via
   `m03_queue_max`.
3. **Rate limit et plage horaire silencieux** — un envoi refusé ne montre
   aucune erreur explicite (juste une condition non remplie côté script) ;
   c'est le bouton "Envoyer" côté `aidant.html` qui doit afficher la vraie
   raison (voir §7 ci-dessous).
4. **Service `input_datetime.set_value` n'existe plus** dans cette version
   de HA → toujours utiliser `input_datetime.set_datetime` (sinon HTTP 400).
5. ✅ **`script.m03_reset_reglages` (`m03_reset_reglages.yaml`) supprimé le
   14/08.** Il était orphelin depuis le 13/08 (son seul appelant,
   `dashboard_aidant_v2.yaml`, avait déjà été retiré) et ses valeurs codées
   en dur (`queue_max=8`, `envoi_debut=09:00`) ne correspondaient plus aux
   vraies valeurs d'usine (`config.json` = `queue_max:5`, `envoi_debut:08:00`).
   Le bouton "Remettre les valeurs par défaut" de `aidant.html` est
   désormais la seule implémentation du reset — voir section Interface
   ci-dessus. Fichier supprimé (local + `Z:\`) et scripts rechargés côté
   HA (14/08) — l'entité `script.m03_reset_reglages` n'existe plus.
6. **Rotation infinie corrigée (14/08)** — avant : `m03_afficher_suivant`
   remettait le message affiché en fin de file (A→B→C→A→… en boucle
   perpétuelle). Depuis : le message est retiré définitivement une fois
   montré ; le timer ne redémarre que s'il reste des messages.
7. **Ordre des vérifications du bouton Envoyer corrigé (14/08)** —
   `updateSendButton()` dans `aidant.html` vérifiait "message non vide" AVANT
   les restrictions (file pleine / plage horaire / rate limit), donc une
   restriction active ne s'affichait qu'après avoir commencé à taper.
   Réordonné : restrictions vérifiées en premier.
8. **Seuil 3 couleurs ajouté (14/08)** — `MIN_CHARS = 5` : gris (vide) → bleu
   `typing` (1-4 caractères, pas encore envoyable) → vert `ready` (5+
   caractères, envoyable).
9. **Boîte "ℹ️ Message en cours d'affichage" retirée (14/08)** — faisait
   triple emploi avec BANDEAU KIOSK (LIVE) et MESSAGES EN COURS (tag "EN
   COURS D'AFFICHAGE"). La boîte `hint-card` reste utilisée pour la file
   d'attente ("N messages en attente — dans X min"), info non dupliquée
   ailleurs.
10. **Incohérence `queue_max` corrigée (14/08)** — `config.json` avait
    `queue_max: 8` alors que le slider de `aidant.html` affiche "5
    recommandé" et les `DEFAUTS` JS embarqués valent 5. Remis à 5 dans
    `config.json`. ⚠️ Si l'entité live `input_number.m03_queue_max` a déjà
    été forcée à 8 par un ancien reset, elle ne se corrigera pas toute
    seule — cliquer sur "Remettre les valeurs par défaut" la réaligne.
11. **Événement passé (agenda)** : `sensor.m03_agenda_formate` en état
    `passe` a un attribut `texte` vide — rien n'est affiché.
12. **Reboot** : reprise automatique 30 s après démarrage HA
    (`m03_reprise_timer_apres_reboot`) ; les templates filtrent `''`/`unknown`/
    `unavailable` pour éviter "unknown : unknown" à l'écran.

## Fichiers impliqués

| Fichier | Rôle |
|:---|:---|
| `packages/oblig_m03_ecran_msg/m03_ecran_msg.yaml` | Source de vérité — helpers, timer, automations, scripts, 3 sensors template |
| ~~`packages/oblig_m03_ecran_msg/m03_reset_reglages.yaml`~~ | **Supprimé le 14/08** (orphelin, valeurs obsolètes — voir Piège §5) |
| `packages/oblig_m03_ecran_msg/m03_rdv_recurrents.yaml` | **Nouveau 14/08** — `shell_command.m03_rdv_recurrents` + automation quotidienne de création des occurrences (contournement absence de `rrule`) |
| `shell_scripts/m03_rdv_recurrents.py` | **Nouveau 14/08** — lit/écrit `www/rdv_recurrents.txt` (règles de récurrence) |
| `www/rdv_recurrents.txt` | **Nouveau 14/08** — base plate des règles récurrentes (1 ligne = 1 règle, format `id\|joursCSV\|HH:MM\|note`) |
| `www/aidant.html` | Saisie message, BANDEAU KIOSK (LIVE), MESSAGES EN COURS, écran Paramètres (réglages + bouton reset), formulaire RDV + liste RDV + liste récurrences ; bloc RDV encadré par `#only-rdv-block` depuis le 15/08 |
| `www/kiosk.html` | Affiche `sensor.m03_texto_formate` dans `msg-box`, agenda dans `calendar-box` (carrousel) |
| `www/config.json` | Valeurs d'usine (`defauts_m03`) lues par `aidant.html` et par le bouton reset |
| `www/calendrier.html` | **Nouveau 15/08** — page dédiée (bouton dans `aidant.html`, PIN requis) qui embarque `aidant.html?only=rdv` en iframe pour n'afficher que le bloc RDV — voir `M10_gestion_aidants.md` pour le mécanisme PIN |
| `dashboards/dashboard_aidant.yaml` | Coquille iframe vers `aidant.html` (via `launch.html`) |

## Annotations (historique)

- 2026-08-11 (v2→v3) : file de rotation + fix "unknown" + affichage immédiat ;
  ajout `m03_envoyer` (plage horaire, rate limit, file d'horodatages), reprise
  après reboot, durée/limites configurables, sensors passés en trigger-based.
- 2026-08-13 : `initial:` retirés des réglages persistants (sauf
  `m03_message_auteur`) ; ajout de `script.m03_reset_reglages` (jamais
  vraiment câblé à une UI active — retiré avec `dashboard_aidant_v2.yaml`
  le même jour) ; découverte des 3 sources de défauts non alignées.
- 2026-08-14 : clôture — file qui ne se vidait plus (retrait définitif au
  lieu de remise en fin), ordre des vérifications du bouton Envoyer corrigé,
  seuil 3 couleurs (gris/bleu/vert, 5 caractères mini), bouton "Remettre les
  valeurs par défaut" ajouté dans `aidant.html` (lit `config.json`), boîte
  "en cours d'affichage" dédupliquée, incohérence `queue_max` (8→5) corrigée
  dans `config.json`, `script.m03_reset_reglages`/`m03_reset_reglages.yaml`
  supprimé (orphelin depuis le 13/08, valeurs obsolètes, plus aucun appelant).
- 2026-08-14 (suite) : `calendar.google_agenda_famille` (jamais créé, Google
  Calendar abandonné) remplacé par `calendar.calendrier_local` (intégration
  native HA "Local Calendar") — mis à jour dans `m03_ecran_msg.yaml` et
  `kiosk.html`. Ajout d'un formulaire de création de rendez-vous dans
  `aidant.html` (date + heure + note ≤ 60 car.) via le service générique
  `calendar.create_event`, durée par défaut 30 min. `kiosk.html` : agenda et
  messages alignés (1.3em, gras).
- 2026-08-14 (fin) : liste "RENDEZ-VOUS À VENIR" ajoutée dans `aidant.html`
  sous le formulaire, avec suppression par événement (`calendar.delete_event`
  + modale de confirmation custom NON/OUI) — non vérifié en live (pas
  d'accès API cette session), voir avertissement ci-dessus.
- 2026-08-14 (fin, suite) : récurrence repensée en popup (au lieu du menu
  déroulant initial) — "Récurrent ?" NON/OUI puis, si OUI, 7 cases à cocher
  (vides par défaut) + raccourcis 5j/7j, une seule heure pour tous les jours.
  Affichage kiosk des RDV plafonné à 3 lignes + carrousel lent (9 s) si plus,
  fenêtre glissante 7 jours, dédoublonnage des récurrents par `uid`.
- 2026-08-14 (fin, suite 2) : **découverte que `calendar.create_event` ne
  supporte pas `rrule`** (vérifié sur la doc officielle HA 2026.8.2) — la
  récurrence par `rrule` créée juste avant ne fonctionnait donc pas
  (silencieusement ignorée). Remplacée par une vraie solution : package
  `m03_rdv_recurrents.yaml` (règles stockées dans `www/rdv_recurrents.txt`
  via `shell_scripts/m03_rdv_recurrents.py`, automation quotidienne
  `m03_rdv_recurrents_creer_du_jour` à 00:05 qui crée l'occurrence du jour).
  Nouvelle liste "🔁 RENDEZ-VOUS RÉCURRENTS" dans `aidant.html` pour gérer
  (et arrêter) les règles — non vérifiée en live (pas d'accès API cette
  session).
- 2026-08-15 : retour utilisateur — le bandeau calendrier du kiosk affichait
  jusqu'à 3 lignes en rotation (version du 14/08), ce n'était pas la demande.
  Repensé : **une seule ligne, le RDV le plus proche uniquement.** Carrousel
  seulement si plusieurs RDV au même créneau exact (max 3), 1 minute par RDV
  affiché. Ajout d'un garde-fou pour éviter que le poll 20 s du kiosk ne
  redémarre le carrousel avant la fin de la minute (comparaison du groupe de
  RDV par liste d'`uid`, même principe que `lastMainKey`).
- 2026-08-15 (correctif) : bug `?return_response=true` → `?return_response`
  corrigé dans `refreshRdvRecurrentsList()` (`aidant.html`), repéré par
  analogie avec le même bug confirmé en direct sur M31 (photos) — **non
  retesté en direct sur M03 spécifiquement**.
- 2026-08-15 (suite) : page dédiée `calendrier.html` — bouton dans `aidant.html`
  (zone « 🔗 Pages dédiées »), protégé par un code PIN partagé
  (`input_text.m10_pin_pages_dediees`, voir `M10_gestion_aidants.md`). Le bloc
  RDV (formulaire + liste + récurrents) a été encadré par `#only-rdv-block`
  dans `aidant.html` ; `calendrier.html` embarque `aidant.html?only=rdv` en
  iframe plutôt que de dupliquer la logique — une seule source de vérité.
  Non vérifié en direct cette session.
- 2026-08-15 (suite, retour utilisateur) : le bloc « Prendre un rendez-vous »
  (formulaire + liste + récurrents, `#only-rdv-block`) est désormais **caché
  par défaut** sur l'écran principal d'`aidant.html` — la page dédiée
  `calendrier.html` suffit. Reste dans le DOM (nécessaire pour le mode
  `?only=rdv`), juste masqué par CSS (`#only-rdv-block { display: none; }`).
  Poussé et vérifié MD5 ; pas de redémarrage HA requis (changement HTML/CSS
  pur).
- 2026-08-15 (suite) : `calendrier.html` s'ouvre désormais en **overlay
  iframe** depuis `aidant.html` (`openCalendrier()`/`closeCalendrier()`) au
  lieu d'une navigation plein écran (`window.location.href`) — hypothèse :
  l'app Companion Android (confirmée via log HA côté téléphone) perd le
  contexte de session authentifiée lors d'une navigation plein écran, comme
  `config.html` (toujours en iframe) n'a jamais eu ce problème. Le bouton
  retour de `calendrier.html` appelle `window.parent.closeCalendrier()` avec
  repli sur l'ancienne navigation si ouvert hors iframe. Voir
  `M31_photos.md` pour le détail complet du diagnostic 401. Poussé et
  vérifié en direct (fichier servi par HA) ; **non confirmé par
  l'utilisateur**.
- 2026-08-18 : demande utilisateur, par analogie avec le même travail fait sur
  le bouton visio (M33) — `updateSendButton()` précisait « ⏰ Envoi désactivé
  (…) » et « Envoi… » sans le mot « message ». Devenu « ⏰ Envoi de message
  désactivé (…) » et « Envoi de message… ».
- 2026-08-18 (suite, **tous les cas de figure**) : demande utilisateur —
  audit complet des 6 états de `updateSendButton()`. 2 en manquaient encore :
  « Attendre encore ~X min » (limite de débit) → « Envoi de message —
  attendre encore ~X min » ; « Encore X caractère(s)… » (message trop court)
  → « Message — encore X caractère(s)… ». Les 4 autres (« Envoyer le
  message », « Saisir un message… », « File pleine — max X messages »,
  « Envoi de message… » pendant l'appel réseau) contenaient déjà « message ».
  Les 6 états du bouton mentionnent maintenant tous « message ». Poussé (MD5
  vérifié).
