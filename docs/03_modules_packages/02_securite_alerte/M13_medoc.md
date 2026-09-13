# M13 — Rappel Médicaments

> Fiche rédigée le 2026-08-16 à partir de `raspi/packages/m20_medoc.yaml` (local).
> Source live : `Z:\packages\m20_medoc.yaml`.
> ⚠️ Nom d'affichage **M13** (interface), préfixe d'entités **m20** (héritage
> de `input_boolean.module_m20_medoc`, déjà présent dans `m00_modules.yaml`).

## Rôle
Afficher un **rappel** sur l'écran de la personne aidée à l'heure de prise des
médicaments, pour 4 moments de la journée : matin / midi / soir / coucher.
Chaque moment a son heure réglable et s'active indépendamment. Le rappel
s'affiche sur le kiosk pendant une durée réglable (commune aux 4 moments) puis
disparaît tout seul.

## ⚠️ Ce que ce module N'EST PAS
- **Il ne détecte PAS la prise.** Il ne sait pas si le médicament a été pris,
  ni s'il a été pris deux fois. C'est un simple rappel visuel.
- **Ce n'est pas une alerte.** Rien n'est envoyé à un aidant. Décision
  utilisateur 2026-08-16 : « c'est un rappel, ça s'arrête à une notif ».
- **Pas d'acquittement.** Aucun bouton « C'est fait » : le rappel disparaît
  seul à la fin de sa fenêtre d'affichage (décision utilisateur : « affiché un
  certain temps puis disparaît »).

## ⚠️ Piège pathologie — surdosage
Un rappel seul peut être **dangereux** pour une personne à risque de reprise :
elle oublie qu'elle a déjà pris, voit le rappel, reprend → surdosage. À
n'activer que **selon la pathologie**. La vraie sécurité reste le **pilulier
hebdomadaire** préparé par un aidant : le rappel pointe vers le bon
**compartiment** (« compartiment du matin »), il ne distribue rien. Voir
`CAHIER_DES_CHARGES.md §8`.

## Fonctionnement (100 % côté client, pas d'automation)
Le kiosk (`www/kiosk.html`, fonction `refreshMedoc()`) lit les entités et
calcule lui-même s'il faut afficher un rappel : pour chaque zone active, si
l'heure courante est dans la fenêtre `[heure_zone ; heure_zone + durée]`.
Même approche que les sessions TV — rien à importer, distribuable tel quel.
Le bandeau (`#medoc-banner`) est un overlay plein largeur en haut de l'écran,
orange, qui pulse, et se superpose au reste (photos/TV) car un rappel de
médicament doit passer devant. Rafraîchi dans `refreshAll()` (cycle 20 s —
largeur de fenêtre 5-240 min, donc la granularité suffit).

⚠️ Pas de gestion du passage de minuit : un rappel de coucher réglé à 23h50
avec 30 min s'arrête à minuit. Acceptable pour un simple rappel, cas rare.

## Dépendances
| Élément | Source | Statut |
|:--------|:-------|:-------|
| `input_boolean.module_m20_medoc` | M00 (`m00_modules.yaml`) | Interrupteur du module — **déjà déclaré ailleurs**, ne pas redéclarer. Off par défaut. |
| Bandeau kiosk | `www/kiosk.html` (`refreshMedoc`, `#medoc-banner`) | Affichage du rappel |
| Config 4 zones | `www/config.html` (onglet Sécurité → 💊 Rappels médicaments, `buildMedoc`) | Réglage heures + activation + durée |

## Entités
| Entité | Rôle |
|:-------|:-----|
| `input_datetime.m20_medoc_matin` / `_midi` / `_soir` / `_couche` | Heure de rappel de chaque moment (`has_time`, **pas** `has_date`) |
| `input_boolean.m20_medoc_matin_actif` / `_midi_actif` / `_soir_actif` / `_couche_actif` | Active/désactive chaque moment indépendamment |
| `input_number.m20_medoc_duree_min` | Durée d'affichage du rappel (min), commune aux 4 zones (5-240) |

## Pièges connus / TODO
1. ⚠️ **Pas de `initial:`** (piège HA documenté, cf. M10) : sinon les heures
   réglées seraient écrasées à chaque redémarrage. Conséquence : à la toute
   première création, les 4 heures valent 00:00 — à régler une fois via
   Configuration → Sécurité → Rappels médicaments.
2. **Nouvelles entités = redémarrage HA requis** (input_datetime/boolean/
   number ne se rechargent pas à chaud).
3. **Activer aussi le module M13** (`module_m20_medoc`) dans les modules
   Sécurité — sinon `refreshMedoc()` sort immédiatement et rien ne s'affiche.
4. Réservé aux profils **sans risque de reprise** (voir piège surdosage).

## Annotations
- 2026-08-16 : création. 4 zones (matin/midi/soir/coucher), heure réglable +
  activation par zone, durée d'affichage commune. Rappel pur affiché puis
  effacé, sans acquittement ni alerte aidant (décisions utilisateur). Calcul
  côté kiosk, pas d'automation. Déployé (MD5 vérifié), `check_config` valide.
  Redémarrage HA requis pour créer les entités.
