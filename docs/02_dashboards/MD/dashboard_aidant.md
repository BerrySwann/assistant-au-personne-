# Dashboard Aidant (interface famille)

> Fiche mise à jour le 2026-08-11 à partir de `raspi/dashboards/dashboard_aidant.yaml` (local).
> Source live : `Z:\dashboards\dashboard_aidant.yaml`.
> Version : Claude 18:55.

## Rôle
Interface **à distance** pour les aidants/famille (via Nabu Casa) : envoyer un message à la personne aidée (affiché sur le kiosk M03), suivre le statut rapide de la maison (température, porte, bandeau), lancer la visio, et régler les règles d'envoi des messages (limite par aidant, plage horaire).

## Vues
| Vue | Path | Contenu principal | Cartes principales |
|:----|:-----|:------------------|:-------------------|
| Aidant | `/lovelace/aidant` | Panel unique : chips de statut, température M01, bouton visio, envoi de message M03 (saisie, file d'attente, bandeau) | `mushroom-chips-card`, `mushroom-template-card`, `button-card`, `entities`, `markdown` |
| Paramètres | `/lovelace/settings` | Panel unique : réglage de la limite d'envoi par aidant et de la plage horaire autorisée (M03) | `button-card` (retour), `mushroom-title-card`, `entities`, `grid` |

## Sections détaillées

### Vue « Aidant » (type `panel`)
1. **Chips — statut rapide** (`mushroom-chips-card`) : 4 chips template — température salon (couleur selon `sensor.m01_alerte_temperature` : froid → bleu, canicule → rouge), porte d'entrée (ouverte/fermée via `binary_sensor.snzb04p_porte_ext_contact`), état message (`sensor.m03_bandeau_principal` : "Aucun msg" / "Message actif"), et ⚙️ accès paramètres (`/lovelace/settings`).
2. **Température (M01)** (`grid` 2 colonnes) : 2 `mushroom-template-card` — salon (`sensor.snzb02d_salon_temperature` + `sensor.m01_resume_temp_salon`, icône canapé) et chambre (`sensor.snzb02d_chambre_temperature` + `sensor.m01_resume_temp_chambre`, icône lit) ; couleur bleue si < 16 °C, rouge si > 28 °C.
3. **Visio** (`button-card` dégradé vert) : « Lancer la Visio » → navigation vers `/lovelace/visio`.
4. **💬 Message pour la personne aidée** (titre `mushroom-title-card`, module M03) :
   - Résumé paramètres cliquable : « 🛡️ X msg / Y min » + plage horaire (`input_number.m03_rl_max`, `input_select.m03_rl_fenetre`, `input_datetime.m03_envoi_debut/fin`) → vers `/lovelace/settings`.
   - Carte identité : `button-card` affichant le nom de l'utilisateur connecté (`hass.user?.name`, défaut « La famille »).
   - Champ de saisie (`entities` sur `input_text.m03_message_famille`).
   - Compteur de caractères (`mushroom-template-card`) : max 60, ⚠️ si ≤ 10 restants, rouge dès 55.
   - Bouton **Envoyer** (`button-card` à logique JS embarquée) : icône, libellé, fond et action dynamiques — gris si file pleine (≥ 5), orange si hors plage horaire, orange si rate-limit atteint (attente ~N min), sinon bleu → appelle `script.m03_envoyer` avec `auteur` = nom de l'utilisateur.
   - Liste des messages (`markdown`) : message affiché 🟢 (auteur, heure, âge) + file d'attente ⏳ (n/5).
5. **Statut envoi + bandeau (M03)** :
   - Hint délai (`mushroom-template-card`) : « n messages en attente — s'affichera dans ~15 min » / « Message en cours d'affichage » / « Aucun message ».
   - Bandeau identique kiosk (`mushroom-template-card`) : texte depuis `state_attr('sensor.m03_bandeau_principal','texte')`, icône/couleur selon l'état (`agenda_urgent` rouge, `agenda_proche` orange, `texto` bleu, `agenda_futur` vert), âge d'affichage.

### Vue « Paramètres » (type `panel`)
1. Bouton retour (`button-card`) « Paramètres messages » → `/lovelace/aidant`.
2. **🛡️ Limite d'envoi par aidant** : `grid` 2 colonnes — `input_number.m03_rl_max` (« Messages max ») et `input_select.m03_rl_fenetre` (« Fenêtre (min) »).
3. **🕐 Plage d'envoi autorisée** : `grid` 2 colonnes — `input_datetime.m03_envoi_debut` (« Début ») et `input_datetime.m03_envoi_fin` (« Fin »).

## Cartes utilisées
| Type | Nombre |
|:-----|:-------|
| `custom:mushroom-chips-card` | 1 |
| `custom:mushroom-template-card` | 6 |
| `custom:button-card` | 4 |
| `custom:mushroom-title-card` | 3 |
| `entities` | 5 |
| `markdown` | 1 |
| `grid` | 3 |
| `vertical-stack` | 2 |
| **Total** | **25** |

Dont **14 cartes custom HACS** (mushroom + button-card, avec `card_mod` systématique pour le style) et **11 cartes natives**. Les 2 vues sont en mode `panel`.

## Notes
- **Entités utilisées** (par module) :
  - *M01 (température)* : `sensor.m01_alerte_temperature`, `sensor.m01_resume_temp_salon`, `sensor.m01_resume_temp_chambre`
  - *Capteurs (Z2M)* : `sensor.snzb02d_salon_temperature`, `sensor.snzb02d_chambre_temperature` (Aqara SNZB-02D), `binary_sensor.snzb04p_porte_ext_contact` (SONOFF SNZB-04P)
  - *M03 (messages)* : `sensor.m03_bandeau_principal` (+ attribut `texte`) ; `input_text.m03_message_famille`, `m03_affiche_msg`, `m03_affiche_auteur`, `m03_queue_msg`, `m03_queue_auteur`, `m03_queue_timestamps`, `m03_rate_limit` ; `input_datetime.m03_affiche_depuis`, `m03_envoi_debut`, `m03_envoi_fin` ; `input_number.m03_rl_max` ; `input_select.m03_rl_fenetre` ; `script.m03_envoyer`
- **Intégrateurs** : Zigbee2MQTT (Z2M) pour les capteurs, HACS (Mushroom, button-card, card-mod), Nabu Casa pour l'accès distant des aidants.
- **Logique dynamique** : le bouton Envoyer embarque du JS (template `[[[ ]]]`) qui recalcule en direct icône/libellé/fond/tap_action selon 3 verrous — file pleine (max 5 messages), plage horaire, rate-limit par aidant (`m03_rate_limit`) ; l'auteur est déduit de `hass.user?.name`.
- **File de messages M03** : max 5 en attente, affichage différé (~15 min) quand un message est déjà à l'écran ; message limité à 60 caractères.
- Le bouton « Lancer la Visio » est déjà en place (navigation vers la vue visio).

## Mise à jour 2026-08-13 — Deux évolutions majeures

### 1. L'ancien dashboard (25 cartes) a été remplacé le 12/08
`dashboard_aidant.yaml` (Z:) ne contient plus que **388 octets** : une vue qui charge `www/aidant.html` en iframe via `local/launch.html` (cache-buster). La page HTML autonome (token localStorage, config.json) est devenue **l'interface aidant principale** — la doc ci-dessus (25 cartes, version « Claude 18:55 ») décrit une version **archivée**.

### 2. Nouveau `dashboard_aidant_v2.yaml` — migration native (en test 13/08)
Réponse à la règle produit « grand public, hyper simple » : un **dashboard 100% natif** (zéro HTML, zéro token, zéro cache) déclaré `lovelace-aidant-v2` dans `configuration.yaml`, design **Bubble Card** (HACS) :
- **2 vues** : `accueil` (en-tête, températures, bouton Visio → Meet, bandeau, saisie + Envoyer, file) et `parametres` (réglages + bouton reset `script.m03_reset_reglages`)
- **Mobile-first** : `max_width: 480px`, une seule colonne, 90% d'usage téléphone
- L'auteur du message passe par `[[[ return user.name; ]]]` (JS button-card/bubble-card — le Jinja `{{ user }}` n'est pas rendu dans service_data)
- Source : `visio_meet.jit.si/maquette/dashboard_aidant_v2.yaml` (maquette) + Z:
- ⚠️ Les 2 interfaces coexistent en test : aidant.html (fiable, corrigé) vs v2 (natif). Décision de bascule à l'usage.
