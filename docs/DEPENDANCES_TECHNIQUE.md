# DEPENDANCES TECHNIQUE — Assistant au personne
*Genere automatiquement par `sync_dependances.py` — 2026-08-29*

Chaine : **fichier source -> entites produites -> consommateurs** (YAML, dashboards, JS, automations, scripts).

## Sources analysees

- `automations.yaml` (2 entites referencees)
- `configuration.yaml` (1 entites referencees)
- `dashboards/dashboard_aidant.yaml` (0 entites referencees)
- `dashboards/dashboard_kiosk.yaml` (0 entites referencees)
- `dashboards/dashboard_modules.yaml` (48 entites referencees)
- `dashboards/dashboard_test_simulation.yaml` (31 entites referencees)
- `packages/confo_m32_musique/m32_musique.yaml` (2 entites referencees)
- `packages/confo_m34_television/m34_liens_youtube.yaml` (11 entites referencees)
- `packages/confo_m34_television/m34_television.yaml` (53 entites referencees)
- `packages/m00_modules.yaml` (0 entites referencees)
- `packages/m00_simulation.yaml` (5 entites referencees)
- `packages/m00_simulation_sensors.yaml` (4 entites referencees)
- `packages/m01_temp_hygro.yaml` (8 entites referencees)
- `packages/m02_inactivite.yaml` (45 entites referencees)
- `packages/m02_log_presence.yaml` (1 entites referencees)
- `packages/m11_capteur_lit.yaml` (2 entites referencees)
- `packages/m13_porte_ext.yaml` (1 entites referencees)
- `packages/m20_medoc.yaml` (1 entites referencees)
- `packages/m31_photos.yaml` (11 entites referencees)
- `packages/m33_visio.yaml` (6 entites referencees)
- `packages/oblig_m03_ecran_msg/m03_ecran_msg.yaml` (28 entites referencees)
- `packages/oblig_m03_ecran_msg/m03_rdv_recurrents.yaml` (4 entites referencees)
- `packages/secur_m10_sos/m10_gestion_aidants.yaml` (4 entites referencees)
- `packages/secur_m10_sos/m10_groupe_aidants.yaml` (8 entites referencees)
- `packages/secur_m10_sos/m10_sos.yaml` (9 entites referencees)
- `scenes.yaml` (0 entites referencees)
- `scripts.yaml` (0 entites referencees)
- `shell_scripts/m03_rdv_recurrents.py` (3 entites referencees)
- `shell_scripts/m31_photos_liste.py` (1 entites referencees)
- `shell_scripts/m31_photos_supprimer.py` (1 entites referencees)
- `shell_scripts/m31_photos_televerser.py` (1 entites referencees)
- `shell_scripts/m32_musique_liens.py` (1 entites referencees)
- `shell_scripts/m33_visio_signal.py` (0 entites referencees)
- `shell_scripts/m34_liens_youtube.py` (1 entites referencees)
- `www/aidant.html` (66 entites referencees)
- `www/appairage.html` (6 entites referencees)
- `www/calendrier.html` (4 entites referencees)
- `www/config.html` (59 entites referencees)
- `www/config.json` (0 entites referencees)
- `www/kiosk.html` (27 entites referencees)
- `www/launch.html` (0 entites referencees)
- `www/musique.html` (8 entites referencees)
- `www/photos.html` (10 entites referencees)
- `www/video.html` (4 entites referencees)

## Chaines de dependances par module

### (natif/autre)

```
packages/confo_m34_television/m34_liens_youtube.yaml
  └─→ automation.confo_m34_mise_a_jour_hebdo_des_liens_youtube
packages/confo_m34_television/m34_television.yaml
  └─→ automation.confo_m34_bouton_ok_relancer_la_session_avec_la_chaine_choisie
  └─→ automation.confo_m34_retour_photos_si_module_tv_desactive
  └─→ automation.confo_m34_verifier_les_sessions_tv_toutes_les_minutes
packages/m00_modules.yaml
  └─→ input_boolean.module_dashboard_fam
  └─→ input_boolean.module_msg_famille
packages/m00_simulation_sensors.yaml
  └─→ binary_sensor.snzb04p_porte_ext_contact
  └─→ sensor.snzb02d_chambre_temperature
  └─→ sensor.snzb02d_salon_humidity
  └─→ sensor.snzb02d_salon_temperature
```

**Consomme par :**

- `dashboards/dashboard_modules.yaml` : input_boolean.module_dashboard_fam, input_boolean.module_msg_famille
- `packages/m01_temp_hygro.yaml` : sensor.snzb02d_chambre_temperature, sensor.snzb02d_salon_humidity, sensor.snzb02d_salon_temperature
- `packages/m13_porte_ext.yaml` : binary_sensor.snzb04p_porte_ext_contact
- `www/aidant.html` : binary_sensor.snzb04p_porte_ext_contact, sensor.snzb02d_chambre_temperature, sensor.snzb02d_salon_temperature
- `www/config.html` : input_boolean.module_dashboard_fam, input_boolean.module_msg_famille

### M01

```
packages/m00_modules.yaml
  └─→ input_boolean.module_m01_temp_hygro
packages/m01_temp_hygro.yaml
  └─→ sensor.m01_alerte_humidite
  └─→ sensor.m01_alerte_temperature
  └─→ sensor.m01_hygro_salon_avg_24h
  └─→ sensor.m01_resume_temp_chambre
  └─→ sensor.m01_resume_temp_salon
  └─→ sensor.m01_temp_chambre_max_24h
  └─→ sensor.m01_temp_chambre_min_24h
  └─→ sensor.m01_temp_salon_max_24h
  └─→ sensor.m01_temp_salon_min_24h
```

**Consomme par :**

- `dashboards/dashboard_modules.yaml` : input_boolean.module_m01_temp_hygro
- `packages/m01_temp_hygro.yaml` : input_boolean.module_m01_temp_hygro
- `www/aidant.html` : input_boolean.module_m01_temp_hygro
- `www/config.html` : input_boolean.module_m01_temp_hygro

### M02

```
packages/m00_modules.yaml
  └─→ input_boolean.m02_pir_couloir_actif
  └─→ input_boolean.m02_pir_cuisine_actif
  └─→ input_boolean.m02_pir_sdb_actif
  └─→ input_boolean.m02_presence_chambre_actif
  └─→ input_boolean.m02_presence_salon_actif
  └─→ input_boolean.module_m02_inactivite
packages/m02_inactivite.yaml
  └─→ automation.m02_activite_detectee_reset_horodatage
  └─→ automation.m02_check_inactivite_toutes_les_5_min
  └─→ automation.m02_fin_apres_midi_apprentissage_seuil
  └─→ automation.m02_fin_matin_apprentissage_seuil
  └─→ automation.m02_fin_nuit_apprentissage_seuil
  └─→ automation.m02_fin_sieste_apprentissage_seuil
  └─→ automation.m02_fin_soiree_apprentissage_seuil
  └─→ binary_sensor.m02_activite_detectee
  └─→ input_boolean.m02_absence_nuit_anormale
  └─→ input_boolean.m02_alerte_active
  └─→ input_datetime.m02_derniere_activite
  └─→ input_number.m02_ema_alpha
  └─→ input_number.m02_facteur_alerte
  └─→ input_number.m02_facteur_apprentissage
  └─→ input_number.m02_jours_apprentissage
  └─→ input_number.m02_obs_gap
  └─→ input_number.m02_seuil_aprem
  └─→ input_number.m02_seuil_matin
  └─→ input_number.m02_seuil_nuit
  └─→ input_number.m02_seuil_sieste
  └─→ input_number.m02_seuil_soir
  └─→ sensor.m02_inactivite_minutes
  └─→ sensor.m02_seuil_alerte_effectif
  └─→ sensor.m02_seuil_tranche_actuelle
  └─→ sensor.m02_tranche_horaire
packages/m02_log_presence.yaml
  └─→ shell_command.m02_log_presence_salon
```

**Consomme par :**

- `automations.yaml` : shell_command.m02_log_presence_salon
- `dashboards/dashboard_modules.yaml` : input_boolean.module_m02_inactivite
- `dashboards/dashboard_test_simulation.yaml` : binary_sensor.m02_activite_detectee, input_boolean.m02_absence_nuit_anormale, input_boolean.m02_alerte_active, input_boolean.module_m02_inactivite, input_datetime.m02_derniere_activite, input_number.m02_facteur_alerte, input_number.m02_jours_apprentissage, input_number.m02_obs_gap (+9)
- `packages/m02_inactivite.yaml` : input_boolean.module_m02_inactivite
- `www/appairage.html` : input_boolean.m02_pir_couloir_actif, input_boolean.m02_pir_cuisine_actif, input_boolean.m02_pir_sdb_actif, input_boolean.m02_presence_chambre_actif, input_boolean.m02_presence_salon_actif
- `www/config.html` : input_boolean.m02_pir_couloir_actif, input_boolean.m02_pir_cuisine_actif, input_boolean.m02_pir_sdb_actif, input_boolean.module_m02_inactivite

### M03

```
packages/m00_modules.yaml
  └─→ input_boolean.module_m03_ecran_msg
packages/oblig_m03_ecran_msg/m03_ecran_msg.yaml
  └─→ automation.m03_reprendre_rotation_apres_redemarrage_ha
  └─→ automation.m03_rotation_afficher_message_suivant
  └─→ automation.m03_vider_la_file_a_minuit
  └─→ input_datetime.m03_affiche_depuis
  └─→ input_datetime.m03_envoi_debut
  └─→ input_datetime.m03_envoi_fin
  └─→ input_datetime.m03_message_envoi
  └─→ input_number.m03_affichage_duree
  └─→ input_number.m03_queue_max
  └─→ input_number.m03_rl_max
  └─→ input_select.m03_rl_fenetre
  └─→ input_text.m03_affiche_auteur
  └─→ input_text.m03_affiche_msg
  └─→ input_text.m03_message_auteur
  └─→ input_text.m03_message_famille
  └─→ input_text.m03_queue_auteur
  └─→ input_text.m03_queue_msg
  └─→ input_text.m03_queue_timestamps
  └─→ input_text.m03_rate_limit
  └─→ script.m03_afficher_suivant
  └─→ script.m03_envoyer
  └─→ sensor.m03_agenda_formate
  └─→ sensor.m03_bandeau_principal
  └─→ sensor.m03_texto_formate
  └─→ shell_command.m03_log_message
  └─→ timer.m03_rotation
packages/oblig_m03_ecran_msg/m03_rdv_recurrents.yaml
  └─→ automation.m03_rdv_recurrents_creer_l_evenement_du_jour
  └─→ shell_command.m03_rdv_recurrents
```

**Consomme par :**

- `dashboards/dashboard_modules.yaml` : input_boolean.module_m03_ecran_msg
- `packages/m31_photos.yaml` : shell_command.m03_rdv_recurrents
- `packages/oblig_m03_ecran_msg/m03_ecran_msg.yaml` : input_boolean.module_m03_ecran_msg
- `shell_scripts/m03_rdv_recurrents.py` : shell_command.m03_rdv_recurrents
- `www/aidant.html` : input_boolean.module_m03_ecran_msg, input_datetime.m03_affiche_depuis, input_datetime.m03_envoi_debut, input_datetime.m03_envoi_fin, input_number.m03_affichage_duree, input_number.m03_queue_max, input_number.m03_rl_max, input_select.m03_rl_fenetre (+12)
- `www/config.html` : input_boolean.module_m03_ecran_msg
- `www/kiosk.html` : sensor.m03_texto_formate, shell_command.m03_rdv_recurrents

### M04

```
packages/m00_modules.yaml
  └─→ input_boolean.module_m04_calendrier
packages/secur_m10_sos/m10_sos.yaml
  └─→ automation.m04_sos_bouton_appuye
  └─→ automation.m04_sos_reset_manuel
```

**Consomme par :**

- `www/aidant.html` : input_boolean.module_m04_calendrier
- `www/config.html` : input_boolean.module_m04_calendrier
- `www/kiosk.html` : input_boolean.module_m04_calendrier

### M10

```
packages/m00_modules.yaml
  └─→ input_boolean.module_m10_sos
packages/secur_m10_sos/m10_gestion_aidants.yaml
  └─→ input_boolean.m10_proximite_aidant_1
  └─→ input_boolean.m10_proximite_aidant_2
  └─→ input_boolean.m10_proximite_aidant_3
  └─→ input_boolean.m10_proximite_aidant_4
  └─→ input_boolean.m10_proximite_aidant_5
  └─→ input_boolean.m10_proximite_aidant_6
  └─→ input_boolean.m10_proximite_aidant_7
  └─→ input_text.m10_droits_aidants
packages/secur_m10_sos/m10_groupe_aidants.yaml
  └─→ script.m10_envoyer_alerte_moderee
  └─→ script.m10_envoyer_alerte_sos
packages/secur_m10_sos/m10_sos.yaml
  └─→ input_boolean.m10_sos_declenche
```

**Consomme par :**

- `dashboards/dashboard_modules.yaml` : input_boolean.m10_proximite_aidant_1, input_boolean.m10_proximite_aidant_2, input_boolean.m10_proximite_aidant_3, input_boolean.m10_proximite_aidant_4, input_boolean.m10_proximite_aidant_5, input_boolean.m10_proximite_aidant_6, input_boolean.m10_proximite_aidant_7, input_boolean.module_m10_sos
- `dashboards/dashboard_test_simulation.yaml` : input_boolean.m10_sos_declenche, input_boolean.module_m10_sos
- `packages/secur_m10_sos/m10_groupe_aidants.yaml` : input_boolean.m10_proximite_aidant_1, input_text.m10_droits_aidants
- `packages/secur_m10_sos/m10_sos.yaml` : input_boolean.module_m10_sos, script.m10_envoyer_alerte_sos
- `www/aidant.html` : input_text.m10_droits_aidants
- `www/calendrier.html` : input_text.m10_droits_aidants
- `www/config.html` : input_boolean.m10_proximite_aidant_1, input_boolean.m10_proximite_aidant_2, input_boolean.m10_proximite_aidant_3, input_boolean.m10_proximite_aidant_4, input_boolean.m10_proximite_aidant_5, input_boolean.m10_proximite_aidant_6, input_boolean.m10_proximite_aidant_7, input_boolean.module_m10_sos (+1)
- `www/photos.html` : input_text.m10_droits_aidants
- `www/video.html` : input_text.m10_droits_aidants

### M11

```
packages/m00_modules.yaml
  └─→ input_boolean.module_m11_capteur_lit
packages/m11_capteur_lit.yaml
  └─→ binary_sensor.m11_lit_occupe
  └─→ sensor.m11_lit_duree_occupation
```

**Consomme par :**

- `dashboards/dashboard_modules.yaml` : input_boolean.module_m11_capteur_lit
- `dashboards/dashboard_test_simulation.yaml` : input_boolean.module_m11_capteur_lit
- `www/config.html` : input_boolean.module_m11_capteur_lit

### M12

```
packages/m00_modules.yaml
  └─→ input_boolean.module_m12_cam_ia
```

**Consomme par :**

- `dashboards/dashboard_modules.yaml` : input_boolean.module_m12_cam_ia
- `www/config.html` : input_boolean.module_m12_cam_ia

### M13

```
packages/m00_modules.yaml
  └─→ input_boolean.module_m13_porte_ext
packages/m13_porte_ext.yaml
  └─→ sensor.m13_porte_ext_duree_ouverture
```

**Consomme par :**

- `dashboards/dashboard_modules.yaml` : input_boolean.module_m13_porte_ext
- `www/config.html` : input_boolean.module_m13_porte_ext

### M14

```
packages/m00_modules.yaml
  └─→ input_boolean.module_m14_fenetre
```

**Consomme par :**

- `dashboards/dashboard_modules.yaml` : input_boolean.module_m14_fenetre
- `www/config.html` : input_boolean.module_m14_fenetre

### M17

```
packages/m00_modules.yaml
  └─→ input_boolean.module_m17_lumiere_nuit
```

**Consomme par :**

- `dashboards/dashboard_modules.yaml` : input_boolean.module_m17_lumiere_nuit
- `www/config.html` : input_boolean.module_m17_lumiere_nuit

### M20

```
packages/m00_modules.yaml
  └─→ input_boolean.module_m20_medoc
packages/m20_medoc.yaml
  └─→ input_boolean.m20_medoc_couche_actif
  └─→ input_boolean.m20_medoc_matin_actif
  └─→ input_boolean.m20_medoc_midi_actif
  └─→ input_boolean.m20_medoc_soir_actif
  └─→ input_datetime.m20_medoc_couche
  └─→ input_datetime.m20_medoc_matin
  └─→ input_datetime.m20_medoc_midi
  └─→ input_datetime.m20_medoc_soir
  └─→ input_number.m20_medoc_duree_min
```

**Consomme par :**

- `dashboards/dashboard_modules.yaml` : input_boolean.module_m20_medoc
- `packages/m20_medoc.yaml` : input_boolean.module_m20_medoc
- `www/config.html` : input_boolean.m20_medoc_couche_actif, input_boolean.m20_medoc_matin_actif, input_boolean.m20_medoc_midi_actif, input_boolean.m20_medoc_soir_actif, input_boolean.module_m20_medoc, input_number.m20_medoc_duree_min
- `www/kiosk.html` : input_boolean.module_m20_medoc, input_number.m20_medoc_duree_min

### M22

```
packages/m00_modules.yaml
  └─→ input_boolean.module_m22_douche
```

**Consomme par :**

- `dashboards/dashboard_modules.yaml` : input_boolean.module_m22_douche
- `www/config.html` : input_boolean.module_m22_douche

### M30

```
packages/m00_modules.yaml
  └─→ input_boolean.module_m30_kiosk_ecran
```

**Consomme par :**

- `dashboards/dashboard_modules.yaml` : input_boolean.module_m30_kiosk_ecran
- `www/aidant.html` : input_boolean.module_m30_kiosk_ecran
- `www/config.html` : input_boolean.module_m30_kiosk_ecran
- `www/kiosk.html` : input_boolean.module_m30_kiosk_ecran

### M31

```
packages/m00_modules.yaml
  └─→ input_boolean.module_m31_kiosk_foto
packages/m31_photos.yaml
  └─→ input_number.m31_photos_intervalle_s
  └─→ input_text.m31_photos_dossier
  └─→ script.m31_lancer_diaporama
  └─→ shell_command.m31_photos_liste
  └─→ shell_command.m31_photos_supprimer
  └─→ shell_command.m31_photos_televerser_chunk
  └─→ shell_command.m31_photos_televerser_debut
  └─→ shell_command.m31_photos_televerser_fin
```

**Consomme par :**

- `dashboards/dashboard_modules.yaml` : input_boolean.module_m31_kiosk_foto
- `packages/confo_m34_television/m34_television.yaml` : script.m31_lancer_diaporama
- `packages/m31_photos.yaml` : input_boolean.module_m31_kiosk_foto
- `shell_scripts/m31_photos_liste.py` : shell_command.m31_photos_liste
- `shell_scripts/m31_photos_supprimer.py` : shell_command.m31_photos_liste
- `shell_scripts/m31_photos_televerser.py` : shell_command.m31_photos_supprimer
- `www/aidant.html` : input_boolean.module_m31_kiosk_foto
- `www/config.html` : input_boolean.module_m31_kiosk_foto
- `www/kiosk.html` : input_boolean.module_m31_kiosk_foto, input_number.m31_photos_intervalle_s, shell_command.m31_photos_liste
- `www/photos.html` : shell_command.m31_photos_liste, shell_command.m31_photos_supprimer, shell_command.m31_photos_televerser_chunk, shell_command.m31_photos_televerser_debut, shell_command.m31_photos_televerser_fin

### M32

```
packages/confo_m32_musique/m32_musique.yaml
  └─→ input_boolean.m32_creneau1_actif
  └─→ input_boolean.m32_creneau2_actif
  └─→ input_boolean.m32_creneau3_actif
  └─→ input_boolean.m32_creneau4_actif
  └─→ input_datetime.m32_creneau1_debut
  └─→ input_datetime.m32_creneau1_fin
  └─→ input_datetime.m32_creneau2_debut
  └─→ input_datetime.m32_creneau2_fin
  └─→ input_datetime.m32_creneau3_debut
  └─→ input_datetime.m32_creneau3_fin
  └─→ input_datetime.m32_creneau4_debut
  └─→ input_datetime.m32_creneau4_fin
  └─→ shell_command.m32_musique_liens
packages/m00_modules.yaml
  └─→ input_boolean.module_m32_kiosk_zic
```

**Consomme par :**

- `dashboards/dashboard_modules.yaml` : input_boolean.module_m32_kiosk_zic
- `packages/confo_m32_musique/m32_musique.yaml` : input_boolean.module_m32_kiosk_zic
- `www/aidant.html` : input_boolean.module_m32_kiosk_zic
- `www/config.html` : input_boolean.module_m32_kiosk_zic
- `www/kiosk.html` : input_boolean.module_m32_kiosk_zic, shell_command.m32_musique_liens
- `www/musique.html` : shell_command.m32_musique_liens

### M33

```
packages/m00_modules.yaml
  └─→ input_boolean.module_m33_visio
packages/m33_visio.yaml
  └─→ automation.m33_horaires_visio_par_defaut_une_seule_fois_demarrage_ha
  └─→ input_boolean.m33_appel_en_cours
  └─→ input_boolean.m33_appel_urgent
  └─→ input_boolean.m33_horaires_initialises
  └─→ input_datetime.m33_horaire_debut
  └─→ input_datetime.m33_horaire_fin
  └─→ input_text.m33_appel_par
  └─→ shell_command.m33_visio_signal_envoyer
  └─→ shell_command.m33_visio_signal_lire
  └─→ shell_command.m33_visio_signal_purger
```

**Consomme par :**

- `dashboards/dashboard_modules.yaml` : input_boolean.module_m33_visio
- `packages/m33_visio.yaml` : input_boolean.module_m33_visio
- `www/aidant.html` : input_boolean.m33_appel_en_cours, input_boolean.m33_appel_urgent, input_boolean.module_m33_visio, input_datetime.m33_horaire_debut, input_datetime.m33_horaire_fin, input_text.m33_appel_par, shell_command.m33_visio_signal_envoyer, shell_command.m33_visio_signal_lire (+1)
- `www/config.html` : input_boolean.module_m33_visio, input_datetime.m33_horaire_debut, input_datetime.m33_horaire_fin
- `www/kiosk.html` : input_boolean.m33_appel_en_cours, input_boolean.m33_appel_urgent, input_datetime.m33_horaire_debut, input_datetime.m33_horaire_fin, input_text.m33_appel_par, shell_command.m33_visio_signal_envoyer, shell_command.m33_visio_signal_lire

### M34

```
packages/confo_m34_television/m34_liens_youtube.yaml
  └─→ automation.m34_marquer_video_vue_5_min_avant_sa_fin_reelle
  └─→ input_boolean.module_m34_liens_youtube
  └─→ sensor.m34_video_embed
  └─→ shell_command.m34_liens_youtube
packages/confo_m34_television/m34_television.yaml
  └─→ automation.m34_horaires_par_defaut_une_seule_fois_demarrage_ha
  └─→ automation.m34_rechargement_immediat_si_chaine_changee_en_session_active
  └─→ input_boolean.m34_horaires_initialises
  └─→ input_boolean.m34_session1_actif
  └─→ input_boolean.m34_session2_actif
  └─→ input_boolean.m34_session3_actif
  └─→ input_boolean.m34_session4_actif
  └─→ input_button.m34_session1_ok
  └─→ input_button.m34_session2_ok
  └─→ input_button.m34_session3_ok
  └─→ input_button.m34_session4_ok
  └─→ input_datetime.m34_session1_debut
  └─→ input_datetime.m34_session1_fin
  └─→ input_datetime.m34_session1_marquer_vu_a
  └─→ input_datetime.m34_session2_debut
  └─→ input_datetime.m34_session2_fin
  └─→ input_datetime.m34_session2_marquer_vu_a
  └─→ input_datetime.m34_session3_debut
  └─→ input_datetime.m34_session3_fin
  └─→ input_datetime.m34_session3_marquer_vu_a
  └─→ input_datetime.m34_session4_debut
  └─→ input_datetime.m34_session4_fin
  └─→ input_datetime.m34_session4_marquer_vu_a
  └─→ input_select.m34_session1_chaine
  └─→ input_select.m34_session2_chaine
  └─→ input_select.m34_session3_chaine
  └─→ input_select.m34_session4_chaine
  └─→ input_text.m34_session1_youtube_url
  └─→ input_text.m34_session2_youtube_url
  └─→ input_text.m34_session3_youtube_url
  └─→ input_text.m34_session4_youtube_url
  └─→ input_text.m34_session_affichee
  └─→ script.m34_lancer_session
  └─→ sensor.m34_etat_global
  └─→ sensor.m34_session1_fenetre
  └─→ sensor.m34_session2_fenetre
  └─→ sensor.m34_session3_fenetre
  └─→ sensor.m34_session4_fenetre
packages/m00_modules.yaml
  └─→ input_boolean.module_m34_television
```

**Consomme par :**

- `dashboards/dashboard_modules.yaml` : input_boolean.m34_session1_actif, input_boolean.m34_session2_actif, input_boolean.m34_session3_actif, input_boolean.module_m34_television, input_datetime.m34_session1_debut, input_datetime.m34_session1_fin, input_datetime.m34_session2_debut, input_datetime.m34_session2_fin (+9)
- `packages/confo_m34_television/m34_liens_youtube.yaml` : input_datetime.m34_session1_marquer_vu_a, input_datetime.m34_session2_marquer_vu_a, input_datetime.m34_session3_marquer_vu_a, input_datetime.m34_session4_marquer_vu_a, script.m34_lancer_session
- `packages/confo_m34_television/m34_television.yaml` : input_boolean.module_m34_liens_youtube, input_boolean.module_m34_television, shell_command.m34_liens_youtube
- `packages/m31_photos.yaml` : shell_command.m34_liens_youtube
- `shell_scripts/m32_musique_liens.py` : shell_command.m34_liens_youtube
- `shell_scripts/m34_liens_youtube.py` : shell_command.m34_liens_youtube
- `www/aidant.html` : input_boolean.module_m34_television
- `www/config.html` : input_boolean.m34_session1_actif, input_boolean.m34_session2_actif, input_boolean.m34_session3_actif, input_boolean.m34_session4_actif, input_boolean.module_m34_television, script.m34_lancer_session

### M40

```
packages/m00_modules.yaml
  └─→ input_boolean.module_m40_chauffage
```

**Consomme par :**

- `www/config.html` : input_boolean.module_m40_chauffage

### SIM

```
packages/m00_simulation.yaml
  └─→ automation.simu_reset_auto_bouton_sos_apres_appui
  └─→ input_boolean.sim_lit_occupe
  └─→ input_boolean.sim_pir_couloir
  └─→ input_boolean.sim_pir_cuisine
  └─→ input_boolean.sim_pir_sdb
  └─→ input_boolean.sim_presence_chambre
  └─→ input_boolean.sim_presence_salon
  └─→ input_boolean.sim_snzb06p_presence
  └─→ input_boolean.sim_sos_bouton
packages/m00_simulation_sensors.yaml
  └─→ input_boolean.sim_porte_ext_contact
  └─→ input_number.sim_hygro_salon
  └─→ input_number.sim_temp_chambre
  └─→ input_number.sim_temp_salon
```

**Consomme par :**

- `dashboards/dashboard_test_simulation.yaml` : input_boolean.sim_lit_occupe, input_boolean.sim_pir_couloir, input_boolean.sim_pir_cuisine, input_boolean.sim_pir_sdb, input_boolean.sim_porte_ext_contact, input_boolean.sim_presence_chambre, input_boolean.sim_presence_salon, input_boolean.sim_sos_bouton (+3)
- `packages/m02_inactivite.yaml` : input_boolean.sim_pir_couloir, input_boolean.sim_pir_cuisine, input_boolean.sim_pir_sdb, input_boolean.sim_presence_chambre
- `packages/m11_capteur_lit.yaml` : input_boolean.sim_lit_occupe
- `packages/secur_m10_sos/m10_sos.yaml` : input_boolean.sim_sos_bouton
- `www/aidant.html` : input_number.sim_temp_chambre, input_number.sim_temp_salon
