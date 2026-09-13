# IA_TREE - Arborescences du projet

> Genere le 2026-08-11. Trees du LOCAL (C:\Users\Berry Swann\Documents\Assitant au personne) et de Z:\ (config HA live).
> Exclusions : caches (.cache, deps, .storage, frontend HACS), binaires/images, __pycache__.

## 1. LOCAL - C:\Users\Berry Swann\Documents\Assitant au personne

```
├── docs/
│   ├── 00_IA/
│   │   ├── _gen_tree.py
│   │   ├── IA_CONTEXT_BASE_AI.md
│   │   └── IA_TREE.md
│   ├── 01_config_system/
│   │   ├── MD/
│   │   │   └── configuration.md
│   │   └── YAML/
│   │       └── configuration.yaml
│   ├── 02_dashboards/
│   │   ├── MD/
│   │   │   ├── dashboard_aidant.md
│   │   │   ├── dashboard_kiosk.md
│   │   │   ├── dashboard_modules.md
│   │   │   └── dashboard_test_simulation.md
│   │   └── YAML/
│   │       ├── dashboard_aidant.yaml
│   │       ├── dashboard_kiosk.yaml
│   │       ├── dashboard_modules.yaml
│   │       └── dashboard_test_simulation.yaml
│   ├── 03_modules_packages/
│   │   ├── 01_socle/
│   │   │   ├── M00_modules.md
│   │   │   ├── m00_modules.yaml
│   │   │   ├── M00_simulation.md
│   │   │   ├── m00_simulation.yaml
│   │   │   ├── M00_simulation_sensors.md
│   │   │   └── m00_simulation_sensors.yaml
│   │   ├── 02_securite_alerte/
│   │   │   ├── M02_inactivite.md
│   │   │   ├── m02_inactivite.yaml
│   │   │   ├── M04_gestion_aidants.md
│   │   │   ├── m04_gestion_aidants.yaml
│   │   │   ├── M04_groupe_aidants.md
│   │   │   ├── m04_groupe_aidants.yaml
│   │   │   ├── M04_sos.md
│   │   │   ├── m04_sos.yaml
│   │   │   ├── M05_capteur_lit.md
│   │   │   ├── m05_capteur_lit.yaml
│   │   │   ├── M15_porte_ext.md
│   │   │   └── m15_porte_ext.yaml
│   │   ├── 03_communication/
│   │   │   ├── M03_ecran_msg.md
│   │   │   ├── m03_ecran_msg.yaml
│   │   │   ├── M20_visio.md
│   │   │   └── m20_visio.yaml
│   │   ├── 04_divertissement/
│   │   │   ├── M08_photos.md
│   │   │   ├── m08_photos.yaml
│   │   │   ├── M11_tv.md
│   │   │   ├── m11_tv.yaml
│   │   │   ├── M16_liens_youtube.md
│   │   │   └── m16_liens_youtube.yaml
│   │   └── 05_confort/
│   │       ├── M01_temp_hygro.md
│   │       └── m01_temp_hygro.yaml
│   ├── 04_automations_scripts/
│   │   └── INDEX_automations.md
│   ├── 05_projet/
│   │   ├── CAHIER_DES_CHARGES.md
│   │   ├── dependances.md
│   │   ├── hardware.md
│   │   ├── PROCEDURE_AJOUT_MATERIEL.md
│   │   ├── PROCEDURE_DEPLOIEMENT.md
│   │   ├── PROJET_MODULAIRE_HA_SESSION_2026-06-30.md
│   │   ├── README.md
│   │   ├── STRUCTURE.md
│   │   └── TEST_PROTOCOL.md
│   ├── 06_pages_web/
│   │   ├── aidant.html
│   │   ├── appairage.html
│   │   ├── liens_youtube.txt
│   │   └── README.md
│   ├── DEPENDANCES_GLOBALES.md
│   ├── INDEX.md
│   └── README.md
├── Docs_0/
│   ├── dashboards/
│   │   └── dashboards.md
│   ├── packages/
│   │   ├── M00_modules.md
│   │   ├── M01_temp_hygro.md
│   │   ├── M03_automations.md
│   │   ├── M08_photos.md
│   │   ├── M11_tv.md
│   │   └── M15_porte_ext.md
│   └── installation.md
├── historique/
│   └── histo_2026-08-11_s1.txt
├── raspi/
│   ├── dashboards/
│   │   ├── dashboard_aidant.yaml
│   │   ├── dashboard_kiosk.yaml
│   │   ├── dashboard_modules.yaml
│   │   └── dashboard_test_simulation.yaml
│   ├── historique/
│   │   ├── claude_histo_2026-08-11_raspi_s1.txt
│   │   └── claude_histo_2026-08-11_raspi_s2.txt
│   ├── packages/
│   │   ├── SETUP/
│   │   │   ├── setup_01_capteurs_zigbee.yaml
│   │   │   ├── setup_02_media_camera.yaml
│   │   │   └── setup_03_presence_integrations.yaml
│   │   ├── m00_modules.yaml
│   │   ├── m00_simulation.yaml
│   │   ├── m01_temp_hygro.yaml
│   │   ├── m02_inactivite.yaml
│   │   ├── m03_ecran_msg.yaml
│   │   ├── m04_gestion_aidants.yaml
│   │   ├── m04_groupe_aidants.yaml
│   │   ├── m04_sos.yaml
│   │   ├── m05_capteur_lit.yaml
│   │   ├── m08_photos.yaml
│   │   ├── m11_tv.yaml
│   │   ├── m15_porte_ext.yaml
│   │   └── m16_liens_youtube.yaml
│   ├── www/
│   │   ├── aidant.html
│   │   └── appairage.html
│   ├── configuration.yaml
│   └── NOTES.md
├── visio_meet.jit.si/
│   ├── custom_components/
│   │   └── visio_jitsi/
│   │       ├── __init__.py
│   │       ├── config_flow.py
│   │       ├── const.py
│   │       ├── jitsi_card.js
│   │       ├── manifest.json
│   │       ├── services.yaml
│   │       └── strings.json
│   ├── hacs.json
│   └── README.md
├── CAHIER_DES_CHARGES.md
├── dashboard_aidant_mobile_mockup.html
├── dependances.md
├── hardware.md
├── IA_CONTEXT_BASE_AI.md
├── PROJET_MODULAIRE_HA_SESSION_2026-06-30.md
├── README.md
├── STRUCTURE.md
└── TEST_PROTOCOL.md
```

## 2. Z:\ - config HA live (partage Samba HAOS)

```
├── .cloud/
├── .opencode/
│   ├── skills/
│   │   └── histo/
│   │       └── SKILL.md
│   ├── .gitignore
│   ├── package-lock.json
│   └── package.json
├── blueprints/
│   ├── automation/
│   │   └── homeassistant/
│   │       ├── motion_light.yaml
│   │       └── notify_leaving_zone.yaml
│   ├── script/
│   │   └── homeassistant/
│   │       └── confirmable_notification.yaml
│   └── template/
│       └── homeassistant/
│           └── inverted_binary_sensor.yaml
├── custom_components/
│   ├── browser_mod/
│   │   ├── __init__.py
│   │   ├── binary_sensor.py
│   │   ├── browser.py
│   │   ├── browser_mod.js
│   │   ├── browser_mod_browser_panel.js
│   │   ├── browser_mod_config_panel.js
│   │   ├── camera.py
│   │   ├── config_flow.py
│   │   ├── connection.py
│   │   ├── const.py
│   │   ├── diagnostics.py
│   │   ├── entities.py
│   │   ├── frontend_patch.py
│   │   ├── helpers.py
│   │   ├── light.py
│   │   ├── manifest.json
│   │   ├── media_player.py
│   │   ├── mod_view.py
│   │   ├── panel.py
│   │   ├── sensor.py
│   │   ├── service.py
│   │   ├── services.yaml
│   │   └── store.py
│   ├── hacs/
│   │   ├── repositories/
│   │   │   ├── __init__.py
│   │   │   ├── appdaemon.py
│   │   │   ├── base.py
│   │   │   ├── integration.py
│   │   │   ├── plugin.py
│   │   │   ├── python_script.py
│   │   │   ├── template.py
│   │   │   └── theme.py
│   │   ├── utils/
│   │   │   ├── __init__.py
│   │   │   ├── backup.py
│   │   │   ├── configuration_schema.py
│   │   │   ├── data.py
│   │   │   ├── decode.py
│   │   │   ├── decorator.py
│   │   │   ├── file_system.py
│   │   │   ├── filters.py
│   │   │   ├── github_graphql_query.py
│   │   │   ├── json.py
│   │   │   ├── logger.py
│   │   │   ├── path.py
│   │   │   ├── queue_manager.py
│   │   │   ├── regex.py
│   │   │   ├── store.py
│   │   │   ├── url.py
│   │   │   ├── validate.py
│   │   │   ├── version.py
│   │   │   └── workarounds.py
│   │   ├── validate/
│   │   │   ├── __init__.py
│   │   │   ├── archived.py
│   │   │   ├── base.py
│   │   │   ├── brands.py
│   │   │   ├── description.py
│   │   │   ├── hacsjson.py
│   │   │   ├── images.py
│   │   │   ├── information.py
│   │   │   ├── integration_manifest.py
│   │   │   ├── issues.py
│   │   │   ├── manager.py
│   │   │   ├── README.md
│   │   │   └── topics.py
│   │   ├── websocket/
│   │   │   ├── __init__.py
│   │   │   ├── critical.py
│   │   │   ├── repositories.py
│   │   │   └── repository.py
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── config_flow.py
│   │   ├── const.py
│   │   ├── coordinator.py
│   │   ├── data_client.py
│   │   ├── diagnostics.py
│   │   ├── entity.py
│   │   ├── enums.py
│   │   ├── exceptions.py
│   │   ├── frontend.py
│   │   ├── icons.json
│   │   ├── iconset.js
│   │   ├── manifest.json
│   │   ├── repairs.py
│   │   ├── switch.py
│   │   ├── system_health.py
│   │   ├── types.py
│   │   └── update.py
│   ├── visio_jitsi/
│   │   ├── __init__.py
│   │   ├── config_flow.py
│   │   ├── const.py
│   │   ├── jitsi_card.js
│   │   ├── manifest.json
│   │   ├── services.yaml
│   │   └── strings.json
│   ├── webrtc/
│   │   ├── www/
│   │   │   ├── digital-ptz.js
│   │   │   ├── embed.html
│   │   │   ├── video-rtc.js
│   │   │   └── webrtc-camera.js
│   │   ├── __init__.py
│   │   ├── config_flow.py
│   │   ├── manifest.json
│   │   ├── media_player.py
│   │   ├── services.yaml
│   │   └── utils.py
│   └── xmltv_epg/
│       ├── model/
│       │   ├── __init__.py
│       │   ├── category.py
│       │   ├── channel.py
│       │   ├── episode_number.py
│       │   ├── guide.py
│       │   ├── image.py
│       │   ├── omit_on_error_validator.py
│       │   └── program.py
│       ├── __init__.py
│       ├── api.py
│       ├── config_flow.py
│       ├── const.py
│       ├── coordinator.py
│       ├── entity.py
│       ├── helper.py
│       ├── image.py
│       ├── manifest.json
│       └── sensor.py
├── dashboards/
│   ├── dashboard_aidant.yaml
│   ├── dashboard_aidant.yaml.bak
│   ├── dashboard_kiosk.yaml
│   ├── dashboard_modules.yaml
│   ├── dashboard_test_simulation.yaml
│   └── dashboard_test_simulation.yaml.bak
├── docs/
│   ├── 00_IA/
│   │   └── IA_CONTEXT_BASE_AI.md
│   ├── 01_config_system/
│   │   ├── MD/
│   │   │   └── configuration.md
│   │   └── YAML/
│   │       └── configuration.yaml
│   ├── 02_dashboards/
│   │   ├── MD/
│   │   │   ├── dashboard_aidant.md
│   │   │   ├── dashboard_kiosk.md
│   │   │   ├── dashboard_modules.md
│   │   │   └── dashboard_test_simulation.md
│   │   └── YAML/
│   │       ├── dashboard_aidant.yaml
│   │       ├── dashboard_kiosk.yaml
│   │       ├── dashboard_modules.yaml
│   │       └── dashboard_test_simulation.yaml
│   ├── 03_modules_packages/
│   │   ├── 01_socle/
│   │   │   ├── M00_modules.md
│   │   │   ├── m00_modules.yaml
│   │   │   ├── M00_simulation.md
│   │   │   ├── m00_simulation.yaml
│   │   │   ├── M00_simulation_sensors.md
│   │   │   └── m00_simulation_sensors.yaml
│   │   ├── 02_securite_alerte/
│   │   │   ├── M02_inactivite.md
│   │   │   ├── m02_inactivite.yaml
│   │   │   ├── M04_gestion_aidants.md
│   │   │   ├── m04_gestion_aidants.yaml
│   │   │   ├── M04_groupe_aidants.md
│   │   │   ├── m04_groupe_aidants.yaml
│   │   │   ├── M04_sos.md
│   │   │   ├── m04_sos.yaml
│   │   │   ├── M05_capteur_lit.md
│   │   │   ├── m05_capteur_lit.yaml
│   │   │   ├── M15_porte_ext.md
│   │   │   └── m15_porte_ext.yaml
│   │   ├── 03_communication/
│   │   │   ├── M03_ecran_msg.md
│   │   │   ├── m03_ecran_msg.yaml
│   │   │   ├── M20_visio.md
│   │   │   └── m20_visio.yaml
│   │   ├── 04_divertissement/
│   │   │   ├── M08_photos.md
│   │   │   ├── m08_photos.yaml
│   │   │   ├── M11_tv.md
│   │   │   ├── m11_tv.yaml
│   │   │   ├── M16_liens_youtube.md
│   │   │   └── m16_liens_youtube.yaml
│   │   └── 05_confort/
│   │       ├── M01_temp_hygro.md
│   │       └── m01_temp_hygro.yaml
│   ├── 04_automations_scripts/
│   │   └── INDEX_automations.md
│   ├── 05_projet/
│   │   ├── CAHIER_DES_CHARGES.md
│   │   ├── dependances.md
│   │   ├── hardware.md
│   │   ├── PROJET_MODULAIRE_HA_SESSION_2026-06-30.md
│   │   ├── README.md
│   │   ├── STRUCTURE.md
│   │   └── TEST_PROTOCOL.md
│   ├── DEPENDANCES_GLOBALES.md
│   ├── INDEX.md
│   └── README.md
├── packages/
│   ├── m00_modules.yaml
│   ├── m00_simulation.yaml
│   ├── m00_simulation_sensors.yaml
│   ├── m00_simulation_sensors.yaml.bak
│   ├── m01_temp_hygro.yaml
│   ├── m02_inactivite.yaml
│   ├── m03_ecran_msg.yaml
│   ├── m04_gestion_aidants.yaml
│   ├── m04_gestion_aidants.yaml.bak
│   ├── m04_groupe_aidants.yaml
│   ├── m04_groupe_aidants.yaml.bak
│   ├── m04_sos.yaml
│   ├── m05_capteur_lit.yaml
│   ├── m05_capteur_lit.yaml.bak
│   ├── m08_photos.yaml
│   ├── m11_tv.yaml
│   ├── m15_porte_ext.yaml
│   ├── m16_liens_youtube.yaml
│   └── m20_visio.yaml
├── shell_scripts/
│   └── m16_liens_youtube.py
├── themes/
├── tts/
├── www/
│   ├── community/
│   │   ├── auto-entities/
│   │   │   └── auto-entities.js
│   │   ├── Bubble-Card/
│   │   │   ├── bubble-card.js
│   │   │   └── bubble-pop-up-fix.js
│   │   ├── button-card/
│   │   │   └── button-card.js
│   │   ├── Home-Assistant-Lovelace-HTML-Jinja2-Template-card/
│   │   │   └── html-template-card.js
│   │   ├── lovelace-auto-entities/
│   │   │   └── auto-entities.js
│   │   ├── lovelace-card-mod/
│   │   │   └── card-mod.js
│   │   ├── lovelace-mushroom/
│   │   │   └── mushroom.js
│   │   └── stack-in-card/
│   │       └── stack-in-card.js
│   ├── photos_famille/
│   ├── aidant.html
│   ├── appairage.html
│   ├── liens_youtube.txt
│   └── m16_shorts_ignores.txt
├── .prettierrc.yaml
├── AGENTS.local.md.example
├── AGENTS.md
├── automations.yaml
├── configuration.yaml
├── go2rtc.yaml
├── IA_CONTEXT_BASE_AI.md
├── opencode.json
├── recap.md
├── scenes.yaml
├── scripts.yaml
└── secrets.yaml
```

## Notes

- `docs/` existe en local ET sur Z: (synchronise le 2026-08-11 a 12:15)
- Z: contient des `.bak` dans packages/ et dashboards/ (non charges par HA, a nettoyer)
- `custom_components/` : browser_mod, hacs, visio_jitsi (en test), webrtc, xmltv_epg
- Fichiers IA sur Z: : AGENTS.md, IA_CONTEXT_BASE_AI.md, opencode.json, recap.md, AGENTS.local.md.example