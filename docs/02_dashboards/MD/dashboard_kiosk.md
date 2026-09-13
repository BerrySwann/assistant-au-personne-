# Dashboard Kiosk (écran occupant)

> Fiche rédigée le 2026-08-11 à partir de `raspi/dashboards/dashboard_kiosk.yaml`.
> Source live : `Z:\dashboards\dashboard_kiosk.yaml`.

## Rôle
Écran permanent de l'occupant (kiosk TV) - **zéro interaction complexe requise**. Affiche l'horloge, les messages, la TV/photos selon les modules actifs.

## Vue unique : « Accueil »
- 4 cartes `custom` (cartes personnalisées - Browser Mod / HTML / autres)
- 1 `vertical-stack`

## Caractéristiques
| Élément | Détail |
|:--------|:-------|
| Mode | YAML (déclaré dans configuration.yaml) |
| URL | `/lovelace-kiosk` |
| Icône | `mdi:television` |
| Public | Occupant uniquement |

## Notes
- C'est l'écran cible des redirections navigateur (M11 TV, visio M20) : après un appel/une session, le navigateur y revient
- Le dashboard affiche des cartes conditionnelles selon `sensor.m11_etat_global` (bascule TV/Photos)
