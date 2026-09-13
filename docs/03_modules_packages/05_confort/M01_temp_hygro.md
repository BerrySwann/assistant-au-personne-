# M01 — Température & Hygrométrie

> Fiche rédigée le 2026-08-11 à partir de `raspi/packages/m01_temp_hygro.yaml` (local).
> Source live : `Z:\packages\m01_temp_hygro.yaml`.

## Rôle
Surveiller température et humidité des pièces (SONOFF SNZB-02D, Zigbee Z2M) :
- **Statistiques 24 h** : min/max température salon et chambre, moyenne humidité salon (plateforme `statistics`, fenêtre 24 h, échantillonnage 150)
- **Alertes confort** : froid (< 16 °C) ou canicule (> 28 °C) au salon, froid en chambre (< 16 °C), humidité élevée (> 70 %) ou basse (< 30 %)
- **Résumés** : « T°C ↓min° ↑max° » prêts à l'affichage pour le salon et la chambre

Toutes les alertes passent à `inactif` quand `module_temp_hygro` est OFF. Aucune automation ni notification dans le package : les alertes sont des capteurs template consommés par l'UI.

## Dépendances
| Élément | Source | Statut |
|:--------|:-------|:-------|
| `sensor.snzb02d_salon_temperature` | SONOFF SNZB-02D salon (Zigbee Z2M) | ⚠️ Adapter l'entity_id si le nom Z2M diffère (avertissement du YAML) |
| `sensor.snzb02d_salon_humidity` | SONOFF SNZB-02D salon (Zigbee Z2M) | ⚠️ idem |
| `sensor.snzb02d_chambre_temperature` | SONOFF SNZB-02D chambre (Zigbee Z2M) | ⚠️ idem |
| `input_boolean.module_temp_hygro` | Interrupteur de module (M00) | Référencé dans les templates mais NON déclaré dans ce package — ne pas le redéclarer ici |

## Entités
| Entité | Rôle |
|:-------|:-----|
| `sensor.m01_temp_salon_min_24h` | Min 24 h température salon (`value_min`, fenêtre 24 h, échantillonnage 150) |
| `sensor.m01_temp_salon_max_24h` | Max 24 h température salon (`value_max`) |
| `sensor.m01_hygro_salon_avg_24h` | Moyenne 24 h humidité salon (`mean`) |
| `sensor.m01_temp_chambre_min_24h` | Min 24 h température chambre (`value_min`) |
| `sensor.m01_temp_chambre_max_24h` | Max 24 h température chambre (`value_max`) |
| `sensor.m01_alerte_temperature` | États : `inactif` / `froid` (< 16 °C salon) / `canicule` (> 28 °C salon) / `froid_chambre` (< 16 °C chambre) / `ok` ; attribut `message` |
| `sensor.m01_alerte_humidite` | États : `inactif` / `elevee` (> 70 %) / `basse` (< 30 %) / `ok` |
| `sensor.m01_resume_temp_salon` | Résumé salon « T°C ↓min° ↑max° » (icon mdi:sofa) |
| `sensor.m01_resume_temp_chambre` | Résumé chambre « T°C ↓min° ↑max° » (icon mdi:bed) |

## Automations
Aucune automation dans le YAML source (module purement déclaratif : statistiques + templates).

## Pièges connus / TODO
1. ⚠️ **Avertissement du YAML** : « Adapter les entity_id sources si le nom Z2M diffère » — les 3 `sensor.snzb02d_*` dépendent du nommage effectif après pairage du SNZB-02D
2. **Défauts `float` incohérents** : l'état `m01_alerte_temperature` utilise `float(20)` mais l'attribut `message` utilise `float(0)` — si un capteur est indisponible, l'état reste `ok` (20 par défaut) alors que le message affiche « ⚠️ Froid au salon : 0°C » (même mécanique pour l'humidité avec `float(50)`)
3. **Panne capteur masquée** : les valeurs par défaut font retomber les templates sur `ok` — une coupure du capteur n'est pas détectable via l'alerte (à surveiller côté Z2M)
4. **Humidité chambre non exploitée** : seule l'humidité du salon est référencée dans le package (aucun `snzb02d_chambre_humidity`)
5. **Aucune notification** : les alertes sont des capteurs template consommés par l'UI — aucune alerte push ni automation n'est générée ici
6. `input_boolean.module_temp_hygro` non déclaré dans ce package : doit venir de M00 (ne pas le redéclarer, conflit de clé entre packages)

## Annotations
- 2026-08-11 : fiche rédigée — aucune `annotations_log` dans le YAML source.
