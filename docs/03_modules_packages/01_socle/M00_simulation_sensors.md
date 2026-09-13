# M00-SIM (M01/M15) — Simulation Temp & Porte

> Fiche rédigée le 2026-08-11 à partir de `raspi/packages/m00_simulation_sensors.yaml` (local).
> Source live : `Z:\packages\m00_simulation_sensors.yaml`.

## Rôle
Module **socle / simulation** : simuler les capteurs **SNZB-02D** (température/hygrométrie) et **SNZB-04P** (contact porte) tant que le matériel réel n'est pas pairé. Permet à **M01, M15 et l'interface Aidant** d'afficher des valeurs simulées.

⚠️ **À SUPPRIMER AU PAIRAGE DES VRAIS CAPTEURS** : ces template sensors portent les entity_id des futurs capteurs réels et les **masqueraient** s'ils étaient pairés en même temps.

⚠️ **Noms volontairement sans tiret (« SNZB02D »)** : le tiret deviendrait « _ » dans l'entity_id (`snzb_02d_*` au lieu de `snzb02d_*`). Pas de `unique_id` : les entity_id sont dérivés du nom (les anciennes entrées `snzb_02d_*` du registry ont été désactivées).

## Dépendances
| Élément | Source | Statut |
|:--------|:-------|:-------|
| `input_number.sim_temp_salon` | Simulation SNZB-02D salon (température) | ⚠️ Placeholder — à supprimer au pairage du vrai capteur |
| `input_number.sim_temp_chambre` | Simulation SNZB-02D chambre (température) | ⚠️ Placeholder — idem |
| `input_number.sim_hygro_salon` | Simulation SNZB-02D salon (hygrométrie) | ⚠️ Placeholder — idem |
| `input_boolean.sim_porte_ext_contact` | Simulation SNZB-04P (contact porte) | ⚠️ Placeholder — idem |
| Modules M01 / M15 / interface Aidant | Consommateurs des valeurs simulées | Affichent ces valeurs tant que le matériel n'est pas là |

## Entités
| Entité | Rôle |
|:-------|:-----|
| `input_number.sim_temp_salon` | « SIMU — Température Salon » (5-35 °C, pas 0.5, défaut 21) |
| `input_number.sim_temp_chambre` | « SIMU — Température Chambre » (5-35 °C, pas 0.5, défaut 19) |
| `input_number.sim_hygro_salon` | « SIMU — Hygrométrie Salon » (10-90 %, pas 1, défaut 50) |
| `input_boolean.sim_porte_ext_contact` | « SIMU — Porte extérieure (**ON = fermée, OFF = ouverte**) » — `initial: true` |
| `sensor.SNZB02D Salon Temperature` | Template sensor (device_class `temperature`, °C) — renvoie `sim_temp_salon` — ⚠️ simulé, sans unique_id |
| `sensor.SNZB02D Salon Humidity` | Template sensor (device_class `humidity`, %) — renvoie `sim_hygro_salon` — ⚠️ simulé, sans unique_id |
| `sensor.SNZB02D Chambre Temperature` | Template sensor (device_class `temperature`, °C) — renvoie `sim_temp_chambre` — ⚠️ simulé, sans unique_id |
| `binary_sensor.SNZB04P Porte Ext Contact` | Template binary_sensor (device_class `opening`) — ON si `sim_porte_ext_contact` = on — ⚠️ simulé, sans unique_id |

## Automations
| ID | Alias | Déclencheur | Action |
|:---|:------|:------------|:-------|
| — | Aucune dans ce package | — | Fichier déclaratif (helpers + template sensors) |

## Pièges connus / TODO avant déploiement
1. ⚠️ **À supprimer au pairage des vrais capteurs** : les template sensors portent les entity_id des futurs capteurs réels et les masqueraient s'ils étaient pairés en même temps
2. **Noms sans tiret volontairement (SNZB02D)** : ne pas renommer — le tiret donnerait `snzb_02d_*` au lieu de `snzb02d_*` dans l'entity_id
3. **Pas de `unique_id`** : entity_id dérivés du nom ; les anciennes entrées `snzb_02d_*` du registry ont été désactivées
4. **Valeurs simulées** : pilotées à la main (input_number / input_boolean) — affichées à M01, M15 et l'interface Aidant, ne pas les confondre avec de vraies mesures
5. **`sim_porte_ext_contact` : ON = fermée, OFF = ouverte** (logique inversée par rapport à un contact réel, à garder en tête lors des tests M15)

## Annotations
- Pas d'`annotations_log` dans la source YAML.
