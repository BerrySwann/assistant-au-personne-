# ENTITES — Assistant au personne (instance .241)
*Genere automatiquement par `sync_dependances.py` — 2026-08-29*

> Source : `Z:\packages`, `Z:\dashboards`, `Z:\www` (JS), `Z:\shell_scripts`, `Z:\automations.yaml`
> Colonne **Live** : presente (oui/non) sur l'instance 10.32.154.241 au moment de la generation.
> Colonne **Definie dans** : fichier YAML qui la cree. `(natif)` = creee par HA/Z2M/appareil.

**Total entites definies dans les YAML du projet : 207**
- Entites d'etat verifiables : 194
- Presentes sur l'instance : 184
- **Fantomes** (definies mais absentes de l'instance) : 10
- Total entites sur l'instance : 271

## (natif/autre) — 10 entites

| Entite | Definie dans | Consommee par | Live |
|:-------|:-------------|:--------------|:----:|
| `automation.confo_m34_bouton_ok_relancer_la_session_avec_la_chaine_choisie` | packages/confo_m34_television/m34_television.yaml | **ORPHELINE** | oui |
| `automation.confo_m34_mise_a_jour_hebdo_des_liens_youtube` | packages/confo_m34_television/m34_liens_youtube.yaml | **ORPHELINE** | oui |
| `automation.confo_m34_retour_photos_si_module_tv_desactive` | packages/confo_m34_television/m34_television.yaml | **ORPHELINE** | oui |
| `automation.confo_m34_verifier_les_sessions_tv_toutes_les_minutes` | packages/confo_m34_television/m34_television.yaml | **ORPHELINE** | oui |
| `binary_sensor.snzb04p_porte_ext_contact` | packages/m00_simulation_sensors.yaml | packages/m13_porte_ext.yaml, www/aidant.html | oui |
| `input_boolean.module_dashboard_fam` | packages/m00_modules.yaml | dashboards/dashboard_modules.yaml, www/config.html | oui |
| `input_boolean.module_msg_famille` | packages/m00_modules.yaml | dashboards/dashboard_modules.yaml, www/config.html | oui |
| `sensor.snzb02d_chambre_temperature` | packages/m00_simulation_sensors.yaml | packages/m01_temp_hygro.yaml, www/aidant.html | oui |
| `sensor.snzb02d_salon_humidity` | packages/m00_simulation_sensors.yaml | packages/m01_temp_hygro.yaml | oui |
| `sensor.snzb02d_salon_temperature` | packages/m00_simulation_sensors.yaml | packages/m01_temp_hygro.yaml, www/aidant.html | oui |

## M01 — 10 entites

| Entite | Definie dans | Consommee par | Live |
|:-------|:-------------|:--------------|:----:|
| `input_boolean.module_m01_temp_hygro` | packages/m00_modules.yaml | dashboards/dashboard_modules.yaml, packages/m01_temp_hygro.yaml, www/aidant.html, www/config.html | oui |
| `sensor.m01_alerte_humidite` | packages/m01_temp_hygro.yaml | **ORPHELINE** | oui |
| `sensor.m01_alerte_temperature` | packages/m01_temp_hygro.yaml | **ORPHELINE** | oui |
| `sensor.m01_hygro_salon_avg_24h` | packages/m01_temp_hygro.yaml | **ORPHELINE** | **non** |
| `sensor.m01_resume_temp_chambre` | packages/m01_temp_hygro.yaml | **ORPHELINE** | oui |
| `sensor.m01_resume_temp_salon` | packages/m01_temp_hygro.yaml | **ORPHELINE** | oui |
| `sensor.m01_temp_chambre_max_24h` | packages/m01_temp_hygro.yaml | **ORPHELINE** | oui |
| `sensor.m01_temp_chambre_min_24h` | packages/m01_temp_hygro.yaml | **ORPHELINE** | oui |
| `sensor.m01_temp_salon_max_24h` | packages/m01_temp_hygro.yaml | **ORPHELINE** | oui |
| `sensor.m01_temp_salon_min_24h` | packages/m01_temp_hygro.yaml | **ORPHELINE** | oui |

## M02 — 32 entites

| Entite | Definie dans | Consommee par | Live |
|:-------|:-------------|:--------------|:----:|
| `automation.m02_activite_detectee_reset_horodatage` | packages/m02_inactivite.yaml | **ORPHELINE** | oui |
| `automation.m02_check_inactivite_toutes_les_5_min` | packages/m02_inactivite.yaml | **ORPHELINE** | oui |
| `automation.m02_fin_apres_midi_apprentissage_seuil` | packages/m02_inactivite.yaml | **ORPHELINE** | oui |
| `automation.m02_fin_matin_apprentissage_seuil` | packages/m02_inactivite.yaml | **ORPHELINE** | oui |
| `automation.m02_fin_nuit_apprentissage_seuil` | packages/m02_inactivite.yaml | **ORPHELINE** | oui |
| `automation.m02_fin_sieste_apprentissage_seuil` | packages/m02_inactivite.yaml | **ORPHELINE** | oui |
| `automation.m02_fin_soiree_apprentissage_seuil` | packages/m02_inactivite.yaml | **ORPHELINE** | oui |
| `binary_sensor.m02_activite_detectee` | packages/m02_inactivite.yaml | dashboards/dashboard_test_simulation.yaml | oui |
| `input_boolean.m02_absence_nuit_anormale` | packages/m02_inactivite.yaml | dashboards/dashboard_test_simulation.yaml | oui |
| `input_boolean.m02_alerte_active` | packages/m02_inactivite.yaml | dashboards/dashboard_test_simulation.yaml | oui |
| `input_boolean.m02_pir_couloir_actif` | packages/m00_modules.yaml | www/appairage.html, www/config.html | oui |
| `input_boolean.m02_pir_cuisine_actif` | packages/m00_modules.yaml | www/appairage.html, www/config.html | oui |
| `input_boolean.m02_pir_sdb_actif` | packages/m00_modules.yaml | www/appairage.html, www/config.html | oui |
| `input_boolean.m02_presence_chambre_actif` | packages/m00_modules.yaml | www/appairage.html | oui |
| `input_boolean.m02_presence_salon_actif` | packages/m00_modules.yaml | www/appairage.html | oui |
| `input_boolean.module_m02_inactivite` | packages/m00_modules.yaml | dashboards/dashboard_modules.yaml, dashboards/dashboard_test_simulation.yaml, packages/m02_inactivite.yaml, www/config.html | oui |
| `input_datetime.m02_derniere_activite` | packages/m02_inactivite.yaml | dashboards/dashboard_test_simulation.yaml | oui |
| `input_number.m02_ema_alpha` | packages/m02_inactivite.yaml | **ORPHELINE** | oui |
| `input_number.m02_facteur_alerte` | packages/m02_inactivite.yaml | dashboards/dashboard_test_simulation.yaml | oui |
| `input_number.m02_facteur_apprentissage` | packages/m02_inactivite.yaml | **ORPHELINE** | oui |
| `input_number.m02_jours_apprentissage` | packages/m02_inactivite.yaml | dashboards/dashboard_test_simulation.yaml | oui |
| `input_number.m02_obs_gap` | packages/m02_inactivite.yaml | dashboards/dashboard_test_simulation.yaml | oui |
| `input_number.m02_seuil_aprem` | packages/m02_inactivite.yaml | dashboards/dashboard_test_simulation.yaml | oui |
| `input_number.m02_seuil_matin` | packages/m02_inactivite.yaml | dashboards/dashboard_test_simulation.yaml | oui |
| `input_number.m02_seuil_nuit` | packages/m02_inactivite.yaml | dashboards/dashboard_test_simulation.yaml | oui |
| `input_number.m02_seuil_sieste` | packages/m02_inactivite.yaml | dashboards/dashboard_test_simulation.yaml | oui |
| `input_number.m02_seuil_soir` | packages/m02_inactivite.yaml | dashboards/dashboard_test_simulation.yaml | oui |
| `sensor.m02_inactivite_minutes` | packages/m02_inactivite.yaml | dashboards/dashboard_test_simulation.yaml | oui |
| `sensor.m02_seuil_alerte_effectif` | packages/m02_inactivite.yaml | dashboards/dashboard_test_simulation.yaml | oui |
| `sensor.m02_seuil_tranche_actuelle` | packages/m02_inactivite.yaml | dashboards/dashboard_test_simulation.yaml | oui |
| `sensor.m02_tranche_horaire` | packages/m02_inactivite.yaml | dashboards/dashboard_test_simulation.yaml | oui |
| `shell_command.m02_log_presence_salon` | packages/m02_log_presence.yaml | automations.yaml | n/a |

## M03 — 29 entites

| Entite | Definie dans | Consommee par | Live |
|:-------|:-------------|:--------------|:----:|
| `automation.m03_rdv_recurrents_creer_l_evenement_du_jour` | packages/oblig_m03_ecran_msg/m03_rdv_recurrents.yaml | **ORPHELINE** | oui |
| `automation.m03_reprendre_rotation_apres_redemarrage_ha` | packages/oblig_m03_ecran_msg/m03_ecran_msg.yaml | **ORPHELINE** | oui |
| `automation.m03_rotation_afficher_message_suivant` | packages/oblig_m03_ecran_msg/m03_ecran_msg.yaml | **ORPHELINE** | oui |
| `automation.m03_vider_la_file_a_minuit` | packages/oblig_m03_ecran_msg/m03_ecran_msg.yaml | **ORPHELINE** | oui |
| `input_boolean.module_m03_ecran_msg` | packages/m00_modules.yaml | dashboards/dashboard_modules.yaml, packages/oblig_m03_ecran_msg/m03_ecran_msg.yaml, www/aidant.html, www/config.html | oui |
| `input_datetime.m03_affiche_depuis` | packages/oblig_m03_ecran_msg/m03_ecran_msg.yaml | www/aidant.html | oui |
| `input_datetime.m03_envoi_debut` | packages/oblig_m03_ecran_msg/m03_ecran_msg.yaml | www/aidant.html | oui |
| `input_datetime.m03_envoi_fin` | packages/oblig_m03_ecran_msg/m03_ecran_msg.yaml | www/aidant.html | oui |
| `input_datetime.m03_message_envoi` | packages/oblig_m03_ecran_msg/m03_ecran_msg.yaml | **ORPHELINE** | oui |
| `input_number.m03_affichage_duree` | packages/oblig_m03_ecran_msg/m03_ecran_msg.yaml | www/aidant.html | oui |
| `input_number.m03_queue_max` | packages/oblig_m03_ecran_msg/m03_ecran_msg.yaml | www/aidant.html | oui |
| `input_number.m03_rl_max` | packages/oblig_m03_ecran_msg/m03_ecran_msg.yaml | www/aidant.html | oui |
| `input_select.m03_rl_fenetre` | packages/oblig_m03_ecran_msg/m03_ecran_msg.yaml | www/aidant.html | oui |
| `input_text.m03_affiche_auteur` | packages/oblig_m03_ecran_msg/m03_ecran_msg.yaml | www/aidant.html | oui |
| `input_text.m03_affiche_msg` | packages/oblig_m03_ecran_msg/m03_ecran_msg.yaml | www/aidant.html | oui |
| `input_text.m03_message_auteur` | packages/oblig_m03_ecran_msg/m03_ecran_msg.yaml | **ORPHELINE** | oui |
| `input_text.m03_message_famille` | packages/oblig_m03_ecran_msg/m03_ecran_msg.yaml | www/aidant.html | oui |
| `input_text.m03_queue_auteur` | packages/oblig_m03_ecran_msg/m03_ecran_msg.yaml | www/aidant.html | oui |
| `input_text.m03_queue_msg` | packages/oblig_m03_ecran_msg/m03_ecran_msg.yaml | www/aidant.html | oui |
| `input_text.m03_queue_timestamps` | packages/oblig_m03_ecran_msg/m03_ecran_msg.yaml | www/aidant.html | oui |
| `input_text.m03_rate_limit` | packages/oblig_m03_ecran_msg/m03_ecran_msg.yaml | www/aidant.html | oui |
| `script.m03_afficher_suivant` | packages/oblig_m03_ecran_msg/m03_ecran_msg.yaml | **ORPHELINE** | oui |
| `script.m03_envoyer` | packages/oblig_m03_ecran_msg/m03_ecran_msg.yaml | www/aidant.html | oui |
| `sensor.m03_agenda_formate` | packages/oblig_m03_ecran_msg/m03_ecran_msg.yaml | **ORPHELINE** | oui |
| `sensor.m03_bandeau_principal` | packages/oblig_m03_ecran_msg/m03_ecran_msg.yaml | www/aidant.html | oui |
| `sensor.m03_texto_formate` | packages/oblig_m03_ecran_msg/m03_ecran_msg.yaml | www/aidant.html, www/kiosk.html | oui |
| `shell_command.m03_log_message` | packages/oblig_m03_ecran_msg/m03_ecran_msg.yaml | **ORPHELINE** | n/a |
| `shell_command.m03_rdv_recurrents` | packages/oblig_m03_ecran_msg/m03_rdv_recurrents.yaml | packages/m31_photos.yaml, shell_scripts/m03_rdv_recurrents.py, www/aidant.html, www/kiosk.html | n/a |
| `timer.m03_rotation` | packages/oblig_m03_ecran_msg/m03_ecran_msg.yaml | www/aidant.html | oui |

## M04 — 3 entites

| Entite | Definie dans | Consommee par | Live |
|:-------|:-------------|:--------------|:----:|
| `automation.m04_sos_bouton_appuye` | packages/secur_m10_sos/m10_sos.yaml | **ORPHELINE** | oui |
| `automation.m04_sos_reset_manuel` | packages/secur_m10_sos/m10_sos.yaml | **ORPHELINE** | oui |
| `input_boolean.module_m04_calendrier` | packages/m00_modules.yaml | www/aidant.html, www/config.html, www/kiosk.html | oui |

## M10 — 12 entites

| Entite | Definie dans | Consommee par | Live |
|:-------|:-------------|:--------------|:----:|
| `input_boolean.m10_proximite_aidant_1` | packages/secur_m10_sos/m10_gestion_aidants.yaml | dashboards/dashboard_modules.yaml, packages/secur_m10_sos/m10_groupe_aidants.yaml, www/config.html | oui |
| `input_boolean.m10_proximite_aidant_2` | packages/secur_m10_sos/m10_gestion_aidants.yaml | dashboards/dashboard_modules.yaml, www/config.html | oui |
| `input_boolean.m10_proximite_aidant_3` | packages/secur_m10_sos/m10_gestion_aidants.yaml | dashboards/dashboard_modules.yaml, www/config.html | oui |
| `input_boolean.m10_proximite_aidant_4` | packages/secur_m10_sos/m10_gestion_aidants.yaml | dashboards/dashboard_modules.yaml, www/config.html | oui |
| `input_boolean.m10_proximite_aidant_5` | packages/secur_m10_sos/m10_gestion_aidants.yaml | dashboards/dashboard_modules.yaml, www/config.html | oui |
| `input_boolean.m10_proximite_aidant_6` | packages/secur_m10_sos/m10_gestion_aidants.yaml | dashboards/dashboard_modules.yaml, www/config.html | oui |
| `input_boolean.m10_proximite_aidant_7` | packages/secur_m10_sos/m10_gestion_aidants.yaml | dashboards/dashboard_modules.yaml, www/config.html | oui |
| `input_boolean.m10_sos_declenche` | packages/secur_m10_sos/m10_sos.yaml | dashboards/dashboard_test_simulation.yaml | oui |
| `input_boolean.module_m10_sos` | packages/m00_modules.yaml | dashboards/dashboard_modules.yaml, dashboards/dashboard_test_simulation.yaml, packages/secur_m10_sos/m10_sos.yaml, www/config.html | oui |
| `input_text.m10_droits_aidants` | packages/secur_m10_sos/m10_gestion_aidants.yaml | packages/secur_m10_sos/m10_groupe_aidants.yaml, www/aidant.html, www/calendrier.html, www/config.html (+2) | oui |
| `script.m10_envoyer_alerte_moderee` | packages/secur_m10_sos/m10_groupe_aidants.yaml | **ORPHELINE** | oui |
| `script.m10_envoyer_alerte_sos` | packages/secur_m10_sos/m10_groupe_aidants.yaml | packages/secur_m10_sos/m10_sos.yaml | oui |

## M11 — 3 entites

| Entite | Definie dans | Consommee par | Live |
|:-------|:-------------|:--------------|:----:|
| `binary_sensor.m11_lit_occupe` | packages/m11_capteur_lit.yaml | **ORPHELINE** | **non** |
| `input_boolean.module_m11_capteur_lit` | packages/m00_modules.yaml | dashboards/dashboard_modules.yaml, dashboards/dashboard_test_simulation.yaml, www/config.html | oui |
| `sensor.m11_lit_duree_occupation` | packages/m11_capteur_lit.yaml | **ORPHELINE** | **non** |

## M12 — 1 entites

| Entite | Definie dans | Consommee par | Live |
|:-------|:-------------|:--------------|:----:|
| `input_boolean.module_m12_cam_ia` | packages/m00_modules.yaml | dashboards/dashboard_modules.yaml, www/config.html | oui |

## M13 — 2 entites

| Entite | Definie dans | Consommee par | Live |
|:-------|:-------------|:--------------|:----:|
| `input_boolean.module_m13_porte_ext` | packages/m00_modules.yaml | dashboards/dashboard_modules.yaml, www/config.html | oui |
| `sensor.m13_porte_ext_duree_ouverture` | packages/m13_porte_ext.yaml | **ORPHELINE** | **non** |

## M14 — 1 entites

| Entite | Definie dans | Consommee par | Live |
|:-------|:-------------|:--------------|:----:|
| `input_boolean.module_m14_fenetre` | packages/m00_modules.yaml | dashboards/dashboard_modules.yaml, www/config.html | oui |

## M17 — 1 entites

| Entite | Definie dans | Consommee par | Live |
|:-------|:-------------|:--------------|:----:|
| `input_boolean.module_m17_lumiere_nuit` | packages/m00_modules.yaml | dashboards/dashboard_modules.yaml, www/config.html | oui |

## M20 — 10 entites

| Entite | Definie dans | Consommee par | Live |
|:-------|:-------------|:--------------|:----:|
| `input_boolean.m20_medoc_couche_actif` | packages/m20_medoc.yaml | www/config.html | oui |
| `input_boolean.m20_medoc_matin_actif` | packages/m20_medoc.yaml | www/config.html | oui |
| `input_boolean.m20_medoc_midi_actif` | packages/m20_medoc.yaml | www/config.html | oui |
| `input_boolean.m20_medoc_soir_actif` | packages/m20_medoc.yaml | www/config.html | oui |
| `input_boolean.module_m20_medoc` | packages/m00_modules.yaml | dashboards/dashboard_modules.yaml, packages/m20_medoc.yaml, www/config.html, www/kiosk.html | oui |
| `input_datetime.m20_medoc_couche` | packages/m20_medoc.yaml | dynamique (www/config.html) | oui |
| `input_datetime.m20_medoc_matin` | packages/m20_medoc.yaml | dynamique (www/config.html) | oui |
| `input_datetime.m20_medoc_midi` | packages/m20_medoc.yaml | dynamique (www/config.html) | oui |
| `input_datetime.m20_medoc_soir` | packages/m20_medoc.yaml | dynamique (www/config.html) | oui |
| `input_number.m20_medoc_duree_min` | packages/m20_medoc.yaml | www/config.html, www/kiosk.html | oui |

## M22 — 1 entites

| Entite | Definie dans | Consommee par | Live |
|:-------|:-------------|:--------------|:----:|
| `input_boolean.module_m22_douche` | packages/m00_modules.yaml | dashboards/dashboard_modules.yaml, www/config.html | oui |

## M30 — 1 entites

| Entite | Definie dans | Consommee par | Live |
|:-------|:-------------|:--------------|:----:|
| `input_boolean.module_m30_kiosk_ecran` | packages/m00_modules.yaml | dashboards/dashboard_modules.yaml, www/aidant.html, www/config.html, www/kiosk.html | oui |

## M31 — 9 entites

| Entite | Definie dans | Consommee par | Live |
|:-------|:-------------|:--------------|:----:|
| `input_boolean.module_m31_kiosk_foto` | packages/m00_modules.yaml | dashboards/dashboard_modules.yaml, packages/m31_photos.yaml, www/aidant.html, www/config.html (+1) | oui |
| `input_number.m31_photos_intervalle_s` | packages/m31_photos.yaml | www/kiosk.html | oui |
| `input_text.m31_photos_dossier` | packages/m31_photos.yaml | **ORPHELINE** | oui |
| `script.m31_lancer_diaporama` | packages/m31_photos.yaml | packages/confo_m34_television/m34_television.yaml | oui |
| `shell_command.m31_photos_liste` | packages/m31_photos.yaml | shell_scripts/m31_photos_liste.py, shell_scripts/m31_photos_supprimer.py, www/kiosk.html, www/photos.html | n/a |
| `shell_command.m31_photos_supprimer` | packages/m31_photos.yaml | shell_scripts/m31_photos_televerser.py, www/photos.html | n/a |
| `shell_command.m31_photos_televerser_chunk` | packages/m31_photos.yaml | www/photos.html | n/a |
| `shell_command.m31_photos_televerser_debut` | packages/m31_photos.yaml | www/photos.html | n/a |
| `shell_command.m31_photos_televerser_fin` | packages/m31_photos.yaml | www/photos.html | n/a |

## M32 — 14 entites

| Entite | Definie dans | Consommee par | Live |
|:-------|:-------------|:--------------|:----:|
| `input_boolean.m32_creneau1_actif` | packages/confo_m32_musique/m32_musique.yaml | dynamique (www/kiosk.html) | oui |
| `input_boolean.m32_creneau2_actif` | packages/confo_m32_musique/m32_musique.yaml | dynamique (www/kiosk.html) | oui |
| `input_boolean.m32_creneau3_actif` | packages/confo_m32_musique/m32_musique.yaml | dynamique (www/kiosk.html) | oui |
| `input_boolean.m32_creneau4_actif` | packages/confo_m32_musique/m32_musique.yaml | dynamique (www/kiosk.html) | oui |
| `input_boolean.module_m32_kiosk_zic` | packages/m00_modules.yaml | dashboards/dashboard_modules.yaml, packages/confo_m32_musique/m32_musique.yaml, www/aidant.html, www/config.html (+1) | oui |
| `input_datetime.m32_creneau1_debut` | packages/confo_m32_musique/m32_musique.yaml | dynamique (www/kiosk.html) | oui |
| `input_datetime.m32_creneau1_fin` | packages/confo_m32_musique/m32_musique.yaml | dynamique (www/kiosk.html) | oui |
| `input_datetime.m32_creneau2_debut` | packages/confo_m32_musique/m32_musique.yaml | dynamique (www/kiosk.html) | oui |
| `input_datetime.m32_creneau2_fin` | packages/confo_m32_musique/m32_musique.yaml | dynamique (www/kiosk.html) | oui |
| `input_datetime.m32_creneau3_debut` | packages/confo_m32_musique/m32_musique.yaml | dynamique (www/kiosk.html) | oui |
| `input_datetime.m32_creneau3_fin` | packages/confo_m32_musique/m32_musique.yaml | dynamique (www/kiosk.html) | oui |
| `input_datetime.m32_creneau4_debut` | packages/confo_m32_musique/m32_musique.yaml | dynamique (www/kiosk.html) | oui |
| `input_datetime.m32_creneau4_fin` | packages/confo_m32_musique/m32_musique.yaml | dynamique (www/kiosk.html) | oui |
| `shell_command.m32_musique_liens` | packages/confo_m32_musique/m32_musique.yaml | www/kiosk.html, www/musique.html | n/a |

## M33 — 11 entites

| Entite | Definie dans | Consommee par | Live |
|:-------|:-------------|:--------------|:----:|
| `automation.m33_horaires_visio_par_defaut_une_seule_fois_demarrage_ha` | packages/m33_visio.yaml | **ORPHELINE** | oui |
| `input_boolean.m33_appel_en_cours` | packages/m33_visio.yaml | www/aidant.html, www/kiosk.html | oui |
| `input_boolean.m33_appel_urgent` | packages/m33_visio.yaml | www/aidant.html, www/kiosk.html | oui |
| `input_boolean.m33_horaires_initialises` | packages/m33_visio.yaml | **ORPHELINE** | oui |
| `input_boolean.module_m33_visio` | packages/m00_modules.yaml | dashboards/dashboard_modules.yaml, packages/m33_visio.yaml, www/aidant.html, www/config.html | oui |
| `input_datetime.m33_horaire_debut` | packages/m33_visio.yaml | www/aidant.html, www/config.html, www/kiosk.html | oui |
| `input_datetime.m33_horaire_fin` | packages/m33_visio.yaml | www/aidant.html, www/config.html, www/kiosk.html | oui |
| `input_text.m33_appel_par` | packages/m33_visio.yaml | www/aidant.html, www/kiosk.html | oui |
| `shell_command.m33_visio_signal_envoyer` | packages/m33_visio.yaml | www/aidant.html, www/kiosk.html | n/a |
| `shell_command.m33_visio_signal_lire` | packages/m33_visio.yaml | www/aidant.html, www/kiosk.html | n/a |
| `shell_command.m33_visio_signal_purger` | packages/m33_visio.yaml | www/aidant.html | n/a |

## M34 — 43 entites

| Entite | Definie dans | Consommee par | Live |
|:-------|:-------------|:--------------|:----:|
| `automation.m34_horaires_par_defaut_une_seule_fois_demarrage_ha` | packages/confo_m34_television/m34_television.yaml | **ORPHELINE** | oui |
| `automation.m34_marquer_video_vue_5_min_avant_sa_fin_reelle` | packages/confo_m34_television/m34_liens_youtube.yaml | **ORPHELINE** | oui |
| `automation.m34_rechargement_immediat_si_chaine_changee_en_session_active` | packages/confo_m34_television/m34_television.yaml | **ORPHELINE** | oui |
| `input_boolean.m34_horaires_initialises` | packages/confo_m34_television/m34_television.yaml | **ORPHELINE** | oui |
| `input_boolean.m34_session1_actif` | packages/confo_m34_television/m34_television.yaml | dashboards/dashboard_modules.yaml, www/config.html | oui |
| `input_boolean.m34_session2_actif` | packages/confo_m34_television/m34_television.yaml | dashboards/dashboard_modules.yaml, www/config.html | oui |
| `input_boolean.m34_session3_actif` | packages/confo_m34_television/m34_television.yaml | dashboards/dashboard_modules.yaml, www/config.html | oui |
| `input_boolean.m34_session4_actif` | packages/confo_m34_television/m34_television.yaml | www/config.html | oui |
| `input_boolean.module_m34_liens_youtube` | packages/confo_m34_television/m34_liens_youtube.yaml | packages/confo_m34_television/m34_television.yaml | oui |
| `input_boolean.module_m34_television` | packages/m00_modules.yaml | dashboards/dashboard_modules.yaml, packages/confo_m34_television/m34_television.yaml, www/aidant.html, www/config.html | oui |
| `input_button.m34_session1_ok` | packages/confo_m34_television/m34_television.yaml | **ORPHELINE** | oui |
| `input_button.m34_session2_ok` | packages/confo_m34_television/m34_television.yaml | **ORPHELINE** | oui |
| `input_button.m34_session3_ok` | packages/confo_m34_television/m34_television.yaml | **ORPHELINE** | oui |
| `input_button.m34_session4_ok` | packages/confo_m34_television/m34_television.yaml | **ORPHELINE** | oui |
| `input_datetime.m34_session1_debut` | packages/confo_m34_television/m34_television.yaml | dashboards/dashboard_modules.yaml | oui |
| `input_datetime.m34_session1_fin` | packages/confo_m34_television/m34_television.yaml | dashboards/dashboard_modules.yaml | oui |
| `input_datetime.m34_session1_marquer_vu_a` | packages/confo_m34_television/m34_television.yaml | packages/confo_m34_television/m34_liens_youtube.yaml | oui |
| `input_datetime.m34_session2_debut` | packages/confo_m34_television/m34_television.yaml | dashboards/dashboard_modules.yaml | oui |
| `input_datetime.m34_session2_fin` | packages/confo_m34_television/m34_television.yaml | dashboards/dashboard_modules.yaml | oui |
| `input_datetime.m34_session2_marquer_vu_a` | packages/confo_m34_television/m34_television.yaml | packages/confo_m34_television/m34_liens_youtube.yaml | oui |
| `input_datetime.m34_session3_debut` | packages/confo_m34_television/m34_television.yaml | dashboards/dashboard_modules.yaml | oui |
| `input_datetime.m34_session3_fin` | packages/confo_m34_television/m34_television.yaml | dashboards/dashboard_modules.yaml | oui |
| `input_datetime.m34_session3_marquer_vu_a` | packages/confo_m34_television/m34_television.yaml | packages/confo_m34_television/m34_liens_youtube.yaml | oui |
| `input_datetime.m34_session4_debut` | packages/confo_m34_television/m34_television.yaml | dynamique (www/config.html) | oui |
| `input_datetime.m34_session4_fin` | packages/confo_m34_television/m34_television.yaml | dynamique (www/config.html) | oui |
| `input_datetime.m34_session4_marquer_vu_a` | packages/confo_m34_television/m34_television.yaml | packages/confo_m34_television/m34_liens_youtube.yaml | oui |
| `input_select.m34_session1_chaine` | packages/confo_m34_television/m34_television.yaml | dashboards/dashboard_modules.yaml | oui |
| `input_select.m34_session2_chaine` | packages/confo_m34_television/m34_television.yaml | dashboards/dashboard_modules.yaml | oui |
| `input_select.m34_session3_chaine` | packages/confo_m34_television/m34_television.yaml | dashboards/dashboard_modules.yaml | oui |
| `input_select.m34_session4_chaine` | packages/confo_m34_television/m34_television.yaml | dynamique (www/config.html) | oui |
| `input_text.m34_session1_youtube_url` | packages/confo_m34_television/m34_television.yaml | dashboards/dashboard_modules.yaml | oui |
| `input_text.m34_session2_youtube_url` | packages/confo_m34_television/m34_television.yaml | dashboards/dashboard_modules.yaml | oui |
| `input_text.m34_session3_youtube_url` | packages/confo_m34_television/m34_television.yaml | dashboards/dashboard_modules.yaml | oui |
| `input_text.m34_session4_youtube_url` | packages/confo_m34_television/m34_television.yaml | dynamique (www/config.html) | oui |
| `input_text.m34_session_affichee` | packages/confo_m34_television/m34_television.yaml | dynamique (www/config.html) | oui |
| `script.m34_lancer_session` | packages/confo_m34_television/m34_television.yaml | dashboards/dashboard_modules.yaml, packages/confo_m34_television/m34_liens_youtube.yaml, www/config.html | oui |
| `sensor.m34_etat_global` | packages/confo_m34_television/m34_television.yaml | **ORPHELINE** | **non** |
| `sensor.m34_session1_fenetre` | packages/confo_m34_television/m34_television.yaml | **ORPHELINE** | **non** |
| `sensor.m34_session2_fenetre` | packages/confo_m34_television/m34_television.yaml | **ORPHELINE** | **non** |
| `sensor.m34_session3_fenetre` | packages/confo_m34_television/m34_television.yaml | **ORPHELINE** | **non** |
| `sensor.m34_session4_fenetre` | packages/confo_m34_television/m34_television.yaml | **ORPHELINE** | **non** |
| `sensor.m34_video_embed` | packages/confo_m34_television/m34_liens_youtube.yaml | **ORPHELINE** | **non** |
| `shell_command.m34_liens_youtube` | packages/confo_m34_television/m34_liens_youtube.yaml | packages/confo_m34_television/m34_television.yaml, packages/m31_photos.yaml, shell_scripts/m32_musique_liens.py, shell_scripts/m34_liens_youtube.py | n/a |

## M40 — 1 entites

| Entite | Definie dans | Consommee par | Live |
|:-------|:-------------|:--------------|:----:|
| `input_boolean.module_m40_chauffage` | packages/m00_modules.yaml | www/config.html | oui |

## SIM — 13 entites

| Entite | Definie dans | Consommee par | Live |
|:-------|:-------------|:--------------|:----:|
| `automation.simu_reset_auto_bouton_sos_apres_appui` | packages/m00_simulation.yaml | **ORPHELINE** | oui |
| `input_boolean.sim_lit_occupe` | packages/m00_simulation.yaml | dashboards/dashboard_test_simulation.yaml, packages/m11_capteur_lit.yaml | oui |
| `input_boolean.sim_pir_couloir` | packages/m00_simulation.yaml | dashboards/dashboard_test_simulation.yaml, packages/m02_inactivite.yaml | oui |
| `input_boolean.sim_pir_cuisine` | packages/m00_simulation.yaml | dashboards/dashboard_test_simulation.yaml, packages/m02_inactivite.yaml | oui |
| `input_boolean.sim_pir_sdb` | packages/m00_simulation.yaml | dashboards/dashboard_test_simulation.yaml, packages/m02_inactivite.yaml | oui |
| `input_boolean.sim_porte_ext_contact` | packages/m00_simulation_sensors.yaml | dashboards/dashboard_test_simulation.yaml | oui |
| `input_boolean.sim_presence_chambre` | packages/m00_simulation.yaml | dashboards/dashboard_test_simulation.yaml, packages/m02_inactivite.yaml | oui |
| `input_boolean.sim_presence_salon` | packages/m00_simulation.yaml | dashboards/dashboard_test_simulation.yaml | oui |
| `input_boolean.sim_snzb06p_presence` | packages/m00_simulation.yaml | **ORPHELINE** | oui |
| `input_boolean.sim_sos_bouton` | packages/m00_simulation.yaml | dashboards/dashboard_test_simulation.yaml, packages/secur_m10_sos/m10_sos.yaml | oui |
| `input_number.sim_hygro_salon` | packages/m00_simulation_sensors.yaml | dashboards/dashboard_test_simulation.yaml | oui |
| `input_number.sim_temp_chambre` | packages/m00_simulation_sensors.yaml | dashboards/dashboard_test_simulation.yaml, www/aidant.html | oui |
| `input_number.sim_temp_salon` | packages/m00_simulation_sensors.yaml | dashboards/dashboard_test_simulation.yaml, www/aidant.html | oui |

## ORPHELINES (definies, jamais consommees)

- `sensor.m01_alerte_humidite` — definie dans packages/m01_temp_hygro.yaml
- `sensor.m01_alerte_temperature` — definie dans packages/m01_temp_hygro.yaml
- `sensor.m01_hygro_salon_avg_24h` — definie dans packages/m01_temp_hygro.yaml
- `sensor.m01_resume_temp_chambre` — definie dans packages/m01_temp_hygro.yaml
- `sensor.m01_resume_temp_salon` — definie dans packages/m01_temp_hygro.yaml
- `sensor.m11_lit_duree_occupation` — definie dans packages/m11_capteur_lit.yaml
- `sensor.m13_porte_ext_duree_ouverture` — definie dans packages/m13_porte_ext.yaml
- `sensor.m34_session1_fenetre` — definie dans packages/confo_m34_television/m34_television.yaml
- `sensor.m34_session2_fenetre` — definie dans packages/confo_m34_television/m34_television.yaml
- `sensor.m34_session3_fenetre` — definie dans packages/confo_m34_television/m34_television.yaml
- `sensor.m34_session4_fenetre` — definie dans packages/confo_m34_television/m34_television.yaml

## Consommees dynamiquement (nom construit en JS - fausses orphelines)

- `input_boolean.m32_creneau1_actif` — reference via template dynamique dans www/kiosk.html
- `input_boolean.m32_creneau2_actif` — reference via template dynamique dans www/kiosk.html
- `input_boolean.m32_creneau3_actif` — reference via template dynamique dans www/kiosk.html
- `input_boolean.m32_creneau4_actif` — reference via template dynamique dans www/kiosk.html
- `input_datetime.m32_creneau1_debut` — reference via template dynamique dans www/kiosk.html
- `input_datetime.m32_creneau1_fin` — reference via template dynamique dans www/kiosk.html
- `input_datetime.m32_creneau2_debut` — reference via template dynamique dans www/kiosk.html
- `input_datetime.m32_creneau2_fin` — reference via template dynamique dans www/kiosk.html
- `input_datetime.m32_creneau3_debut` — reference via template dynamique dans www/kiosk.html
- `input_datetime.m32_creneau3_fin` — reference via template dynamique dans www/kiosk.html
- `input_datetime.m32_creneau4_debut` — reference via template dynamique dans www/kiosk.html
- `input_datetime.m32_creneau4_fin` — reference via template dynamique dans www/kiosk.html
- `input_text.m34_session4_youtube_url` — reference via template dynamique dans www/config.html

## FANTOMES (definies dans les YAML, absentes de l'instance live)

- `binary_sensor.m11_lit_occupe` — definie dans packages/m11_capteur_lit.yaml -> **renommee en `binary_sensor.m05_lit_occupe`** (registre HA)
- `sensor.m01_hygro_salon_avg_24h` — definie dans packages/m01_temp_hygro.yaml -> **renommee en `sensor.m01_hygro_salon_moy_24h`** (registre HA)
- `sensor.m11_lit_duree_occupation` — definie dans packages/m11_capteur_lit.yaml -> **renommee en `sensor.m05_lit_duree_occupation`** (registre HA)
- `sensor.m13_porte_ext_duree_ouverture` — definie dans packages/m13_porte_ext.yaml -> **renommee en `sensor.m15_porte_ext_duree_ouverture`** (registre HA)
- `sensor.m34_etat_global` — definie dans packages/confo_m34_television/m34_television.yaml -> **renommee en `sensor.confo_m34_etat_global`** (registre HA)
- `sensor.m34_session1_fenetre` — definie dans packages/confo_m34_television/m34_television.yaml -> **renommee en `sensor.confo_m34_session_1_fenetre`** (registre HA)
- `sensor.m34_session2_fenetre` — definie dans packages/confo_m34_television/m34_television.yaml -> **renommee en `sensor.confo_m34_session_fenetre`** (registre HA)
- `sensor.m34_session3_fenetre` — definie dans packages/confo_m34_television/m34_television.yaml -> **renommee en `sensor.confo_m34_session_3_fenetre`** (registre HA)
- `sensor.m34_session4_fenetre` — definie dans packages/confo_m34_television/m34_television.yaml -> **renommee en `sensor.confo_m34_session_4_fenetre`** (registre HA)
- `sensor.m34_video_embed` — definie dans packages/confo_m34_television/m34_liens_youtube.yaml -> **renommee en `sensor.confo_m34_video_en_cours_embed`** (registre HA)

## RENOMMAGES (unique_id du YAML -> entity_id reel du registre HA)

- `binary_sensor.m11_lit_occupe` -> `binary_sensor.m05_lit_occupe`
- `sensor.m01_hygro_salon_avg_24h` -> `sensor.m01_hygro_salon_moy_24h`
- `sensor.m11_lit_duree_occupation` -> `sensor.m05_lit_duree_occupation`
- `sensor.m13_porte_ext_duree_ouverture` -> `sensor.m15_porte_ext_duree_ouverture`
- `sensor.m34_etat_global` -> `sensor.confo_m34_etat_global`
- `sensor.m34_session1_fenetre` -> `sensor.confo_m34_session_1_fenetre`
- `sensor.m34_session2_fenetre` -> `sensor.confo_m34_session_fenetre`
- `sensor.m34_session3_fenetre` -> `sensor.confo_m34_session_3_fenetre`
- `sensor.m34_session4_fenetre` -> `sensor.confo_m34_session_4_fenetre`
- `sensor.m34_video_embed` -> `sensor.confo_m34_video_en_cours_embed`
