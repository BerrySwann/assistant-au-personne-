# Structure du repo

```
assistant-au-personne-/
│
├── README.md                        ← Présentation du projet
├── profil_template.json             ← Template profil vide
├── CONTRIBUTING.md                  ← Comment contribuer (à créer)
├── LICENSE                          ← MIT (à créer)
│
├── docs/
│   ├── questionnaire.md             ← Questions + mapping modules (à créer)
│   ├── hardware.md                  ← Liste matériel + aperçu prix (à créer)
│   └── installation.md              ← Guide pas à pas HAOS (à créer)
│
└── modules/
    │
    ├── temperature_monitor/         ← OBLIGATOIRE
    │   ├── README.md
    │   ├── sensors.yaml
    │   ├── automations.yaml
    │   └── dashboard_card.yaml
    │
    ├── inactivity_monitor/          ← OBLIGATOIRE
    │   ├── README.md
    │   ├── sensors.yaml
    │   ├── automations.yaml
    │   └── dashboard_card.yaml
    │
    ├── screen_messages/             ← OBLIGATOIRE
    ├── camera_monitoring/           ← FORTEMENT CONSEILLÉ
    ├── sos_button/                  ← FORTEMENT CONSEILLÉ
    ├── mattress_sensor/             ← FORTEMENT CONSEILLÉ
    ├── kiosk_screen/
    ├── kiosk_photos/
    ├── tv_control/
    ├── music_therapy/
    ├── youtube_invidious/
    ├── visio_jitsi/
    ├── shower_tracking/
    ├── medication_reminder/
    ├── meal_reminder/
    ├── door_monitor/
    ├── night_lighting/
    ├── family_dashboard/
    └── heating_control/
```

## Convention par module

Chaque dossier `modules/xxx/` contient :

| Fichier | Contenu |
|---------|---------|
| `README.md` | Description, matériel requis, aperçu prix, guide installation |
| `sensors.yaml` | Capteurs et templates HA |
| `automations.yaml` | Automations HA |
| `dashboard_card.yaml` | Carte Lovelace (Mushroom Cards) |

## Convention YAML

Même style que le projet `home_assistant_re-build` :
- Bordures ASCII (╭─╮ titre principal, ┌─┐ titre secondaire)
- Header obligatoire : DESCRIPTION / CALCUL & SOURCES / DÉPENDANCES / VIGNETTES
- Slug `# --- unique_id ---` avant chaque entité
- `unique_id` en minuscules avec underscores
- `name` avec majuscules initiales
