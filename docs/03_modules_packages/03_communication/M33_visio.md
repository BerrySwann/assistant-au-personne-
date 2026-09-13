# M33 — Visio Conférence

> Fiche réécrite le 2026-08-15 (remplace `M20_visio.md`, jamais renommée
> depuis le pivot Google Meet du 12/08 puis le renommage de fichier
> `m20_visio.yaml` → `m33_visio.yaml` du 13/08). Source : `raspi/packages/m33_visio.yaml`.
> Source live : `Z:\packages\m33_visio.yaml`.

## Rôle
**Depuis le 2026-08-16 : visioconférence maison (WebRTC), pair-à-pair, sans
service externe.** L'aidant appelle depuis `www/aidant.html`, l'écran de la
personne aidée (`www/kiosk.html`) répond automatiquement, sans aucun clic.
Voir la section « VISIO MAISON » plus bas pour le détail.

L'ancien mécanisme Google Meet (`input_text.m33_visio_url` + iframe) reste
présent dans le code en repli, mais n'est plus le chemin normal : il imposait
un écran « Rejoindre » à la personne aidée, ce que le cas d'usage
(Alzheimer) ne permet pas.

Priorité d'affichage du cadre kiosk : **Appel en cours > Visio Meet (si
activée) > TV (M34) > Photos (M31)**.

## Historique
Conçu à l'origine comme intégration Jitsi (exploration `custom_components/visio_jitsi`, archivée dans `visio_meet.jit.si/`, non retenue). **Pivot Google Meet acté le 2026-08-12** (décision utilisateur — projet grand public non-technicien, besoin d'hyper simple) : salle permanente `meet.google.com/czg-supk-snw`. Fichier `m20_visio.yaml` renommé `m33_visio.yaml` le 13/08.

## Révision 2026-08-15 — unification du double mécanisme
Jusqu'ici, DEUX mécanismes d'URL visio coexistaient, non synchronisés :
- `input_text.m33_visio_url` (côté HA, consommé par `kiosk.html`)
- `localStorage.visio_url` dans `aidant.html` (carte de config dédiée « Lien Visio », valeur d'usine dans `www/config.json`)

Un changement d'URL dans l'un des deux mécanismes n'était PAS répercuté dans l'autre. **Unifié le 15/08** :
- `www/aidant.html` : carte « Lien Visio » et son mécanisme `localStorage` **supprimés**. Le bouton « Lancer la Visio » lit désormais `input_text.m33_visio_url` en direct via l'API HA (`launchVisio()`).
- `www/config.html` (onglet Confort → section « 📹 M33 — Visio ») : nouveau champ pour éditer `input_text.m33_visio_url` — c'est désormais le seul point de configuration.
- `www/config.json` : entrée `visio_url` (ancien mécanisme de valeur d'usine) supprimée.

⚠️ **Non vérifié en direct cette session** (pas de token HA actif) : à confirmer que `input_text.m33_visio_url` porte bien une valeur sur l'instance live (sinon `aidant.html` affiche « URL Visio non configurée » au clic).

## Dépendances
| Élément | Source | Statut |
|:--------|:-------|:-------|
| `input_boolean.module_m33_visio` | M00 (`m00_modules.yaml`) | ⚠️ Déjà déclaré dans `m00_modules.yaml` — NE PAS le redéclarer ici (conflit de clé entre packages) |
| Zone principale du kiosk TV | `www/kiosk.html` | Bascule Visio (priorité) / TV (M34) / Photos (M31) — logique dans `refreshMain()` |
| Salle Google Meet de la famille | Externe | URL renseignée manuellement via `config.html` |

## Entités
| Entité | Rôle |
|:-------|:-----|
| `input_boolean.m33_appel_en_cours` | 🆕 16/08 — Signal d'appel visio maison. Allumé par l'aidant, surveillé par le kiosk (sondage dédié 2 s). |
| `input_text.m33_appel_par` | 🆕 16/08 — Nom de l'aidant en ligne. Affiché aux autres aidants (« Appel en cours avec X ») et vidé au raccrochage, manuel comme automatique. |
| `shell_command.m33_visio_signal_envoyer` | 🆕 16/08 — Dépose un message de signalisation (base64) pour l'autre correspondant |
| `shell_command.m33_visio_signal_lire` | 🆕 16/08 — Relève les messages en attente (lecture destructrice), appelé avec `?return_response` **sans `=true`** |
| `shell_command.m33_visio_signal_purger` | 🆕 16/08 — Vide les deux boîtes, appelé au début et à la fin de chaque appel |
| `input_text.m33_visio_url` | URL Google Meet — mécanisme de repli, plus le chemin normal |
| `input_datetime.m33_horaire_debut` / `_fin` | 🆕 18/08 — Plage horaire d'appel autorisée (voir section dédiée plus bas). Réglage déplacé le même jour de l'onglet Aidants vers 📺 Vidésio (regroupé avec les horaires TV) |
| `input_boolean.m33_appel_urgent` | 🆕 18/08 — Passe outre la plage horaire pour l'appel en cours |
| `input_boolean.m33_horaires_initialises` | 🆕 18/08 — État interne du seed horaires par défaut (voir plus bas), pas destiné à être modifié à la main |

## Automations
Aucune automation dans le YAML source. La bascule du cadre kiosk (Visio / TV / Photos) est gérée côté client par `www/kiosk.html`, pas en YAML.

## Correctif 2026-08-15 (même jour, suite, audit sécurité) — liste blanche d'URL
Audit sécurité externe (Hermes) sur `raspi/www/` : `input_text.m33_visio_url` est un champ HA libre, éditable par n'importe quel compte HA (même non-admin, via l'API/UI), injecté brut dans `kiosk.html` en `<iframe src="..." allow="camera; microphone; fullscreen">` **sans aucune validation**. Un lien de phishing collé par erreur (ou malveillance) s'y serait ouvert en plein écran sur le kiosk, avec caméra+micro autorisés automatiquement, sans clic de l'utilisateur — risque confirmé réel après vérification indépendante du code.
- **Correctif** : `isTrustedVisioUrl(url)` (nouvelle fonction, dupliquée dans `kiosk.html` et `aidant.html`) — vérifie `protocol === 'https:' && hostname === 'meet.google.com'` avant d'ouvrir l'iframe (kiosk) ou `window.open()` (bouton « Lancer la Visio » dans aidant.html). URL non conforme → message d'avertissement affiché à la place, rien n'est ouvert.
- Cohérent avec le pivot Google Meet acté le 12/08 (salle permanente unique) — Jitsi n'étant plus utilisé, aucune raison d'accepter d'autres domaines.
- **Déployé et vérifié en direct** (`curl` : présence confirmée de `isTrustedVisioUrl` dans les deux fichiers servis par HA). Pas testé avec une vraie URL malveillante par l'utilisateur (comportement attendu, pas de risque à le vérifier en conditions réelles).

## ✅ 2026-08-16 — VISIO MAISON (WebRTC) : CONSTRUITE ET FONCTIONNELLE

**État : opérationnelle, confirmée en direct par l'utilisateur.** Remplace
Google Meet. Ce qui suit documente le parcours complet (y compris les pistes
écartées) pour ne pas refaire le même chemin.

### Ce qui tourne aujourd'hui
L'aidant appuie sur **📹 Appeler** dans l'interface Aidant → l'écran de la
personne aidée bascule **tout seul** sur l'appel, **sans aucun clic de sa
part**. L'aidant raccroche → l'écran revient seul aux photos (ou à la TV).

| Élément | Rôle |
|:--------|:-----|
| `input_boolean.m33_appel_en_cours` | Signal d'appel. Allumé par l'aidant, surveillé par le kiosk. |
| `shell_command.m33_visio_signal_envoyer` / `_lire` / `_purger` | Canal de signalisation (SDP + candidats ICE), voir `shell_scripts/m33_visio_signal.py` |
| `www/aidant.html` | Côté appelant : caméra, offre WebRTC, panneau vidéo, raccrochage |
| `www/kiosk.html` | Côté récepteur : réponse automatique, affichage plein cadre |

**L'image et le son passent en direct d'un appareil à l'autre** (P2P). Home
Assistant ne sert qu'à l'établissement de la connexion. Aucun service externe,
aucun compte, aucune salle, aucun abonnement.

### Pourquoi shell_command et pas les événements WebSocket
Les commandes `fire_event` / `subscribe_events` transportent parfaitement un
SDP de 4 Ko (testé en direct), **mais sont réservées aux comptes ADMIN**. Or
les aidants sont volontairement non-admin (voir M10). Les passer admin pour
qu'ils puissent téléphoner ruinerait tout le système de droits. D'où le
passage par `shell_command`, déjà éprouvé en non-admin pour l'envoi de photos.

### Détails d'implémentation à connaître
- **Base64 obligatoire** : le SDP contient guillemets et sauts de ligne, qui
  ne survivraient pas au passage par une ligne de commande système. La page
  encode avant d'envoyer, décode après lecture.
- **Lecture destructrice** : `_lire` renvoie les messages en attente PUIS vide
  la boîte — sinon la même offre serait retraitée en boucle.
- **Purge au démarrage** : chaque appel commence par `_purger`, sinon les
  restes d'un appel interrompu (page fermée en pleine négociation) font
  échouer le suivant.
- **Sondage rapide dédié** (`APPEL_POLL = 2000` dans kiosk.html) : le cycle
  général du kiosk tourne à 20 s, ce qui donnait 10-20 s de latence avant que
  l'appel n'apparaisse (retour utilisateur). Corrigé par un sondage à 2 s qui
  ne lit qu'UNE entité, plutôt que d'accélérer tout le reste inutilement.
- **`object-fit: contain`** et non `cover` sur les deux vidéos : `cover`
  rognait les bords et coupait le visage (retour utilisateur — effet de zoom
  marqué sur la caméra frontale).
- **Dégradation propre** : si l'écran kiosk n'a pas de caméra, l'appel
  fonctionne quand même (la personne voit et entend l'aidant, qui ne la voit
  pas). Les transceivers passent en `recvonly`.

### 🛡️ Fin d'appel non explicite — le cas critique
Situation réelle signalée par l'utilisateur : *« j'ai fermé l'appli HA et j'ai
ma trombine affichée »*. Si l'aidant ferme son application sans raccrocher,
plus rien n'est transmis et **l'image se FIGE sur l'écran de la personne
aidée**, qui n'a aucun moyen de comprendre ni de réagir. C'est exactement la
situation à ne jamais laisser arriver dans ce projet.

Deux mécanismes complémentaires, car aucun ne couvre tous les cas :

| Mécanisme | Où | Couvre | Délai |
|:----------|:---|:-------|:------|
| `pagehide` + `fetch(keepalive:true)` | `aidant.html` | Fermeture propre de l'application/onglet — le cas courant | Immédiat |
| **Détection de flux mort** (`getStats()` → `bytesReceived`) | `kiosk.html` | Batterie vide, perte réseau, plantage — tout ce que le premier ne peut pas signaler | 6 s |

⚠️ **Pourquoi ne pas se fier aux états WebRTC** (`connectionState` à
`'failed'`/`'disconnected'`) : ils mettent une **trentaine de secondes** à
basculer, le navigateur attendant de constater l'absence de réponse. Beaucoup
trop long ici. D'où la mesure directe des octets reçus : s'ils n'augmentent
plus, plus rien n'arrive, quoi qu'en dise l'état de la connexion.

Réglages (constantes en tête de `kiosk.html`) :
- `VISIO_CYCLES_SANS_FLUX = 6` — secondes sans nouvel octet avant raccrochage
- `VISIO_GRACE_MS = 10000` — délai de grâce sur `'disconnected'` (hoquet Wi-Fi
  qui se répare seul), pour ne pas couper un appel qui allait reprendre
- `VISIO_TIMEOUT_MS = 45000` — abandon si l'appel n'aboutit jamais

Dans tous les cas c'est le **kiosk** qui éteint `input_boolean.
m33_appel_en_cours` : l'aidant retrouve donc aussi son bouton « Appeler » dans
un état cohérent. ✅ Confirmé fonctionnel par l'utilisateur.

### 🔒 Un seul appel à la fois (16/08, suite)
Trou trouvé **sur question de l'utilisateur**, pas en test : que se passait-il
si un 2e aidant appelait pendant un appel ?

Comportement avant correctif :
- Le kiosk **ignorait** la demande (sa surveillance teste « interrupteur
  allumé ET aucun appel actif ») → le 2e aidant restait bloqué
  **indéfiniment** sur « Appel en cours… », sans message ni erreur.
- **Plus grave** : chaque appel démarrait par une purge des boîtes de
  signalisation. Si le 1er appel était encore en train de s'établir, cette
  purge **effaçait son offre** et le faisait échouer silencieusement — le
  nouvel appel détruisait l'appel en cours.
- Le garde-fou `if (visioEnCours)` ne protégeait que du double-clic sur LE
  MÊME appareil ; un autre aidant a sa propre variable, à `false`.

Décision : **un seul appel simultané** (un seul écran, une seule personne
aidée — deux appels n'auraient aucun sens).

| Correctif | Où |
|:----------|:---|
| `visioOccupeParAutre()` — lit l'interrupteur + le nom, ignore notre propre appel | `aidant.html` |
| Refus explicite « Appel déjà en cours avec X » au lieu d'attendre dans le vide | `launchVisio()` |
| **Purge déplacée APRÈS la vérification** — ferme le point le plus grave | `launchVisio()` |
| Bouton **grisé et réellement désactivé** (`btn.disabled`), nommé | `majEtatBoutonAppel()`, sondage 4 s |
| Libération de `m33_appel_par` au raccrochage manuel **et automatique** | `aidant.html` + `kiosk.html` |

⚠️ Le sondage du bouton est à 4 s et non sur le cycle général (30 s), bien
trop lent pour refléter une situation temps réel.

### Ergonomie (retours utilisateur, corrigés le 16/08)
- Le bouton vert « 📹 Appeler » **disparaît pendant l'appel**, remplacé par
  « 📴 Raccrocher » dans le panneau vidéo — ne pas proposer d'appeler alors
  qu'un appel est déjà en cours.
- Vignette locale (sa propre image) en incrustation, état de l'appel affiché
  en haut à gauche du cadre.

### 🕐 Plage horaire + urgence (18/08)
Idée émise le 16/08 (« ne pas réveiller la personne en pleine nuit »),
construite le 18/08. L'appel s'affiche tout seul sur le kiosk, sans sonnerie
ni geste requis — il fallait donc éviter qu'il s'affiche en pleine nuit.

| Entité | Rôle |
|:-------|:-----|
| `input_datetime.m33_horaire_debut` / `_fin` | Plage horaire autorisée (réglée dans `config.html` → Confort → 📺 Vidésio, regroupée avec les horaires TV). Pas de `initial:` (cf. M00/M13) : vaut 00:00–00:00 tant que non réglée → plage vide → tout appel non urgent bloqué. |
| `input_boolean.m33_appel_urgent` | Réglé par `launchVisio()` juste avant l'appel — `on` uniquement si l'aidant a confirmé « appel urgent » dans le pavé rouge (voir plus bas), `off` sinon. Remis à off à chaque raccrochage. **Aucune case à cocher** — état transitoire décidé au clic, pas une préférence persistante. |

**⚠️ Révision 18/08 (même jour, refonte) : la case « 🚨 Urgence » cochée en
permanence a été RETIRÉE.** Retour utilisateur direct : *« c'est quoi cette
crotte ? ça sert à quoi ? c'est moi qui ai demandé ? »* — la plage horaire +
la dérogation urgence, oui (demandées le 16/08) ; la case à cocher en
permanence pour l'obtenir, c'était un choix d'implémentation, jamais demandé,
et redondant avec ce que le bouton affichait déjà. Remplacée par une
**confirmation à la demande** : hors plage, cliquer sur « Appel Visio » ouvre
directement le modal de confirmation générique déjà utilisé ailleurs dans
l'app (`askConfirm()`, bouton « Oui » en rouge — même pavé que pour confirmer
la suppression d'un message ou d'un RDV) : *« ⚠️ Hors plage horaire
(09:00–17:00). Confirmer un appel visio URGENT à la personne aidée ? »*. Dans
la plage horaire normale, ce modal n'apparaît jamais — rien à cocher, rien à
voir.

**Retour visuel sur le bouton « Appel Visio »** (`majEtatBoutonAppel()`,
sondage 4 s) — même logique que le bouton d'envoi des messages
(`.btn-send.plage`) :
- **Dans la plage** : vert, « 📹 Appel Visio ».
- **Hors plage** : ambre/marron (`.btn-visio.hors-plage`), texte
  **« ⏰ Appel Visio désactivé (09:00–17:00) »** — les heures réellement
  configurées (`visioHoraire()`), même principe que « ⏰ Envoi de message
  désactivé (…) » pour les messages. Le bouton reste **cliquable** : cliquer
  dessus déclenche la confirmation « urgent ? » ci-dessus, ce n'est pas une
  impasse.

**Double contrôle, à deux endroits différents, pour deux raisons différentes :**
- `aidant.html` (`launchVisio()`, via `visioHoraire()`/`checkPlage()`) —
  bloque l'appel **avant même de l'envoyer**, avec une confirmation explicite
  hors plage. C'est le chemin normal.
- `kiosk.html` (`visioDoitRepondre()`, dans `refreshMain()` ET
  `surveillerAppel()`) — garde-fou **redondant** : même si
  `m33_appel_en_cours` était allumé par un autre moyen (Outils dev > États,
  script de test...), le kiosk ne répond jamais automatiquement hors plage
  sans le drapeau urgent. N'interrompt jamais un appel déjà en cours — ne
  s'applique qu'au moment de décrocher.

En cas d'erreur réseau ou d'entités pas encore créées (avant le redémarrage
HA), `aidant.html` ne bloque PAS l'appel (fail-open côté aidant : un souci
technique ne doit jamais empêcher un vrai appel). Côté kiosk, une entité
absente/inconnue est traitée comme « plage non réglée » → refus de répondre
(fail-closed côté réception, cohérent avec l'objectif « ne pas réveiller »).

**Défaut 09:00–17:00** (demandé le 18/08, même jour) : plutôt que de laisser
la plage à 00:00–00:00 (vide, tout bloqué) jusqu'à un réglage manuel,
`automation.m33_seed_horaires_defaut` applique 09:00/17:00 **une seule fois**,
au tout premier démarrage HA suivant la création des entités — même
mécanisme que les horaires TV par défaut de M34 (`m34_seed_horaires_defaut`),
gardé par `input_boolean.m33_horaires_initialises` pour ne plus jamais
toucher aux heures une fois réglées manuellement (`initial:` aurait, lui,
écrasé un réglage manuel à CHAQUE redémarrage — piège HA documenté ailleurs
dans le projet, voir M00/M13).

### Reste à faire
- **Caméra sur l'écran kiosk** : le PC de test n'en a pas, donc l'aidant ne
  voit pas encore la personne aidée (l'inverse fonctionne). Question
  matérielle, pas logicielle — le code gère déjà la dégradation.
- **Appel depuis l'extérieur** : non testé. Fonctionnera tant que les deux
  appareils sont sur le réseau Tailscale ; un relais TURN pourrait être
  nécessaire selon les réseaux traversés (voir le prototype `visio_test.html`,
  qui affiche le type de connexion réellement retenu).
- **Supprimer `www/visio_test.html`** une fois le module stabilisé.
- **Token longue durée sur le kiosk** (via l'écran de configuration
  d'`aidant.html`) : sinon la session expire au bout de quelques heures et le
  kiosk devient muet.

### Le problème de départ
Google Meet impose un écran « Rejoindre » à la personne aidée : un clic est
nécessaire pour entrer dans l'appel. Rédhibitoire pour le cas d'usage
(personne Alzheimer devant un kiosk) — l'appel doit s'afficher tout seul.

### Pistes explorées et écartées
| Piste | Résultat |
|:------|:---------|
| **meet.jit.si** (Jitsi public, `prejoinPageEnabled=false`) | ❌ Depuis août 2023, le 1er participant doit s'authentifier (Google/GitHub/Facebook), et **cette authentification est impossible depuis un iframe embarqué** (non implémenté par Jitsi). Le kiosk resterait bloqué sur « en attente du modérateur ». Fonctionnerait UNIQUEMENT si l'aidant rejoint et s'authentifie en premier. |
| **Intégration `visio_jitsi`** (custom, présente sur l'instance depuis le 10/08, hors session, jamais documentée) | ❌ Abandonnée. Services `lancer`/`raccrocher` fonctionnels côté API, mais reposent sur `browser_mod` : aucun navigateur réellement connecté, et l'ID cible est périmé à 3 endroits différents — dont une faute de frappe (`brosser.b19af76_d3adeeb9`) dans sa propre config, et une valeur encore différente dans `input_text.m34_browser_id_tv`. Mécanisme jugé trop fragile. |
| **Auto-héberger Jitsi** | ❌ Incompatible avec la contrainte « simple pour tout le monde » : imposerait serveur + domaine + certificat + ports ouverts à chaque personne installant le système. |
| **WebRTC maison** | 🟡 Concept VALIDÉ, test final non réalisé (voir ci-dessous). |

### WebRTC maison — ce qui est déjà prouvé
Deux points durs levés, testés en direct :
1. **Home Assistant peut servir de serveur de signalisation** — via les
   événements WS personnalisés (`fire_event`/`subscribe_events`). Un SDP de
   4 Ko passe intact. C'est habituellement la brique qu'il faut héberger
   soi-même : ici, aucune infrastructure supplémentaire.
   ⚠️ MAIS ces deux commandes sont **réservées aux comptes ADMIN** →
   inutilisable tel quel pour un aidant non-admin. Solution prévue :
   `shell_command` (déjà prouvé en non-admin pour l'upload photo, gros
   volumes, voir M31).
2. **STUN public suffit à découvrir l'adresse publique** — candidat `srflx`
   obtenu. Reste à confirmer qu'une connexion aboutit réellement, et si un
   relais TURN est nécessaire quand l'aidant appelle depuis l'extérieur (4G).

Prototype : **`raspi/www/visio_test.html`** — page de test autonome
(diagnostic en 4 points + verdict sur le type de candidat ICE retenu).
Référencée nulle part, à supprimer une fois la décision prise.

### ⛔ LE VRAI BLOCAGE : HTTPS obligatoire
Les navigateurs **refusent l'accès caméra/micro** sur une page servie en
`http://` vers une adresse locale. Règle du navigateur, **non contournable par
du code**, et valable pour Meet, Jitsi et toute solution maison
indifféremment. Sans HTTPS, aucune visio n'est possible sur le kiosk.

Solutions de certificat testées le 16/08 :
| Solution | Résultat |
|:---------|:---------|
| Certificat **auto-signé** (généré, en place dans `/ssl/`) | 🟡 Fonctionne dans le navigateur (après acceptation de l'avertissement), mais **casse l'app Companion** qui refuse les certificats auto-signés → inacceptable, les aidants passent par l'app. |
| **DuckDNS → IP locale** | ❌ DuckDNS **refuse de publier une IP privée** (vérifié sur 3 DNS publics : TXT présent, aucun enregistrement A). L'idée ne marche pas. |
| **DuckDNS → IP publique + port 443** | ❌ Refusé par l'utilisateur (« hors de question d'ouvrir un port »). |
| **Nabu Casa** | ❌ Son abonnement est déjà rattaché à son instance de PRODUCTION (1 abonnement = 1 instance). |
| **Tailscale** | 🟡 **Piste retenue, en cours.** Certificat Let's Encrypt valide, aucun port ouvert, accès distant inclus. Add-on installé, MagicDNS + HTTPS activés, nom obtenu : `homeassistant-1.tail0c740d.ts.net`. Contrepartie : app Tailscale à installer sur chaque appareil (kiosk + téléphones des aidants). |

### ✅ Solution HTTPS retenue : Tailscale (résolu le 16/08)
Configuration en place :
- Add-on Tailscale, option **`share_homeassistant: serve`** (et non `funnel`,
  qui exposerait HA sur Internet public) + `share_on_port: 443`.
- **Proxies de confiance obligatoires** côté HA : `127.0.0.1` et `::1`, avec
  « Faire confiance à X-Forwarded-For » activé. Sans ça, l'add-on refuse de
  démarrer (`FATAL: Unable to connect to Home Assistant as reverse proxy`).
  ⚠️ L'interface refusait silencieusement l'enregistrement — il a fallu écrire
  directement dans `.storage/http` puis redémarrer (sauvegarde :
  `.storage/http.bak-2026-08-16`).
- **Aucun certificat SSL dans HA** : c'est Tailscale qui termine le TLS, HA
  reste en HTTP en interne. Les champs de certificat de Paramètres → Système →
  Réseau doivent rester VIDES.

Adresse d'accès : **`https://homeassistant-1.tail0c740d.ts.net`** (sans port).
Chaque appareil devant joindre HA doit avoir le client Tailscale installé et
connecté — c'est ce qui remplace l'ouverture de port.

⚠️ **Changement d'origine = session perdue.** Passer de `http://<ip>:8123` à
l'adresse Tailscale vide le stockage local du navigateur : il faut se
reconnecter à HA sur la nouvelle adresse, sinon les pages tournent sans token
(erreurs `Login attempt failed from localhost` dans le journal).

## Pièges connus / TODO
1. **Vérifier que `input_text.m33_visio_url` a bien une valeur sur l'instance live** après cette révision — sinon le bouton aidant affiche une erreur de configuration au lieu d'ouvrir la visio. ✅ Renseignée le 15/08 : `https://meet.google.com/czg-supk-snw`.
0. ⚠️ **`input_boolean.module_m33_visio` est un interrupteur MANUEL** : tant qu'il est sur ON, le kiosk affiche la salle visio (vide ou non), en priorité sur TV et photos. HA n'a aucun moyen de savoir si un appel est réellement en cours (service externe). Si personne ne le repasse sur OFF après l'appel, le kiosk reste bloqué sur la visio. Un filet de sécurité (extinction automatique après délai) a été évoqué, **non construit**.
2. ⚠️ **Ne pas redéclarer `input_boolean.module_m33_visio`** : déjà déclaré dans `m00_modules.yaml`.
3. ✅ **Validation d'URL ajoutée le 15/08** (voir correctif ci-dessus) : liste blanche stricte `meet.google.com` uniquement, dans `kiosk.html` (iframe) et `aidant.html` (bouton). Si la salle change un jour de domaine (autre que Google Meet), il faudra mettre à jour `isTrustedVisioUrl()` dans les deux fichiers.
4. **À renseigner manuellement** : l'URL Google Meet de la famille doit être saisie via `config.html` (onglet Confort → M33 Visio) avant tout usage.

## Fichiers impliqués
| Fichier | Rôle |
|:--------|:-----|
| `raspi/packages/m33_visio.yaml` | `input_boolean.m33_appel_en_cours`, les 3 `shell_command`, `input_text.m33_visio_url` |
| `raspi/shell_scripts/m33_visio_signal.py` | 🆕 Canal de signalisation WebRTC (boîtes aux lettres dans `/tmp`) |
| `raspi/www/aidant.html` | Côté appelant : `launchVisio()`, `raccrocherVisio()`, panneau vidéo |
| `raspi/www/kiosk.html` | Côté récepteur : `visioDemarrer()`, `visioArreter()`, `surveillerAppel()` |
| `raspi/www/visio_test.html` | Prototype de diagnostic (contexte sécurisé, caméra, type de connexion) — à supprimer une fois le module stabilisé |
| `raspi/www/config.html` | Champ de l'URL Meet (repli) |
| `raspi/dashboards/dashboard_kiosk.yaml` | ⚠️ Cache-bust `?v=N` à incrémenter à CHAQUE modification de `kiosk.html` |

## Annotations
- 2026-08-11 : fiche `M20_visio.md` rédigée — module alors en tout début de développement (Jitsi envisagé).
- 2026-08-12 : pivot Google Meet acté (salle permanente `meet.google.com/czg-supk-snw`).
- 2026-08-13 : fichier YAML renommé `m20_visio.yaml` → `m33_visio.yaml` (la fiche `.md`, elle, n'avait pas suivi).
- 2026-08-15 : fiche réécrite et renommée `M20_visio.md` → `M33_visio.md` (rattrapage) ; double mécanisme d'URL (HA + localStorage aidant) unifié sur `input_text.m33_visio_url` seul, éditable depuis `config.html`.
- 2026-08-15 (même jour, suite, audit sécurité) : liste blanche d'URL (`meet.google.com` uniquement) ajoutée dans `kiosk.html` et `aidant.html`, suite à un audit sécurité externe (Hermes) ayant identifié l'absence totale de validation avant ouverture (iframe caméra/micro auto-autorisés). Vérifié indépendamment avant correctif — risque confirmé réel.
- 2026-08-16 (correctifs sur le mécanisme Meet existant) : (1) `isTrustedVisioUrl()` rejetait à tort une URL collée sans `https://` — `new URL()` lève une exception sur une chaîne sans schéma, et le navigateur interprétait alors `meet.google.com/xxx` comme un chemin relatif (`/local/meet.google.com/xxx`). Corrigé par `normalizeVisioUrl()` (préfixe `https://` si absent AVANT validation ; la liste blanche n'est pas affaiblie), dans `aidant.html` ET `kiosk.html`. (2) `launchVisio()` appelait `window.open()` APRÈS un `await` — donc hors du geste utilisateur, ce qui fait bloquer la popup **silencieusement** par le navigateur (Safari, WebView Companion). Corrigé : ouverture synchrone d'un onglet vide au clic, puis redirection une fois l'URL validée. Les deux confirmés fonctionnels par l'utilisateur.
- 2026-08-16 : exploration complète pour remplacer Google Meet (clic « Rejoindre » rédhibitoire) — Jitsi public, intégration `visio_jitsi`, auto-hébergement, WebRTC maison. Concept validé sur ses 2 points durs (signalisation via HA, STUN), puis bloqué plusieurs heures sur l'obligation de HTTPS pour la caméra (auto-signé → casse l'app Companion ; DuckDNS → refuse les IP privées ; port 443 → refusé par l'utilisateur ; Nabu Casa → abonnement déjà rattaché à sa prod).
- 2026-08-16 (**RÉSOLU**) : HTTPS obtenu via **Tailscale** (`share_homeassistant: serve`) — certificat valide, aucun port ouvert, accès distant inclus. A nécessité de renseigner les proxies de confiance côté HA, l'interface refusant silencieusement l'enregistrement (écriture directe dans `.storage/http`).
- 2026-08-16 (**VISIO MAISON CONSTRUITE**) : `input_boolean.m33_appel_en_cours` + 3 `shell_command` + `shell_scripts/m33_visio_signal.py` (signalisation base64, lecture destructrice, compatible comptes non-admin) ; `aidant.html` réécrit côté appelant (panneau vidéo, offre WebRTC, raccrochage des deux côtés) ; `kiosk.html` réécrit côté récepteur (réponse automatique, priorité absolue sur TV/photos, sondage dédié 2 s). **Confirmée fonctionnelle en direct par l'utilisateur.** Deux correctifs immédiats suite à ses retours : latence de 10-20 s (cycle kiosk à 20 s → sondage dédié à 2 s) et effet de zoom sur la caméra frontale (`object-fit: cover` → `contain`). Bouton « Appeler » masqué pendant l'appel.
- 2026-08-16 (S3, **un seul appel à la fois**) : trou trouvé sur question de l'utilisateur (« si un appel est en cours et qu'un autre aidant appelle ? »), pas en test. Le 2e aidant restait bloqué indéfiniment sans message, et sa purge des boîtes de signalisation pouvait DÉTRUIRE un 1er appel encore en cours d'établissement. Corrigé : `input_text.m33_appel_par` (nom de l'aidant en ligne), refus explicite avec le nom, purge déplacée après vérification, bouton grisé et réellement désactivé (sondage dédié 4 s), libération du nom au raccrochage manuel comme automatique.
- 2026-08-16 (fin de session, **fiabilisation**) : traitement du cas « l'aidant ferme son application sans raccrocher », signalé en conditions réelles — l'image restait figée devant la personne aidée. Deux mécanismes complémentaires ajoutés : `pagehide` + `fetch(keepalive:true)` côté aidant (immédiat, fermeture propre) et **détection de flux mort** côté kiosk via `getStats()`/`bytesReceived` (6 s, couvre batterie vide / perte réseau / plantage). Les états WebRTC natifs ont été écartés pour ça : ~30 s pour basculer, beaucoup trop long. Garde-fous complémentaires : 10 s de grâce sur `'disconnected'`, 45 s de délai maximum si l'appel n'aboutit jamais. Confirmé fonctionnel par l'utilisateur.
- 2026-08-16 (correctif connexe) : `dashboards/dashboard_aidant.yaml` contenait l'URL de l'iframe **écrite en dur** (`http://10.32.154.241:8123/...`) — le dashboard Aidant restait vide dès qu'on accédait à HA en HTTPS (contenu mixte bloqué par le navigateur). Passé en URL relative `/local/launch.html`, qui suit automatiquement l'origine utilisée.
- 2026-08-18 (**plage horaire + urgence**) : idée du 16/08 construite — `input_datetime.m33_horaire_debut`/`_fin` + `input_boolean.m33_appel_urgent`, réglage initialement dans `config.html` (onglet Aidants), contrôle dans `launchVisio()` (aidant.html, bloque AVANT l'envoi) et contrôle redondant dans `refreshMain()`/`surveillerAppel()` (kiosk.html, ne répond jamais hors plage sans le drapeau urgent). Voir section dédiée plus haut. **Correctif connexe repéré en cours de route** : `m33_visio.yaml` déclarait deux blocs `input_text:` distincts dans le même fichier (clé de mapping dupliquée) — en YAML le second écrase silencieusement le premier au lieu de fusionner. Fusionnés en un seul bloc. Poussé (MD5 vérifié) ; **redémarrage HA requis** pour créer les 3 nouvelles entités (input_datetime × 2, input_boolean × 1) ; heures à régler une première fois (sinon plage 00:00–00:00, tout appel non urgent bloqué).
- 2026-08-18 (suite, **renommage « Vidésio »**) : quelques heures plus tard le même jour, demande utilisateur — regrouper les horaires visio avec les horaires TV et renommer l'ensemble « Vidésio ». Réglage déplacé de l'onglet Aidants vers l'onglet Confort → section « 📺 Vidésio — Sessions TV & Visio » (`#only-tv-block` de `config.html`, aussi accessible via la page dédiée `video.html` renommée « Vidésio »). Détail complet dans `M34_television.md`.
- 2026-08-18 (suite, **défaut 09:00-17:00**) : demande utilisateur — plutôt que de laisser la plage vide (00:00–00:00) jusqu'à un réglage manuel, ajout de `automation.m33_seed_horaires_defaut` + `input_boolean.m33_horaires_initialises`, calqués sur le seed des horaires TV de M34 : applique 09:00/17:00 une seule fois au premier démarrage HA suivant la création des entités, ne touche plus jamais rien ensuite. Poussé (MD5 vérifié) ; **redémarrage HA requis** pour créer les entités et déclencher le seed.
- 2026-08-18 (suite, **retour visuel bouton Appeler**) : demande utilisateur — même logique que le bouton d'envoi des messages, le bouton « Appeler » change de couleur hors plage horaire (ambre/marron, `.btn-visio.hors-plage`) et devient « 🚨 APPEL VISIO » en majuscules/gras/rouge (`.btn-visio.urgent-actif`) sur fond **redevenu vert** quand la case Urgence est cochée. `majEtatBoutonAppel()` (déjà pollée toutes les 4 s pour l'état « occupé par un autre aidant ») étendue pour calculer aussi plage + urgence ; rafraîchie immédiatement au clic sur la case (`onchange`) sans attendre le prochain cycle. Poussé (MD5 vérifié).
- 2026-08-18 (suite, **texte « Appel désactivé (…) »**) : demande utilisateur — le bouton hors plage doit reprendre EXACTEMENT le même principe que le bouton messages (« Envoi désactivé (08:00–19:00) ») : afficher les heures réellement configurées, pas juste une couleur. `visioDansPlage()` éclatée en `visioHoraire()` (renvoie les heures en texte + un drapeau erreur réseau) + `visioDansPlage()` (garde le même comportement booléen fail-open qu'avant, inchangé pour `launchVisio()`). Texte hors plage : « ⏰ Appel désactivé (09:00–17:00) ». Poussé (MD5 vérifié).
- 2026-08-18 (suite, **« Appeler » → « Appel Visio »**) : demande utilisateur — le libellé par défaut du bouton (dans la plage, case Urgence décochée) passe de « 📹 Appeler » à « 📹 Appel Visio ». Renommé dans le HTML, dans `majEtatBoutonAppel()` et dans les commentaires associés. Les autres états du bouton (occupé, hors plage, urgence) contenaient déjà « Appel » et n'ont pas changé.
- 2026-08-18 (suite, **REFONTE — case Urgence retirée**) : retour utilisateur direct (« c'est quoi cette crotte ? ça sert à quoi ? c'est moi qui ai demandé ? ») — la case cochée en permanence n'avait jamais été demandée, c'était un choix d'implémentation pour la dérogation « urgence » (elle, bien demandée le 16/08). Reconnu comme un mauvais choix d'UX (case visible en permanence, y compris en pleine journée où elle ne sert jamais) et retiré : HTML (`#visio-urgence-row`), CSS (`.btn-visio.urgent-actif`), logique JS (`urgenceCb` dans `launchVisio()`/`majEtatBoutonAppel()`/`raccrocherVisio()`) tous supprimés. Remplacé par une demande explicite du user d'utiliser le pavé rouge de confirmation déjà existant dans l'app (`askConfirm()`) : hors plage, le clic sur le bouton ouvre directement la question « appel urgent ? », sans rien à cocher à l'avance. `input_boolean.m33_appel_urgent` reste, mais devient un état transitoire décidé au clic (pas une préférence persistante). Le garde-fou côté kiosk (`visioDoitRepondre()`) est inchangé — il lit toujours le même booléen. Poussé (MD5 vérifié).
- 2026-08-18 (suite, **« Appel Visio » dans TOUS les états**) : demande utilisateur (répétée) — « Appel » seul ne suffisait pas dans les états occupé/hors-plage/toasts, remplacé par « Appel Visio » partout : bouton occupé « 📞 Appel Visio en cours avec X », hors plage « ⏰ Appel Visio désactivé (…) », et les toasts associés (« 📞 Appel Visio déjà en cours », « 📞 Appel Visio déjà en cours avec X », « 📴 Appel Visio terminé »). L'état urgence (« 🚨 APPEL VISIO ») l'avait déjà. Poussé (MD5 vérifié).
- 2026-08-18 (suite, **par analogie, bouton messages**) : demande utilisateur — même traitement que le bouton visio sur le bouton d'envoi des messages (`updateSendButton()`, `sendMessage()`) : « ⏰ Envoi désactivé (…) » → « ⏰ Envoi de message désactivé (…) », et « Envoi… » (pendant l'appel réseau) → « Envoi de message… ». Les autres états contenaient déjà « message » (« Envoyer le message », « Saisir un message… », « File pleine — max X messages »). Poussé (MD5 vérifié).
