# DÉPENDANCES GLOBALES — Système Assistant au Personne
*Dernière mise à jour : 2026-09-13 (soirée — **M32 Musique phase 1 + réparation complète des RDV/récurrences**) — Session dense, deux volets. **(A) M32 « Musique » phase 1 construite** : `packages/confo_m32_musique/m32_musique.yaml` (4 créneaux musique on/off + heures début/fin), `shell_scripts/m32_musique_liens.py` (liste de liens YouTube partagée, numérotée 01-99, stockée dans `www/musique_liens.txt`), `www/musique.html` (créneaux TV en haut en lecture, 4 créneaux musique, ajout/suppression de liens par numéro), bouton 🎵 branché dans `aidant.html`. Règles de priorité gravées : **créneau TV activé = créneau musique bloqué** (et auto-désactivation avec message si une modification d'horaire crée un conflit), créneau TV désactivé ne bloque rien, limite exacte (début musique = fin TV) autorisée. Priorité d'affichage kiosk : **Visio > TV > Musique > Photos**. Phase 2 (lecture sur le kiosk + coupure musique si session TV activée) à construire. Également ce jour : **Meet définitivement retiré** (entité `m33_visio_url` supprimée du package, iframe et validation retirées de `kiosk.html`) — la visio du projet = WebRTC maison uniquement ; ordre des boutons aidant fixé à 📺 Vidésio > 🎵 Musique > 📷 Photos > 💬 Message > 📅 Calendrier ; finitions des 4 pages dédiées (boutons retour identiques 36×36 arrondis, petits textes rgb(180,180,180), espacements 10px, compteur de caractères NOTE) ; kiosk/interface : bandeaux renommés (« 📹 Écran Visioconférence », « 📺 Écran Télévision (désactivée) »). **(B) Soirée — trois bugs RDV/récurrences trouvés et corrigés** (déclencheur : question utilisateur « les messages récurrents du calendrier tu les gères comment », puis constat « à chaque création il m'en crée un nouveau ») : (1) **l'automation `m03_rdv_recurrents_creer_l_evenement_du_jour` plantait à chaque exécution depuis sa mise en place** — `TypeError: can only concatenate str (not "datetime.timedelta") to str` (`start_dt + timedelta` sur une variable template restée chaîne) — donc **aucune occurrence de RDV récurrent n'était créée automatiquement** ; calcul refait en une seule expression, dans les 2 blocs (jour + lendemain). (2) **La suppression d'un RDV ne fonctionnait pas du tout** : `aidant.html` appelait le service REST `calendar/delete_event` **qui n'existe pas** (HA n'expose que `create_event`/`get_events` en REST ; suppression WebSocket-only) → HTTP 400 à chaque clic ; remplacé par la commande WebSocket `calendar/event/delete` (nouvelle fonction `haDeleteEventWebSocket`). (3) **Empilement de doublons** : créer/recréer une récurrence ajoutait des RDV sans vérifier l'existant → **anti-doublon aux 3 endroits** (formulaire `creerRdv()` via `calendar.get_events`, script `m03_rdv_recurrents.py::do_add` qui refuse une règle identique, automation via `get_events` + condition sur les 2 blocs — template `selectattr/map/replace/search`, HA refusant `append()` en Jinja sandboxé). Comportement voulu par l'utilisateur : **supprimer une récurrence supprime aussi les RDV À VENIR** correspondants (même intitulé + même heure) — la modale de confirmation le dit désormais. Message du bouton 🗑️ d'un RDV corrigé au passage (« cet événement uniquement », il annonçait à tort « toute la série »). Horodatage du message : **retiré du kiosk** (bandeau propre) et **réaffiché uniquement côté aidant** (bandeau live + « EN COURS D'AFFICHAGE »). Docs régénérées et poussées (`ENTITES.md`, `DEPENDANCES_TECHNIQUE.md`, `MOC_DEPENDANCES.md` — 207 entités définies, 271 sur l'instance live, 11 orphelines réelles, 10 fantômes dont `sensor.m34_etat_global`, cas connu de renommage en `sensor.confo_m34_etat_global`). Détail des correctifs dans les fiches M03. Session précédente : 2026-08-18 (**suite, REFONTE — case Urgence visio retirée**) — Retour utilisateur direct : « c'est quoi cette crotte ? ça sert à quoi ? c'est moi qui ai demandé ? » à propos de la case « 🚨 Urgence » cochée en permanence. Confirmé : la plage horaire + la dérogation urgence, oui, demandées le 16/08 — la case pour l'obtenir, non, c'était un choix d'implémentation de l'assistant, jamais demandé, et redondant avec l'affichage déjà présent sur le bouton. Retirée entièrement (HTML `#visio-urgence-row`, CSS `.btn-visio.urgent-actif`, logique JS). Remplacée par une confirmation À LA DEMANDE : hors plage horaire, cliquer sur « Appel Visio » ouvre directement le pavé rouge de confirmation déjà existant dans l'app (`askConfirm()`, même modal que pour confirmer une suppression) — « Hors plage horaire (09:00–17:00). Confirmer un appel urgent ? ». Dans la plage normale, rien de tout ça n'apparaît. `input_boolean.m33_appel_urgent` reste en usage interne (réglé au moment du clic, plus une préférence persistante) ; le garde-fou côté kiosk (`visioDoitRepondre()`) est inchangé. Poussé (MD5 vérifié). Détail complet dans `M33_visio.md`. Session précédente du même jour (**suite, retour visuel bouton Appeler**) — Demande utilisateur : le bouton « Appeler » (`aidant.html`) reflète maintenant en direct la plage horaire visio ET la case Urgence, même logique que le bouton d'envoi des messages. Ambre/marron (`.btn-visio.hors-plage`) hors plage ; vert + texte « 🚨 APPEL VISIO » majuscules/gras/rouge (`.btn-visio.urgent-actif`) quand Urgence est cochée. `majEtatBoutonAppel()` étendue (déjà pollée 4 s pour l'état « occupé »), rafraîchie aussi immédiatement au clic sur la case. Poussé (MD5 vérifié). Session précédente du même jour (**suite, défaut 09:00-17:00 visio**) — Demande utilisateur : plutôt que de laisser la plage horaire visio (M33) vide (00:00–00:00) jusqu'à un réglage manuel, ajout d'un seed automatique — `automation.m33_seed_horaires_defaut` + `input_boolean.m33_horaires_initialises` — calqué sur le mécanisme déjà en place pour les horaires TV par défaut de M34 (`m34_seed_horaires_defaut`) : applique 09:00/17:00 une seule fois, au tout premier démarrage HA suivant la création des entités, puis ne touche plus jamais rien (contrairement à `initial:`, qui écraserait un réglage manuel ultérieur à CHAQUE redémarrage). Poussé (MD5 vérifié) ; **redémarrage HA requis** (crée les entités ET déclenche le seed). Détail dans `M33_visio.md`. Session précédente du même jour (**suite, renommage « 📺 Vidésio »**) — Demande utilisateur : la page dédiée/section « 📺 Vidéo » (Sessions TV, M34) devient « 📺 Vidésio — Sessions TV & Visio », et la plage horaire des appels visio (M33, construite plus tôt le même jour dans l'onglet Aidants) est **déplacée** dans cette section, regroupée avec les horaires TV — un seul écran (`video.html`, `config.html?only=tv`) couvre désormais les deux. Libellés renommés partout où « 📺 Vidéo » apparaissait : bouton `aidant.html`, titre + message d'accès refusé `video.html` (corrigé au passage : pointait vers un onglet « Sécurité → Droits d'accès » qui n'existe plus depuis le renommage du 16/08, remplacé par le bon chemin « Aidants »), texte des droits d'accès `config.html`. **Aucun changement d'identifiant technique** : `DROIT_BIT.video` (bit 8) et `input_datetime.m33_horaire_debut`/`_fin` restent inchangés — seul l'affichage change. 3 fichiers poussés (MD5 vérifié) ; docs mises à jour (`M34_television.md`, `M33_visio.md`). Session précédente du même jour (**suite, suppression `input_text.m34_browser_id_tv`**) — Retour utilisateur (« ça sert oui ou non ? ») après vérification de code : plus utilisé nulle part depuis la bascule du 14/08 vers kiosk.html en HTML pur (ni pour la TV — `script.m34_lancer_session` ne l'a jamais consulté depuis cette date — ni pour la visio M33, malgré ce qu'affirmait encore `M34_television.md` à tort). Son seul usage réel restant était `script.m31_lancer_diaporama` (`browser_mod.navigate` pour forcer le retour du navigateur TV sur le dashboard kiosk) — devenu inutile puisque `kiosk.html` gère déjà ce retour tout seul par sondage d'état. Supprimés : le champ (`m34_television.yaml`), sa section UI « ⚙️ Réglages avancés TV » dans `config.html` (n'avait plus que ce seul champ), le seed du démarrage HA. Vidé (`sequence: []`, pas supprimé) : `script.m31_lancer_diaporama`, gardé en coquille car encore appelé par 2 automations de `m34_television.yaml` (retrait de ces 2 appels non fait — hors périmètre). Conséquence directe : `browser_mod` n'a plus AUCUN usage actif dans le projet. Docs mises à jour : `M34_television.md`, `M31_photos.md`. Session précédente du même jour (**+ plage horaire/urgence visio M33**) — Idée émise le 16/08 (« ne pas réveiller la personne en pleine nuit »), construite aujourd'hui : nouvelles entités `input_datetime.m33_horaire_debut`/`_fin` + `input_boolean.m33_appel_urgent` (`m33_visio.yaml`), réglage dans `config.html` (nouvel onglet Aidants → section 🕐), double contrôle : `aidant.html` (`visioDansPlage()` dans `launchVisio()`, bloque AVANT l'envoi, fail-open si erreur réseau/entités absentes) et `kiosk.html` (`visioDoitRepondre()` dans `refreshMain()` + `surveillerAppel()`, garde-fou redondant, fail-closed — ne répond jamais hors plage sans le drapeau urgent, quel que soit ce qui a déclenché l'appel). Case « 🚨 Urgence » ajoutée au-dessus du bouton Appeler, décochée automatiquement à chaque raccrochage. **Correctif connexe repéré en cours de route** : `m33_visio.yaml` déclarait deux blocs `input_text:` séparés dans le même fichier — clé de mapping dupliquée, le second écrasait silencieusement le premier en YAML (pas de fusion). Fusionnés en un seul bloc. **Checklist corrigée au passage** : Santé_M20 Médicaments était resté décoché malgré son build du 16/08 (M13_medoc.md) — dette documentaire de cette session-là, corrigée ici. Déployé (4 fichiers, MD5 vérifié) ; **redémarrage HA requis** pour créer les 3 nouvelles entités ; heures à régler une première fois dans Configuration → Aidants (sinon plage 00:00–00:00, tout appel non urgent bloqué). Détail complet dans `M33_visio.md`. Session précédente : 2026-08-16 (**+ module M13 Rappel médicaments + ménage config**) — (1) NOUVEAU module M13 « Rappel médicaments » (`m20_medoc.yaml`) : 4 moments (matin/midi/soir/coucher), chacun avec heure réglable + activation indépendante + durée d'affichage commune. **Rappel pur** (aucune détection de prise, pas d'acquittement, pas d'alerte — « ça s'arrête à une notif »), calculé 100 % côté kiosk (pas d'automation), bandeau overlay `#medoc-banner`. Config dans l'onglet Sécurité (`buildMedoc`). Off par défaut. ⚠️ Piège surdosage : à réserver aux profils sans risque de reprise, s'appuyer sur un pilulier. Fiche `M13_medoc.md`. (2) Module M14 Repas **abandonné** (signal non fiable). (3) `config.html` : onglet Sécurité **coupé en deux** — la partie Aidants (SOS proximité + droits d'accès) est passée dans un nouvel onglet « 👥 Aidants » en fin de barre avant Outils ; section Visio Google Meet retirée (obsolète depuis la visio maison) ; Sessions TV / Réglages avancés masqués de Confort (restent pour la page Vidéo dédiée). Session précédente du même jour (S3 — **un seul appel visio à la fois**) : trou trouvé sur question de l'utilisateur, pas en test — un 2e aidant appelant pendant un appel restait bloqué indéfiniment sans message, et sa purge des boîtes de signalisation pouvait **détruire** un 1er appel encore en cours d'établissement. Corrigé : nouvelle entité `input_text.m33_appel_par` (nom de l'aidant en ligne), refus explicite « Appel en cours avec X », purge déplacée APRÈS la vérification, bouton grisé et réellement désactivé (sondage dédié 4 s), libération du nom au raccrochage manuel comme automatique. ⚠️ Redémarrage HA requis pour créer `m33_appel_par`. Session précédente du même jour (**✅ VISIO MAISON CONSTRUITE ET FONCTIONNELLE**) — visioconférence WebRTC pair-à-pair, sans aucun service externe : l'aidant appuie sur « Appeler », l'écran de la personne aidée bascule **tout seul** sur l'appel, **sans aucun clic de sa part** (objectif de base, impossible avec Meet ou Jitsi). L'image et le son passent en direct d'un appareil à l'autre ; HA ne sert qu'à l'établissement. Nouveaux éléments : `input_boolean.m33_appel_en_cours` + `shell_command.m33_visio_signal_{envoyer,lire,purger}` + `shell_scripts/m33_visio_signal.py` (signalisation base64, lecture destructrice — via shell_command et NON via les événements WebSocket, réservés aux admins alors que les aidants sont volontairement non-admin, cf. M10). `aidant.html` et `kiosk.html` réécrits de part et d'autre. **HTTPS — le blocage de la journée — résolu par Tailscale** (`share_homeassistant: serve`) : certificat valide, aucun port ouvert, accès distant inclus ; a nécessité les proxies de confiance `127.0.0.1`/`::1` écrits directement dans `.storage/http`, l'interface les refusant silencieusement. **Fiabilisation** (cas signalé en conditions réelles : l'aidant ferme son application sans raccrocher → image figée devant la personne aidée) : `pagehide`+`keepalive` côté aidant et **détection de flux mort** (`bytesReceived`, 6 s) côté kiosk — les états WebRTC natifs mettant ~30 s à basculer, trop long. Correctif connexe : `dashboard_aidant.yaml` avait l'URL de son iframe **écrite en dur** en `http://<ip>` → dashboard vide en HTTPS (contenu mixte), passé en URL relative. Détail complet dans `M33_visio.md`. Session précédente du même jour (**découverte majeure HTTPS + chantier visio bloqué**) — (1) PIÈGE HA : depuis la migration HTTP (`.storage/http` → `yaml_migration_done: true`), un bloc `http:` dans `configuration.yaml` est **purement IGNORÉ**, sans erreur ni message. Toute la doc et les forums parlent encore de cette méthode, devenue silencieusement inopérante — l'utilisateur cherchait depuis 2 ans comment passer sa prod en HTTPS. La config SSL se fait désormais dans **Paramètres → Système → Réseau**. Certificat auto-signé généré (`/ssl/fullchain.pem` + `/ssl/privkey.pem`, openssl, 10 ans, IP en SAN), HTTPS actif sur l'instance. ⚠️ Mais l'app Companion **refuse les certificats auto-signés** → piste Tailscale engagée (certificat valide, aucun port ouvert), nom obtenu `homeassistant-1.tail0c740d.ts.net`, **non finalisée**. (2) VISIO : exploration complète pour remplacer Google Meet (qui impose un clic « Rejoindre » à la personne aidée, rédhibitoire) — Jitsi public (authentification impossible en iframe), intégration `visio_jitsi` (browser_mod trop fragile, IDs périmés), auto-hébergement (incompatible « simple pour tous »), WebRTC maison (concept VALIDÉ : HA sert de serveur de signalisation, SDP 4 Ko testé en direct ; STUN public OK, candidat `srflx`). **Bloqué sur l'obligation HTTPS pour la caméra** — non contournable par du code, vaut pour toute solution. Prototype `www/visio_test.html` créé, test final non réalisé. **Meet reste en place.** Détail complet dans `M33_visio.md`. (3) Correctifs Meet : URL sans `https://` traitée comme chemin relatif, et `window.open()` après `await` bloqué silencieusement — les deux corrigés et confirmés. Session précédente (2026-08-15, **correctif critique `configuration.yaml`** — le panneau `panel_custom` "Outils Dev" (`developer-tools/yaml`) n'avait pas `require_admin: true`, visible et utilisable par TOUT compte connecté, admin ou non : un aidant pouvait l'utiliser pour appeler `input_text.set_value` sur `input_text.m10_droits_aidants` directement, contournant tout le système de droits construit ce même jour. Trouvé en vérifiant en direct via la commande WebSocket `get_panels`, suite à une remarque de l'utilisateur. Corrigé (`require_admin: true` ajouté), `check_config` validé, déployé (MD5-matched) — nécessite un redémarrage HA complet pour prendre effet. `configuration.yaml` local resynchronisé sur l'état live à cette occasion (avait dérivé : entrée dashboard obsolète + ressource en trop, probablement dues à des éditions directes via l'add-on OpenCode). Détail complet dans `M10_gestion_aidants.md`. Session précédente (même jour, suite, **DÉFINITIF** — les 2 PIN construits en session précédente sont supprimés et remplacés par un système de droits par aidant appliqué automatiquement selon l'identité réelle de connexion : bitmask `input_text.m10_droits_aidants` étendu de 2 à 6 droits (config/messages/calendrier/video/photos + nouveau droit 🚨 alertes, demandé explicitement par l'utilisateur, indépendant du SOS existant). Client WebSocket `auth/current_user` (token → user HA → `person.*` via `attributes.user_id` → droits JSON) construit et intégré dans les 4 pages concernées (`config.html`, `calendrier.html`, `video.html`, `photos.html`), chacune vérifiant son propre droit au chargement et affichant un écran "Accès refusé" explicite sinon. Déployé et vérifié en direct (MD5-matched sur les 4 fichiers + contenu confirmé via curl sur l'instance live). ⚠️ Non testable de bout en bout : seuls 2 aidants sur 7 ont un vrai compte HA (`person.eric`, `person.aidant_1_admin_ok`) — les 5 autres doivent être équipés (Paramètres → Personnes → Autoriser la connexion) avant de pouvoir vérifier leurs droits individualisés. Détail complet dans `M10_gestion_aidants.md`. Session précédente (même jour, plus tôt, 2ᵉ audit sécurité — deux corrections déployées : (1) `input_text.m33_visio_url` était injecté sans validation dans un iframe caméra/micro (`kiosk.html`) — liste blanche `meet.google.com` ajoutée dans `kiosk.html` et `aidant.html` ; (2) `config.html` n'avait aucune vérification de rôle (accès direct par URL possible pour tout compte HA) — `escHtml()` ajouté sur le seul point XSS réellement exploitable (`person.friendly_name` dans `buildDroits()`), et un 2ᵉ PIN distinct (`input_text.m10_pin_config`) protège désormais `config.html` lui-même, actif même par URL directe (contrairement au bouton 🔧 simplement masqué dans `aidant.html`). Piste alternative de l'audit (restreindre côté permissions HA) vérifiée et écartée — non réalisable sans composant tiers. ⚠️ Nouvelle entité `m10_pin_config` : redémarrage HA requis, puis réglage manuel de la première valeur via Outils de développement (bootstrap circulaire). Session précédente (même jour, plus tôt) : upload photo utilisable par n'importe quel compte non-admin, résolu proprement. Rappel de la cause : `POST /api/media_source/local_source/upload` (route officielle HA) est réservée aux comptes **administrateur** (`local_source.py` : `is_admin` check), indépendamment du token — confirmé en direct (galerie/suppression, via `shell_command`, fonctionnaient déjà sur un compte non-admin ; seul l'upload échouait). Solution provisoire (passer le compte admin) jugée disproportionnée par l'utilisateur — à raison, ne passe pas à l'échelle pour d'autres comptes. **Contournement construit** : `shell_command.m31_photos_televerser_{debut,chunk,fin}` + `shell_scripts/m31_photos_televerser.py`, upload par morceaux base64 écrits directement sur disque (même logique que la suppression), sans jamais passer par la route admin-only. Taille de morceau ajustée après un retour "HTTP 500" en conditions réelles : 300 000 caractères/appel trop gros pour le serveur (mesuré en direct : 100 000 = OK, 150 000 = échec) → ramené à 50 000. **Confirmé fonctionnel en direct par l'utilisateur**, y compris depuis un compte non-admin sur le téléphone (app Companion Android) — plus lent que l'ancienne méthode (dizaines d'appels séquentiels), accepté comme compromis. Session précédente (même jour, plus tôt) : hypothèse iframe-overlay pour un 401 de navigation infirmée ; vraie cause (admin-only) trouvée par élimination + confirmée dans le code source HA ; suppression photo confirmée fonctionnelle après correctif d'un bug `onclick`/`JSON.stringify` ; upload déplacé de `config.html` vers `photos.html` ; bloc "Prendre un rendez-vous" retiré de l'écran principal d'aidant.html. Session d'avant (même jour) : bug `?return_response=true`→`?return_response` corrigé ; 3 pages dédiées créées ; Confo_M31 Photos rotation construite ; Confo_M33 Visio unifié. Session du 14/08 : fiabilisation Confo_M34 Télévision + clôture oblig_M03 Écran Messages)*

---

## ✅ CHECKLIST — MODULES TORCHÉS (implémentation réelle existante)

> Coché = du code/fichier existe et tourne (même en simulation, même avec un bug connu). Pas coché = **zéro fichier**, juste le toggle `input_boolean.module_*` qui existe et ne fait rien. Un module coché n'est pas forcément fini/sans bug — voir son statut détaillé plus bas pour les réserves.

- [x] oblig_M01 Temp & Hygro
- [x] oblig_M02 Détection Inactivité
- [x] oblig_M03 Écran Messages
- [x] Secur_M10 SOS
- [x] Secur_M11 Capteur Lit
- [ ] Secur_M12 Caméra IA
- [x] Secur_M13 Porte Ext
- [ ] Secur_M14 Fenêtres
- [ ] Secur_M15 Frigo
- [ ] Secur_M16 Congel
- [ ] Secur_M17 Veilleuse Nuit
- [x] Santé_M20 Médicaments *(rappel pur construit 16/08 — corrigé ici le 18/08, checklist non mise à jour au moment du build — voir M13_medoc.md)*
- [ ] Santé_M21 Repas *(abandonné 16/08 — signal non fiable, voir CDC §8, ne sera jamais coché)*
- [ ] Santé_M22 Douche
- [x] Confo_M30 Kiosk Écran *(dashboard seul, pas de logique séparée — complet par nature)*
- [x] Confo_M31 Photos Famille
- [x] Confo_M32 Musique *(phase 1 construite 13/09 — créneaux + liens ; lecture kiosk (phase 2) à faire, voir M32_musique.md)*
- [x] Confo_M33 Visio
- [x] Confo_M34 Télévision
- [ ] Envir_M40 Chauffage

**12/20 torchés, 8/20 jamais commencés** *(dont 1 abandonné volontairement — M21 Repas — qui ne sera jamais coché). M00 non compté — socle, pas un module, voir table de correspondance ci-dessous.*

---

> **RÈGLE ANTI-OUBLI :** À chaque modification d'un YAML dans `raspi/`, cette page DOIT être mise à jour dans la même session. Un YAML pushé en prod sans mise à jour ici = dette documentaire.

> **⚠️ RESTRUCTURATION 2026-08-13 :** la numérotation à plat (M01-M20) est remplacée
> par une numérotation par groupe (façon ReBuild) : `oblig_M01-03`, `Secur_M10-17`,
> `Santé_M20-22`, `Confo_M30-34`, `Envir_M40`. **Les `entity_id` réels (`input_boolean.module_*`)
> ne changent PAS** — seule l'étiquette/le numéro de référence change. Voir table
> de correspondance ancien/nouveau ci-dessous.

---

## 📐 SOURCES DE VÉRITÉ

| Priorité | Source | Rôle |
|:---------|:-------|:-----|
| **1** | **Instance HA live** (10.32.154.241) | Ce qui tourne en prod = référence absolue |
| **2** | **`raspi/` local** | Fichiers de travail → déployés vers `Z:\` |
| **3** | **`docs/DEPENDANCES_GLOBALES.md`** (ce fichier) | Référence technique état d'avancement |
| **4** | **`docs/05_projet/CAHIER_DES_CHARGES.md`** | Référence fonctionnelle (quoi faire) |

---

## 🔢 TABLE DE CORRESPONDANCE — ANCIEN ↔ NOUVEAU NUMÉRO

| Nouveau ID | Ancien | Entity_id (`input_boolean.*`, inchangé) | Nom |
|:-----------|:-------|:------------------------------------------|:----|
| M00 *(socle, hors périmètre — pas un module)* | M00 | *(aucun — pas de toggle propre)* | Registre des 20 toggles (`m00_modules.yaml`) + capteurs de simulation temporaires (`m00_simulation.yaml`, `m00_simulation_sensors.yaml`) |
| oblig_M01_Temp_Hygro | M01 | `module_temp_hygro` | Température & Hygrométrie |
| oblig_M02_Detect_Inactivite | M02 | `module_inactivite` | Détection Inactivité |
| oblig_M03_Ecran_Messages | M03 | `module_ecran_msg` | Écran Messages |
| Secur_M10_SOS | M04 | `module_sos` | Bouton SOS |
| Secur_M11_Capteur_Lit | M05 | `module_capteur_lit` | Capteur Lit |
| Secur_M12_Camera_IA | M06 | `module_cam_ia` | Caméra IA |
| Secur_M13_Porte_Ext (S) | M15 | `module_porte_ext` | Porte Extérieure — multi-capteurs |
| Secur_M14_Fenetre (S) | M18 | `module_fenetre` | Fenêtres — multi-capteurs |
| Secur_M15_Frigo | — nouveau | *(à créer)* | Porte Frigo |
| Secur_M16_Congel | — nouveau | *(à créer)* | Porte Congélateur |
| Secur_M17_Veilleuse_Nuit | M16 (registre) | `module_lumiere_nuit` | Veilleuse Nuit |
| Santé_M20_Médicaments | M13 | `module_medoc` | Médicaments |
| Santé_M21_Repas | M14 | `module_repas` | Repas |
| Santé_M22_Douche | M12 | `module_douche` | Douche |
| Confo_M30_Kiosk_Ecran | M07 | `module_kiosk_ecran` | Kiosk Écran |
| Confo_M31_Photos_Famille | M08 | `module_kiosk_foto` | Photos Famille |
| Confo_M32_Musique | M09 | `module_kiosk_zic` | Musique |
| Confo_M33_Visio | M10 | `module_visio` | Visioconférence |
| Confo_M34_Television | M11 | `module_television` | Télévision |
| Envir_M40_Chauffage | M17 | `module_chauffage` | Chauffage (stand-by) |

**Exclus du registre** (orphelins, aucune automation ne les consomme, retrait géré séparément par l'utilisateur) : ancien M19 (`module_dashboard_fam`), ancien M20 (`module_msg_famille`).

**(S)** = module à capteurs multiples : la logique doit agréger plusieurs entités du même type, pas un `is_state()` unique sur un seul capteur.

---

## 🔗 CHAÎNE DE DÉPENDANCES PAR MODULE

---

## OBLIGATOIRES

### oblig_M01_Temp_Hygro *(ancien M01)*

| MATÉRIEL | CAPTEUR BRUT (source) | ENTITÉ PRODUITE | AVAL |
|:---------|:----------------------|:-----------------|:-----|
| SONOFF SNZB-02D (Z2M) | `sensor.snzb02d_salon_temperature` | `sensor.m01_temp_salon_min_24h` | `aidant.html` |
| SONOFF SNZB-02D (Z2M) | `sensor.snzb02d_salon_temperature` | `sensor.m01_temp_salon_max_24h` | `aidant.html` |
| SONOFF SNZB-02D (Z2M) | `sensor.snzb02d_salon_humidity` | `sensor.m01_hygro_salon_avg_24h` | `aidant.html` |
| SONOFF SNZB-02D (Z2M) | `sensor.snzb02d_chambre_temperature` | `sensor.m01_temp_chambre_min_24h` | `aidant.html` |
| SONOFF SNZB-02D (Z2M) | `sensor.snzb02d_chambre_temperature` | `sensor.m01_temp_chambre_max_24h` | `aidant.html` |
| [calculé] | `sensor.m01_temp_salon_min/max_24h` | `sensor.m01_alerte_temperature` | `aidant.html` (chips) |
| [calculé] | `sensor.snzb02d_salon_humidity` | `sensor.m01_alerte_humidite` | `aidant.html` |
| [calculé] | `sensor.m01_temp_salon_min/max_24h` | `sensor.m01_resume_temp_salon` | `aidant.html` |
| [calculé] | `sensor.m01_temp_chambre_min/max_24h` | `sensor.m01_resume_temp_chambre` | `aidant.html` |

**⚠️ 2026-08-13 :** `aidant.html` bascule sur `input_number.sim_temp_salon/chambre` en fallback si les capteurs Zigbee sont absents (non pairés) — ajouté cette session.
**⚠️ Simulation active :** `sensor.snzb02d_salon/chambre_temperature` (et `_humidity`) sont actuellement des **template sensors simulés** dans `raspi/packages/m00_simulation_sensors.yaml`, qui portent volontairement les `entity_id` des futurs capteurs réels. Rien à changer au pairage — mais tant que les SNZB-02D ne sont pas pairés, ces valeurs sont fictives.
**Fichiers sources :** `raspi/packages/m01_temp_hygro.yaml`, `raspi/packages/m00_simulation_sensors.yaml` (source des valeurs simulées)
**Statut :** ✅ Déployé — dépend du pairage réel des SNZB-02D

---

### oblig_M02_Detect_Inactivite *(ancien M02)*

| MATÉRIEL | CAPTEUR BRUT | ENTITÉ PRODUITE | AVAL |
|:---------|:-------------|:------------------|:-----|
| Contacts portes/fenêtres, PIR simulés, mmWave simulés | `input_boolean.sim_*` | `binary_sensor.m02_activite_detectee` | automations M02 |
| Secur_M11 (Capteur Lit) | `binary_sensor.m05_lit_occupe` | distingue sieste normale / absence anormale | logique M02 |
| [calculé, apprentissage EMA] | gap max observé par tranche horaire | `input_number.m02_seuil_*` (5 tranches) | alertes M02 |

**Fichier source :** `raspi/packages/m02_inactivite.yaml` (v2, réécrit 2026-08-12 — multi-capteurs + apprentissage adaptatif)
**Statut :** ✅ Développé (12/08) — **⚠️ non testé en conditions réelles**, testable via `dashboard_test_simulation.yaml`

---

### oblig_M03_Ecran_Messages *(ancien M03 — clôturé le 14/08)*

> Fiche condensée — voir [`M03_ecran_msg.md`](03_modules_packages/03_communication/M03_ecran_msg.md)
> pour la chaîne de dépendances complète et le guide de dépannage détaillé.

| SOURCE | ENTITÉ | RÔLE | AVAL |
|:-------|:-------|:-----|:-----|
| Saisie famille (`aidant.html`) | `input_text.m03_message_famille` | Zone de saisie | script.m03_envoyer |
| Saisie famille (`aidant.html`) | `input_text.m03_message_auteur` | Auteur (`hass.user.name`, défaut "La famille") | log + queue |
| Auto (script) | `input_text.m03_affiche_msg` / `_affiche_auteur` | Message actuellement affiché | sensor.m03_texto_formate |
| Auto (script) | `input_datetime.m03_affiche_depuis` | Timestamp début d'affichage | sensor.m03_texto_formate (âge) |
| Interne | `input_text.m03_queue_msg` / `_queue_auteur` / `_queue_timestamps` | Files d'attente pipe-séparées | script.m03_afficher_suivant |
| Interne | `timer.m03_rotation` | Timer rotation (durée = `m03_affichage_duree`) | automation m03_rotation_timer_finished |
| Local Calendar (natif HA) | `calendar.calendrier_local` | Événements agenda | sensor.m03_agenda_formate |
| [calculé] | `sensor.m03_bandeau_principal` | Texte final (arbitrage agenda/texto) | `aidant.html` (bandeau live), `kiosk.html` (msg-box) |
| `aidant.html` (formulaire RDV, 14/08) | service `calendar.create_event` | Création directe d'événements (date+heure+note ≤60 car., durée 30 min) | `calendar.calendrier_local` |
| `aidant.html` (récurrence, 14/08) | `shell_command.m03_rdv_recurrents` + `m03_rdv_recurrents.yaml` | Règles jours+heure+note stockées dans `www/rdv_recurrents.txt` ; automation quotidienne (00:05) crée l'occurrence du jour — `calendar.create_event` ne supporte pas `rrule` (vérifié doc officielle HA 2026.8.2) | `calendar.calendrier_local` |

**✅ Corrections du 14/08 (clôture) :** file qui rotait en boucle infinie
(message affiché remis en fin de file) → corrigé, retrait définitif après
affichage. Ordre des vérifications du bouton Envoyer (restrictions
affichées avant la saisie, pas après). Nouveau bouton "Remettre les valeurs
par défaut" dans `aidant.html` (réimplémentation indépendante, lit
`config.json`). Boîte "Message en cours d'affichage" dédupliquée
(faisait triple emploi avec BANDEAU KIOSK + MESSAGES EN COURS).
`calendar.google_agenda_famille` (jamais créé, Google abandonné —
confidentialité) remplacé par `calendar.calendrier_local` (intégration
native Local Calendar) + formulaire de création de RDV ajouté dans
`aidant.html`.

**✅ `script.m03_reset_reglages` (`m03_reset_reglages.yaml`) supprimé le
14/08** — orphelin depuis le 13/08, valeurs codées en dur obsolètes
(`queue_max=8`, `envoi_debut=09:00` — vs `config.json` = `5`/`08:00`).
Supprimé local + `Z:\`, scripts rechargés côté HA — l'entité n'existe plus.

**Fichiers sources :** `raspi/packages/oblig_m03_ecran_msg/m03_ecran_msg.yaml`
**Statut :** ✅ Clos le 14/08

---

## SECUR (Sécurité)

### Secur_M10_SOS *(ancien M04)*

| SOURCE | ENTITÉ | RÔLE | AVAL |
|:-------|:-------|:-----|:-----|
| `input_boolean.sim_sos_bouton` (bouton WOOX réel non pairé) | — | déclenche l'alerte | automation m04_sos_appui |
| Auto | `input_boolean.m04_sos_declenche` | état SOS actif | script.m04_envoyer_alerte_sos |
| Saisie admin | `input_boolean.m04_prox_<id>` (par person.*) | Cases à cocher aidants de proximité | script.m04_envoyer_alerte_sos |
| Script | `script.m04_envoyer_alerte_sos` | Envoi | `notify.persistent_notification` (⚠️ pas de push réel) |

**⚠️ person.x fictifs :** les aidants sont des comptes de test. À remplacer par les vrais `entity_id` quand les aidants auront installé Companion app.
**⚠️ Notification actuelle = `persistent_notification`** (visible dans HA seulement) — **pas de push réel vers un téléphone**, TODO explicite dans le fichier source lui-même.
**Fichiers sources :** `raspi/packages/m04_sos.yaml`, `m04_gestion_aidants.yaml`, `m04_groupe_aidants.yaml`
**Statut :** 🧪 Simulation (bouton non pairé) + ⚠️ notification non opérationnelle en conditions réelles

**Ajout 15/08 (fichier `secur_m10_sos/m10_gestion_aidants.yaml`, distinct des fichiers ci-dessus malgré le nom similaire) :** `input_text.m10_pin_pages_dediees` — code PIN partagé protégeant les 3 nouvelles pages dédiées (`calendrier.html`/`video.html`/`photos.html`, boutons dans `aidant.html`). Éditable dans `config.html` → Sécurité. Voir fiche dédiée [`M10_gestion_aidants.md`](03_modules_packages/02_securite_alerte/M10_gestion_aidants.md) (réécrite le 15/08, remplace `M04_gestion_aidants.md` resté stale — contenait déjà `input_text.m10_droits_aidants`, absent du mirror docs jusqu'ici).

---

### Secur_M11_Capteur_Lit *(ancien M05)*

| MATÉRIEL | CAPTEUR BRUT | ENTITÉ PRODUITE | AVAL |
|:---------|:-------------|:-------------------|:-----|
| `input_boolean.sim_lit_occupe` (Aqara MCCGQ11LM réel non pairé) | — | `binary_sensor.m05_lit_occupe` | oblig_M02 (distingue sieste/absence) |
| [calculé] | `input_boolean.sim_lit_occupe` | `sensor.m05_lit_duree_occupation` | — |

**Fichier source :** `raspi/packages/m05_capteur_lit.yaml`
**Statut :** 🧪 Simulation — capteur réel non pairé

---

### Secur_M12_Camera_IA *(ancien M06)*
**Statut :** ⛔ Non implémenté — toggle `module_cam_ia` seul, aucun fichier

---

### Secur_M13_Porte_Ext (S) *(ancien M15)*

| MATÉRIEL | CAPTEUR BRUT | ENTITÉ PRODUITE | AVAL |
|:---------|:-------------|:-------------------|:-----|
| SONOFF SNZB-04P (Z2M) | `binary_sensor.snzb04p_porte_ext_contact` | `sensor.m15_porte_ext_duree_ouverture` | `aidant.html` (chip-porte) |
| Reolink E1 Pro (WiFi) | `camera.reolink_e1_pro` | (natif HA) | `aidant.html` (WebRTC/panneau alarme) |
| *(candidat, pas encore pairé)* | `contact_porte_entree` (voir `appairage.html`) | alimenterait `binary_sensor.contact_porte_entree_contact` | `aidant.html` (alarme + caméra, déjà câblé, en attente du capteur) |
| *(candidat, pas encore pairé)* | `contact_porte_2` (voir `appairage.html`) | — | — |

**⚠️ Logique inversée :** `state: off` = porte **ouverte**, `state: on` = porte **fermée**
**⚠️ Simulation active :** `binary_sensor.snzb04p_porte_ext_contact` est également simulé par `raspi/packages/m00_simulation_sensors.yaml` tant que le SNZB-04P n'est pas pairé.
**Fichiers sources :** `raspi/packages/m15_porte_ext.yaml`, `raspi/packages/m00_simulation_sensors.yaml`
**Statut :** ⚠️ 1 porte déployée sur plusieurs prévues — module **(S)**, la logique devra agréger plusieurs portes à terme

---

### Secur_M14_Fenetre (S) *(ancien M18)*

**Capteurs candidats (`appairage.html`, aucun pairé) :** `contact_fenetre_salon`, `_salon_2`, `_chambre`, `_chambre_2`, `_bureau`, `_cuisine`, `_sdb` (7 au total)
**Statut :** ⛔ Non implémenté — toggle `module_fenetre` seul, aucun fichier

---

### Secur_M15_Frigo *(nouveau, décidé 2026-08-13)*

**Capteur candidat (`appairage.html`, non pairé) :** `contact_porte_frigo`
**Statut :** ⛔ Non implémenté — **aucun toggle `input_boolean.module_*` créé pour l'instant**

---

### Secur_M16_Congel *(nouveau, décidé 2026-08-13)*

**Capteur candidat (`appairage.html`, non pairé) :** `contact_porte_congel`
**Statut :** ⛔ Non implémenté — **aucun toggle `input_boolean.module_*` créé pour l'instant**

---

### Secur_M17_Veilleuse_Nuit *(ancien M16 du registre socle)*

**✅ Collision résolue le 13/08** : `raspi/packages/m16_liens_youtube.yaml` s'auto-étiquetait aussi "M16" alors que son toggle réel (`module_m34_liens_youtube`) n'est pas dans le registre officiel — c'est en réalité un sous-composant de Confo_M34 (Télévision). Renommé/fusionné dans `raspi/packages/confo_m34_television/m34_liens_youtube.yaml` le 13/08. Le fichier physique `shell_scripts/m16_liens_youtube.py` n'avait en revanche pas suivi ce renommage — corrigé le 14/08 (voir `M34_television.md`).
**Statut :** ⛔ Non implémenté — toggle `module_lumiere_nuit` seul, aucun fichier, aucune automation ne le consomme

---

## SANTÉ

### Santé_M20_Médicaments *(ancien M13)*
**Statut :** ⛔ Non implémenté — 🔴 **priorité critique** (population Alzheimer)

### Santé_M21_Repas *(ancien M14)*
**Statut :** ⛔ Non implémenté

### Santé_M22_Douche *(ancien M12)*
**Statut :** ⛔ Non implémenté

---

## CONFO (Confort & Loisirs)

### Confo_M30_Kiosk_Ecran *(ancien M07)*
**Fichier dédié :** aucun — le "module" est le dashboard `raspi/dashboards/dashboard_kiosk.yaml` lui-même
**Statut :** ⚠️ Existe sous forme de dashboard, pas de logique d'automation séparée (cohérent avec sa nature)

### Confo_M31_Photos_Famille *(ancien M08)*

> ✅ Révisée le 15/08 : noms de fichier/entités corrigés (l'ancienne section
> parlait de `m08_*`/`m08_photos.yaml`, stale — le vrai préfixe est `m31_*`
> depuis toujours). Vraie rotation multi-photos construite ce jour.

| SOURCE | ENTITÉ | RÔLE | AVAL |
|:-------|:-------|:-----|:-----|
| M00 | `input_boolean.module_kiosk_foto` | On/off module | ⚠️ orphelin — plus consommé par le kiosk actuel |
| Config admin | `input_text.m31_photos_dossier` | Dossier photos (URI media_source) | **non consommé** — le dossier réellement scanné est en dur dans `shell_scripts/m31_photos_liste.py` (`/config/www/photos_famille`), pas piloté par cette entité |
| Config admin | `input_number.m31_photos_intervalle_s` | Intervalle diaporama (s) | ✅ **utilisé depuis le 15/08** — lu par `www/kiosk.html` pour cadencer la rotation |
| `shell_command.m31_photos_liste` (→ `shell_scripts/m31_photos_liste.py`) | liste les fichiers image du dossier | fournit la liste au diaporama | `www/kiosk.html` **et** `www/photos.html` (appel `POST /api/services/shell_command/m31_photos_liste?return_response` — ⚠️ **sans** `=true`, bug corrigé et confirmé en direct le 15/08) |
| `shell_command.m31_photos_supprimer` (→ `shell_scripts/m31_photos_supprimer.py`) | supprime un fichier photo sur disque (`www/` ou `media/`) | contourne la limitation WebSocket-only du service natif HA | `www/photos.html` uniquement (droit 📷 requis, identité réelle) — ⚠️ non vérifié en direct cette session |
| Fichier(s) disque, source `www` (dépôt manuel Samba) | `/config/www/photos_famille/*.jpg|.jpeg|.png|.gif` | Photos du diaporama, non authentifiées | `www/kiosk.html` + `www/photos.html` (`<img src>` direct) |
| Fichier(s) disque, source `media` (upload `photos.html`) | `/media/photos_famille/*.jpg|.jpeg|.png|.gif` | Photos du diaporama, **authentifiées HA** | `www/kiosk.html` + `www/photos.html` (`fetch()` + Bearer + Object URL) |
| `shell_command.m31_photos_televerser_debut/chunk/fin` (→ `shell_scripts/m31_photos_televerser.py`) | upload par morceaux base64, écrit directement sur disque | contourne la restriction admin-only de la route HA native | `www/photos.html` uniquement (droit 📷 requis) — ✅ **confirmé en direct le 15/08**, y compris compte non-admin sur téléphone (app Companion) |
| Secur_M10 | `input_text.m10_droits_aidants` (`m10_gestion_aidants.yaml`, 15/08 suite — remplace les 2 PIN) | JSON bitmask droits d'accès (config/messages/calendrier/video/photos/alertes) | Gate d'accès de `config.html`/`calendrier.html`/`video.html`/`photos.html`, appliqué selon l'identité réelle de connexion (WebSocket `auth/current_user`) — voir M10_gestion_aidants.md |
| — | `script.m31_lancer_diaporama` | Retour à l'état "photos" (`sensor.confo_m34_etat_global`) | appelé par `m34_television.yaml` (fin de créneau/désactivation) — ✅ **vérifié le 15/08, PAS orphelin** : ne fait que la navigation `browser_mod.navigate`, la rotation elle-même est 100% côté client (`kiosk.html`) |
| `aidant.html` → `openPhotos()`/`closePhotos()` | overlay iframe (`#screen-photos` → `photos.html`) | Cohérent avec `config.html` (n'a pas résolu le 401, gardé quand même) | `photos.html` répond via `window.parent.closePhotos()` au bouton retour, repli navigation si ouvert hors iframe |

**Fichier source :** `raspi/packages/m31_photos.yaml`
**Statut :** ✅ Rotation multi-photos + upload **confirmés en direct** le 15/08 (bug `?return_response=true` corrigé). Page dédiée `photos.html` (galerie + suppression réelle via `shell_command.m31_photos_supprimer`) construite le même jour, **confirmée fonctionnelle**. 401 sur l'upload : cause réelle = route HA officielle réservée aux comptes admin (`local_source.py`) — **résolu proprement** via un contournement `shell_command` (upload par morceaux, écrit directement sur disque, fonctionne pour n'importe quel compte non-admin ayant le droit 📷, vérifié par identité réelle), **confirmé en direct** par l'utilisateur, y compris sur téléphone (app Companion). Plus lent que l'ancienne méthode (accepté). Reste : réception automatique par email des photos (non construite).

### Confo_M32_Musique *(ancien M09)*

> ✅ Construite le 13/09/2026 (phase 1). Fiche détaillée :
> [`M32_musique.md`](03_modules_packages/04_divertissement/M32_musique.md)

| SOURCE | ENTITÉ | RÔLE | AVAL |
|:-------|:-------|:-----|:-----|
| `confo_m32_musique/m32_musique.yaml` | `input_boolean.m32_creneau{1..4}_actif` | Interrupteurs des 4 créneaux musique | `www/musique.html` (+ arbitrage kiosk en phase 2) |
| `confo_m32_musique/m32_musique.yaml` | `input_datetime.m32_creneau{1..4}_debut` / `_fin` | Heures début/fin de chaque créneau | `www/musique.html` |
| M00 | `input_boolean.module_m32_kiosk_zic` | On/off « Écran Musique » du kiosk (affiché « M10 ») — déclaré dans `m00_modules.yaml`, ne pas redéclarer | phase 2 (kiosk) |
| `shell_command.m32_musique_liens` (→ `shell_scripts/m32_musique_liens.py`) | liste de liens YouTube partagée (`list` / `add` / `delete`) | stockage `www/musique_liens.txt` (01 à 99) | `www/musique.html` |
| Confo_M34 (sessions TV) | lecture des créneaux TV | contrôle de conflit : un créneau TV **activé** bloque un créneau musique (TV désactivée = rien ; limite exacte autorisée) | `www/musique.html` |

**Fichier source :** `raspi/packages/confo_m32_musique/m32_musique.yaml` (+ `shell_scripts/m32_musique_liens.py`, `www/musique.html`)
**Statut :** 🧪 **Phase 1 construite et testée le 13/09/2026** (créneaux + liens + contrôle de conflit TV, auto-désactivation d'un créneau actif qui devient conflictuel). Phase 2 (lecture sur le kiosk + coupure automatique si session TV activée) à faire.

### Confo_M33_Visio *(ancien M10 — fichier renommé le 2026-08-13)*

> ✅ Révisée le 15/08 : noms de fichier/entités corrigés (l'ancienne section
> parlait de `m10_*`/`m10_visio.yaml`, stale — le vrai préfixe est `m33_*`
> depuis toujours). Double mécanisme unifié ce jour.

| SOURCE | ENTITÉ | RÔLE | AVAL |
|:-------|:-------|:-----|:-----|
| Config admin (`config.html` → Confort → M33 Visio) | `input_text.m33_visio_url` | URL unique de la salle (ex: Google Meet) | `www/kiosk.html` (cadre visio) **et** `www/aidant.html` (bouton "Lancer la Visio") |

**Historique :** conçu à l'origine comme intégration Jitsi (voir `visio_meet.jit.si/`, non retenue). Pivot Google Meet acté le 2026-08-12 : salle permanente `meet.google.com/czg-supk-snw`. Fichier `m20_visio.yaml` renommé `m33_visio.yaml` le 13/08.
**✅ Unifié le 15/08** : l'ancien mécanisme séparé d'`aidant.html` (`localStorage.visio_url` + carte "Lien Visio" dédiée) a été supprimé. Un seul champ de config (`input_text.m33_visio_url`, éditable dans `config.html`) alimente désormais les deux usages. ⚠️ Non vérifié en direct sur HA live cette session (pas de token actif) : à confirmer que `input_text.m33_visio_url` porte bien une valeur (sinon `aidant.html` affiche "URL Visio non configurée").
**✅ Sécurisé le 15/08 (suite, audit Hermes)** : `input_text.m33_visio_url` était injecté brut dans l'iframe kiosk (`allow="camera; microphone"`) sans validation — un lien de phishing collé dans cette entité (éditable par tout compte HA, même non-admin) se serait ouvert en plein écran, caméra+micro auto-autorisés. Corrigé : `isTrustedVisioUrl()` (liste blanche `meet.google.com` uniquement) dans `kiosk.html` et `aidant.html`, déployé et vérifié en direct.
**Fichier source :** `raspi/packages/m33_visio.yaml`
**Statut :** ✅ Implémenté, unifié et sécurisé (liste blanche d'URL)

### Confo_M34_Television *(ancien M11 — 4 sessions)*

> ⚠️ Fiche condensée — voir [`M34_television.md`](03_modules_packages/04_divertissement/M34_television.md)
> pour la chaîne de dépendances complète, la table `entity_id` réels (piège
> `confo_` prefix) et le guide de dépannage détaillé. Réécrite le 14/08 après
> refonte complète du kiosk en HTML pur (`www/kiosk.html`).

| SOURCE | ENTITÉ | RÔLE | AVAL |
|:-------|:-------|:-----|:-----|
| M00 | `input_boolean.module_m34_television` | On/off module | conditionne les automations |
| ~~Config admin~~ | ~~`input_text.m34_browser_id_tv`~~ | 🚫 **Supprimé 18/08** — plus utilisé nulle part (ni TV ni visio, vérifié) | ~~script.m31_lancer_diaporama~~ (vidé, `sequence: []`) |
| Config admin | `input_boolean.m34_session{1,2,3,4}_actif` | Active/désactive chaque session | sensor.confo_m34_etat_global |
| Config admin | `input_datetime.m34_session{1,2,3,4}_debut/fin` | Heures cibles par session | sensor.confo_m34_session_*_fenetre |
| Config admin | `input_select.m34_session{1,2,3,4}_chaine` | Chaîne (france tv/Arte/TV5 Monde/Nat Geo — "YouTube" générique retiré le 14/08) | script.m34_lancer_session |
| Config admin | `input_text.m34_session{1,2,3,4}_youtube_url` | URL YouTube par session | sensor.confo_m34_video_en_cours_embed |
| Confo_M34 (rotation) | `m34_liens_youtube.yaml` (`module_m34_liens_youtube`) | Rotation vidéos + anti-répétition | `sensor.confo_m34_video_en_cours_embed`, alimente les sessions |
| [calculé] | `sensor.confo_m34_etat_global` | État courant + texte_affichage | `www/kiosk.html` (bloc vidéo/photo/visio) |
| Secur_M10 | `input_text.m10_droits_aidants` (`m10_gestion_aidants.yaml`, 15/08 suite — remplace le PIN) | Droit 📺 video (bit 8), identité réelle | Gate d'accès de `www/video.html` (iframe `config.html?only=tv`) |

**Bug session4 corrigé le 14/08** (était noté ici comme connu/non corrigé) :
`sensor.confo_m34_video_en_cours_embed` ne gérait que `session1/2/3` —
session4 ajoutée à la condition.
**Autre bug de fond corrigé le 14/08** : `sensor.confo_m34_etat_global`
référençait des `sensor.m34_session_N_fenetre` inexistants (sans le préfixe
réel `confo_`) — aucune session n'était jamais détectée active, la TV
retombait systématiquement sur "photos" quelle que soit l'heure.
**Automations :** voir fiche `M34_television.md` — 5 dans `m34_television.yaml`, 2 dans `m34_liens_youtube.yaml`
**Fichiers sources :** `raspi/packages/confo_m34_television/m34_television.yaml`, `raspi/packages/confo_m34_television/m34_liens_youtube.yaml`, `raspi/shell_scripts/m34_liens_youtube.py`
**Statut :** ✅ Déployé et fiabilisé le 14/08 — architecture navigateur/browser_mod abandonnée au profit d'un iframe YouTube embed direct dans `kiosk.html`

---

## ENVIR (Environnement)

### Envir_M40_Chauffage *(ancien M17)*
**Statut :** ⛔ Non implémenté — annoncé "stand-by" dès l'origine, jamais construit

---

## 🖥️ DASHBOARDS

| FICHIER | TITRE | TYPE | ENTITÉS CLÉS CONSOMMÉES |
|:--------|:------|:-----|:------------------------|
| `raspi/dashboards/dashboard_kiosk.yaml` | Kiosk (occupant) | panel vertical-stack | `sensor.date_time`, `sensor.m03_agenda_formate`, `sensor.m03_texto_formate`, `sensor.m11_etat_global`, `input_text.m10_visio_url` |
| `raspi/dashboards/dashboard_aidant.yaml` | Interface Aidant | panel (iframe `custom:html-template-card` → `aidant.html`) | tout `aidant.html` (fetch API direct, pas de dashboard Lovelace natif) |
| ~~`raspi/dashboards/dashboard_modules.yaml`~~ | Configuration | **retiré le 13/08** — archivé en local (`raspi/_archive/2026-08-13_nettoyage_bak/dashboards/`), plus dans `configuration.yaml`. Remplacé par `config.html` (bouton 🔧 dans `aidant.html`). | `input_boolean.module_*`, réglages M11, saisie M03 |
| `raspi/dashboards/dashboard_test_simulation.yaml` | Simulation | panel | sensors/helpers `sim_*`, réglages M02 |

**⚠️ 2026-08-13 :** `dashboard_aidant.yaml` a été simplifié — l'ancien dashboard Lovelace natif complet est sauvegardé en `.bak`, remplacé par une iframe unique vers `aidant.html` (HTML custom).
**✅ Arbitrage tranché (13/08) :** `aidant.html` (HTML custom) est la version retenue. Le dashboard natif v2 (`lovelace-aidant-v2`, bubble-card) a été retiré de `configuration.yaml` et archivé en local (`raspi/_archive/2026-08-13_nettoyage_bak/dashboards/dashboard_aidant_v2.yaml`), plus servi en prod.

---

## 📦 INTÉGRATIONS & HACS

| Élément | Usage | Statut |
|:--------|:------|:-------|
| Mushroom | Cartes modernes (entity, template, chips, title) | ✅ |
| Button Card | Boutons CSS custom (kiosk horloge, actions) | ✅ |
| card-mod | CSS override | ✅ |
| Browser Mod | Plein écran + navigation/JS pour Confo_M31/M34 | ✅ |
| html-template-card | Iframe `aidant.html`/`config.html` (contourne le blocage CSP du `webpage` card natif) | ✅ |
| XMLTV EPG (custom) | Calage créneaux TV sur horaires réels | ✅ Source : `https://xmltvfr.fr/xmltv/xmltv_tnt.xml.gz` |
| Zigbee2MQTT | Clé Sonoff EFR32MG21 V2 | ✅ |
| Nabu Casa | Accès distant famille | ✅ (push notifications pas encore configurées) |
| OpenCode (add-on) | Agent IA secondaire, édite Z:\ en direct (`AGENTS.md`, `hab`, `zigporter`) | ✅ actif depuis 10/08 |

---

## 🚧 MODULES EN ATTENTE (par priorité)

| Module | Statut | Priorité |
|:-------|:-------|:---------|
| Santé_M20 Médicaments | ⛔ À faire | 🔴 Critique (Alzheimer) |
| Secur_M12 Caméra IA | ⛔ À faire | 🔴 Critique |
| Secur_M10 SOS (aidants réels + push réel) | 🧪 Simulation, notif non opérationnelle | 🔴 Critique |
| Secur_M13 Porte Ext (2e capteur + agrégation) | ⚠️ Partiel | 🔴 Critique |
| oblig_M02 Inactivité (test conditions réelles) | ✅ Développé, non testé réel | 🔴 Critique |
| Secur_M11 Capteur Lit | 🧪 Simulation | 🟡 Important |
| Confo_M34 Télévision | ✅ Déployé et fiabilisé 14/08 (kiosk.html, bug session4 corrigé, bug entity_id fenêtres corrigé) | ✅ Clos |
| Secur_M14 Fenêtres | ⛔ À faire | 🟡 Important |
| Secur_M15/M16 Frigo/Congel | ⛔ À faire (pas de toggle) | 🟡 Important |
| Santé_M21 Repas | ⛔ À faire | 🟡 Important |
| Santé_M22 Douche | ⛔ À faire | 🟡 Important |
| Secur_M17 Veilleuse Nuit | ⛔ À faire | 🟡 Important |
| Confo_M32 Musique | 🧪 Phase 1 construite 13/09 (créneaux + liens, contrôle de conflit TV) — lecture kiosk (phase 2) à faire | 🟢 Optionnel |
| Envir_M40 Chauffage | ⛔ Stand-by | 🟢 Optionnel |

**Ancien M19/M20 (Dashboard Famille / Messages Famille) :** orphelins, retrait géré séparément par l'utilisateur, hors de ce tableau.
