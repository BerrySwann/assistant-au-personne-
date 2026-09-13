# M16 - Liens YouTube

> Fiche mise à jour le 2026-08-11 à partir de `Z:\packages\m16_liens_youtube.yaml` (module modifié le 11/08).

## Rôle
Récupérer les dernières vidéos des chaînes YouTube officielles (france tv, Arte, France 2) + playlist Destination Francophonie (TV5MONDE) via **flux RSS (sans clé API)**, et les stocker dans `www/liens_youtube.txt` (lisible via `/local/liens_youtube.txt`).

Chaque session M11 choisit sa chaîne (france tv / Arte / TV5 Monde / YouTube) via `input_select.m11_sessionN_chaine` — la rotation M16 injecte la plus récente vidéo **NON vue** de cette chaîne. Si la chaîne est épuisée, la plus récente de la chaîne est rejouée. Les vidéos jouées sont marquées « déjà_vu ».

Format d'une ligne : `aaaa-mm-jj|chaine|Titre|https://youtu.be/XXXX|déjà_vu` — dernier champ vide = vidéo pas encore vue.

⚠️ Script : `shell_scripts/m16_liens_youtube.py` (actions `update` / `mark` / `next` avec arg2 = URL pour `mark`, label de chaîne pour `next`).

## Dépendances
| Élément | Source | Statut |
|:--------|:-------|:-------|
| `sensor.m11_etat_global` + `input_text.m11_sessionN_youtube_url` | Module M11 (m11_tv.yaml) | Construction de l'URL embed (session active) |
| `input_select.m11_sessionN_chaine` | Module M11 (m11_tv.yaml) | Choix de chaîne par session (rotation M16) |
| `shell_scripts/m16_liens_youtube.py` | `/config/shell_scripts/` (externe au package) | Script Python — actions update / mark / next |
| Flux RSS france tv, Arte, France 2 + playlist Destination Francophonie (TV5MONDE) | Externes (sans clé API) | Source des vidéos |
| `www/liens_youtube.txt` | Généré par le script | Lisible via `/local/liens_youtube.txt` |

## Entités
| Entité | Rôle |
|:-------|:-----|
| `input_boolean.module_liens_youtube` | « M16 Liens YouTube (france tv, Arte, TV5, FR2) » — interrupteur de module déclaré **dans ce package** (pas dans M00) |
| `shell_command.m16_liens_youtube` | `python3 /config/shell_scripts/m16_liens_youtube.py {{ action | default('') }} {{ arg2 | default('') }}` |
| `sensor.m16_video_embed` | « M16 Vidéo En Cours (embed) » — URL embed `youtube-nocookie` (`?autoplay=1&rel=0`) dérivée de l'URL YouTube de la session active (`sensor.m11_etat_global` = session1..session3) |

## Automations
| ID | Alias | Déclencheur | Action |
|:---|:------|:------------|:-------|
| `m16_maj_liens_hebdo` | M16 — Mise à jour hebdo des liens YouTube | `time` 09:00:00, condition : jour `mon` | `shell_command.m16_liens_youtube` avec `action: update` |

Mode `single`.

## Pièges connus / TODO avant déploiement
1. **Dépendance externe** : le script `python3 /config/shell_scripts/m16_liens_youtube.py` doit exister sur le système (non embarqué dans le package) — vérifier sa présence et son exécutabilité.
2. **Seule l'action `update` est automatisée** (hebdo, lundi 09:00) : les actions `mark` / `next` du script ne sont pas déclenchées par une automation de ce package (appelées ailleurs ou manuellement).
3. **Chaîne épuisée** : la plus récente de la chaîne est rejouée (comportement par conception, décrit en en-tête du module).
4. **`module_liens_youtube` déclaré ici** (et non dans m00_modules.yaml) et **non utilisé comme condition** par l'automation du package — cohérence à vérifier si d'autres modules en dépendent.
5. **Fichier `www/liens_youtube.txt` régénéré par `update`** : format `aaaa-mm-jj|chaine|Titre|URL|déjà_vu` — ne pas éditer à la main (écrasé à la prochaine mise à jour).

## Annotations
- 2026-08-11 : module modifié — le template `m16_video_embed` ne teste plus `session4` (vestige de la version précédente corrigé ; seules les sessions 1 à 3 sont gérées, conformément à M11).
- Pas d'`annotations_log` dans la source YAML.
