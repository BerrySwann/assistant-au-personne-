# M32 — Musique (4 Créneaux + Liste de Liens YouTube)

> Fiche créée le 2026-09-13, à la construction de la **phase 1**.
> Sources live : `Z:\packages\confo_m32_musique\m32_musique.yaml`,
> `Z:\shell_scripts\m32_musique_liens.py`, `Z:\www\musique.html`,
> `Z:\www\musique_liens.txt`.

## État actuel

**Phase 1 (programmation) construite et testée le 13/09/2026** — créneaux,
liens, page de réglage, contrôle de conflit avec la TV.
**Phase 2 (lecture sur le kiosk + arbitrage automatique) À FAIRE.**

## Principe

- **4 créneaux horaires**, sur le modèle des sessions TV (M34) : chacun a une
  heure de début, une heure de fin et un interrupteur actif/inactif.
- **Une seule liste de liens YouTube** partagée par tous les créneaux,
  numérotée de 01 à 99, stockée dans `www/musique_liens.txt`.
- L'écran Musique du kiosk = `input_boolean.module_m32_kiosk_zic` (déclaré
  dans `m00_modules.yaml`, affiché « M10 — Écran Musique » dans `config.html`).

## Règle d'arbitrage — la TV (M34) est PRIORITAIRE

Priorité d'affichage du kiosk : **Visio > TV > Musique > Photos**.

- Un créneau musique ne peut pas chevaucher un créneau TV **activé** →
  refusé par `musique.html` (message explicite) ;
- un créneau TV **désactivé** ne bloque rien ;
- la **limite exacte** (début musique = fin TV) est autorisée ;
- la modification des heures d'un créneau musique **actif** qui créerait un
  conflit → **auto-désactivation** du créneau avec message (plutôt qu'un
  refus en bloc) ;
- (phase 2) si un créneau TV devient actif pendant qu'une musique tourne,
  la musique sera coupée.

## Entités (`m32_musique.yaml`)

| Entité | Type | Rôle |
|:---|:---|:---|
| `input_boolean.m32_creneau{1..4}_actif` | input_boolean | Interrupteur du créneau |
| `input_datetime.m32_creneau{1..4}_debut` | input_datetime (heure seule) | Début du créneau |
| `input_datetime.m32_creneau{1..4}_fin` | input_datetime (heure seule) | Fin du créneau |
| `input_boolean.module_m32_kiosk_zic` | input_boolean | Écran Musique du kiosk (M10, déclaré dans `m00_modules.yaml`) |
| `shell_command.m32_musique_liens` | shell_command | Gestion des liens (`list` / `add` / `delete`) |

Valeurs d'usine : créneaux tous **inactifs**, heures à `00:00`. Réglage
depuis l'interface aidant : bouton **🎵 Musique** (page `musique.html`).

## Gestion des liens (`m32_musique_liens.py`)

- `list` → affiche les liens numérotés (`01` à `99`) ;
- `add <url>` → ajoute un lien (doublon refusé) ;
- `delete <num>` → supprime la ligne numéro `<num>`.
- Fichier de stockage : `www/musique_liens.txt` (une URL par ligne ;
  **doit exister**, créé vide à l'installation).

## Page `musique.html`

- En haut : les **4 créneaux TV (M34)** en lecture (visualiser les plages
  déjà occupées) ;
- au milieu : les **4 créneaux musique** (on/off + heures) avec contrôle de
  conflit en direct ;
- en bas : ajout d'un lien YouTube + suppression par numéro.

## Tests effectués le 13/09/2026

- Backend : ajout (`#01`), doublon refusé, suppression (`#01`), saisie
  hors-plage → OK ;
- conflits TV (4 cas testés) : chevauchement TV activée = **bloqué** ;
  TV désactivée = autorisé ; hors plage TV = autorisé ; limite exacte
  (début musique = fin TV) = autorisé ;
- auto-désactivation d'un créneau actif dont les heures deviennent
  conflictuelles → OK.

## Phase 2 (à faire)

- Lecture de la musique sur le **kiosk** (écran Musique, player YouTube) ;
- coupure automatique si une session TV (M34) devient active ;
- intégration complète à la priorité d'affichage Visio > TV > Musique > Photos.

## Pièges

- `input_boolean.module_m32_kiosk_zic` vit dans `m00_modules.yaml` — ne PAS
  le redéclarer dans ce package (clé dupliquée = écrasement silencieux en
  YAML, même piège que les blocs `input_text:` dupliqués de `m33_visio.yaml`).
- Les `entity_id` de ce module sont créés directement depuis le YAML
  (vérifiés sur l'instance le 13/09 : pas de renommage `confo_` à surveiller
  ici, contrairement à M34).
- Le format des liens passe par un fichier texte : pas de caractères `|`
  (séparateur des règles M03, sans impact ici mais par cohérence).
