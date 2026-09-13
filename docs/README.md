# Documentation du projet « Assistant au Personne »

> Structure créée le 2026-08-11. Règle : **rien n'est déplacé ni effacé** - ce dossier contient des copies organisées + des fiches rédigées.

## Structure

```
documentation/
├── 00_IA/                  Contexte IA (IA_CONTEXT_BASE_AI.md) - à lire en premier
├── 01_config_system/
│   ├── MD/                 Fiche configuration système
│   └── YAML/               configuration.yaml (copie)
├── 02_dashboards/
│   ├── MD/                 4 fiches (kiosk, aidant, modules, test_simulation)
│   └── YAML/               les 4 dashboards (copies)
├── 03_modules_packages/    CLASSÉ PAR FONCTION
│   ├── 01_socle/           M00 (modules, simulation, sensors)
│   ├── 02_securite_alerte/ M02, M04 (SOS/aidants), M05, M15
│   ├── 03_communication/   M03 (messages), M20 (visio)
│   ├── 04_divertissement/  M08 (photos), M11 (TV), M16 (YouTube)
│   └── 05_confort/         M01 (temp/hygro)
│       → chaque module = fiche .md + YAML source
├── 04_automations_scripts/ INDEX des automations et scripts
├── 05_projet/              CAHIER_DES_CHARGES, hardware, dependances, README,
│                           STRUCTURE, TEST_PROTOCOL, spec du 30/06 (copies)
└── 06_pages_web/           Pages web custom (aidant.html, appairage.html) *(ajout 2026-08-11)*
```

## Sources
- **YAML** : copiés depuis `raspi/` (source de travail) + depuis `Z:\` pour les modules absents du local (m00_simulation_sensors, m16, m20)
- **Fiches .md** : rédigées le 2026-08-11 à partir des YAML
- L'ancien dossier `Docs/` (renommé **`Docs_0/`** le 2026-08-11) reste **intact** (source historique, fiches de juillet)

## Écarts signalés (à traiter)
1. `configuration.yaml` : la prod (Z:) a 2 ressources HACS en plus (auto-entities, html-template-card) - voir 01_config_system/MD/configuration.md
2. Modules `m16_liens_youtube` et `m20_visio` : **absents de raspi/** - copies faites depuis Z: (vérifier s'ils doivent être rapatriés en local)
3. `m00_simulation_sensors.yaml` : présent sur Z: seulement (idem)

## Règle de mise à jour
Ce dossier est un **instantané** : toute modification des YAML dans `raspi/` ou sur Z: doit être reportée ici (ou régénérer la copie) pour rester fidèle.

## Dernière synchronisation (2026-08-11 soir)
- **Z: → docs/** : m03_ecran_msg (22 Ko, grosse évolution Claude), m16_liens_youtube, configuration.yaml (+ panel_custom Outils Dev), dashboard_aidant (30 Ko, nouvelle vue Paramètres), dashboard_kiosk, dashboard_test_simulation (+ section M01/M15), IA_CONTEXT_BASE_AI.md
- **Nouveau** : `06_pages_web/` (aidant.html, appairage.html, liens_youtube.txt)
- **Fiches mises à jour** : configuration, dashboard_test_simulation, pages web + M03/M16/dashboard_aidant (agents en parallèle)
