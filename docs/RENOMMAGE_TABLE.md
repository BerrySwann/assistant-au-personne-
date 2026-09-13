# TABLE DE RENOMMAGE — Origine → Nouveau

*Ledger de suivi, mis à jour au fur et à mesure de l'exécution réelle. Convention et périmètre : voir `PLAN_RENOMMAGE_MODULES.md`.*
*Statut : **EXÉCUTÉ le 13/08 2026** — substitution de contenu + réorganisation en dossiers appliquées sur Z:\ et local. Toutes les lignes ci-dessous sont désormais actives. Voir notes critiques en bas de fichier (registre HA, redémarrage requis).*

## Toggles (`input_boolean.module_*`)

| Origine | Nouveau |
|:---|:---|
| module_temp_hygro | module_m01_temp_hygro |
| module_inactivite | module_m02_inactivite |
| module_ecran_msg | module_m03_ecran_msg |
| module_sos | module_m10_sos |
| module_capteur_lit | module_m11_capteur_lit |
| module_cam_ia | module_m12_cam_ia |
| module_porte_ext | module_m13_porte_ext |
| module_fenetre | module_m14_fenetre |
| module_lumiere_nuit | module_m17_lumiere_nuit |
| module_medoc | module_m20_medoc |
| module_repas | module_m21_repas |
| module_douche | module_m22_douche |
| module_kiosk_ecran | module_m30_kiosk_ecran |
| module_kiosk_foto | module_m31_kiosk_foto |
| module_kiosk_zic | module_m32_kiosk_zic |
| module_visio | module_m33_visio |
| module_television | module_m34_television |
| module_liens_youtube | module_m34_liens_youtube |

## oblig_M01 (préfixe inchangé)

| Origine | Nouveau |
|:---|:---|
| m01_temp_salon_min_24h | m01_temp_salon_min_24h |
| m01_temp_salon_max_24h | m01_temp_salon_max_24h |
| m01_hygro_salon_moy_24h *(entity_id réel — diffère du unique_id `m01_hygro_salon_avg_24h`)* | m01_hygro_salon_moy_24h *(inchangé)* |
| m01_temp_chambre_min_24h | m01_temp_chambre_min_24h |
| m01_temp_chambre_max_24h | m01_temp_chambre_max_24h |
| m01_alerte_temperature | m01_alerte_temperature |
| m01_alerte_humidite | m01_alerte_humidite |
| m01_resume_temp_salon | m01_resume_temp_salon |
| m01_resume_temp_chambre | m01_resume_temp_chambre |

## oblig_M02 (préfixe inchangé)

| Origine | Nouveau |
|:---|:---|
| m02_derniere_activite | m02_derniere_activite |
| m02_seuil_matin | m02_seuil_matin |
| m02_seuil_sieste | m02_seuil_sieste |
| m02_seuil_aprem | m02_seuil_aprem |
| m02_seuil_soir | m02_seuil_soir |
| m02_seuil_nuit | m02_seuil_nuit |
| m02_obs_gap | m02_obs_gap |
| m02_facteur_alerte | m02_facteur_alerte |
| m02_facteur_apprentissage | m02_facteur_apprentissage |
| m02_ema_alpha | m02_ema_alpha |
| m02_jours_apprentissage | m02_jours_apprentissage |
| m02_alerte_active | m02_alerte_active |
| m02_absence_nuit_anormale | m02_absence_nuit_anormale |
| m02_activite_detectee | m02_activite_detectee |
| m02_tranche_horaire | m02_tranche_horaire |
| m02_seuil_tranche_actuelle | m02_seuil_tranche_actuelle |
| m02_inactivite_minutes | m02_inactivite_minutes |
| m02_seuil_alerte_effectif | m02_seuil_alerte_effectif |
| m02_check_inactivite | m02_check_inactivite |
| m02_reset_activite | m02_reset_activite |
| m02_fin_slot_matin | m02_fin_slot_matin |
| m02_fin_slot_sieste | m02_fin_slot_sieste |
| m02_fin_slot_aprem | m02_fin_slot_aprem |
| m02_fin_slot_soir | m02_fin_slot_soir |
| m02_fin_slot_nuit | m02_fin_slot_nuit |

## oblig_M03 (préfixe inchangé)

| Origine | Nouveau |
|:---|:---|
| m03_message_famille | m03_message_famille |
| m03_message_auteur | m03_message_auteur |
| m03_queue_msg | m03_queue_msg |
| m03_queue_auteur | m03_queue_auteur |
| m03_affiche_msg | m03_affiche_msg |
| m03_affiche_auteur | m03_affiche_auteur |
| m03_queue_timestamps | m03_queue_timestamps |
| m03_rate_limit | m03_rate_limit |
| m03_rl_max | m03_rl_max |
| m03_affichage_duree | m03_affichage_duree |
| m03_queue_max | m03_queue_max |
| m03_rl_fenetre | m03_rl_fenetre |
| m03_message_envoi | m03_message_envoi |
| m03_affiche_depuis | m03_affiche_depuis |
| m03_envoi_debut | m03_envoi_debut |
| m03_envoi_fin | m03_envoi_fin |
| m03_rotation | m03_rotation |
| m03_envoyer | m03_envoyer |
| m03_afficher_suivant | m03_afficher_suivant |
| m03_agenda_formate | m03_agenda_formate |
| m03_texto_formate | m03_texto_formate |
| m03_bandeau_principal | m03_bandeau_principal |
| m03_reset_reglages | m03_reset_reglages |
| m03_rotation_timer_finished | m03_rotation_timer_finished |
| m03_clear_queue_minuit | m03_clear_queue_minuit |
| m03_historique | m03_historique |
| m03_log_message | m03_log_message |
| m03_reprise_timer_apres_reboot | m03_reprise_timer_apres_reboot |

## Secur_M10 (ancien M04 → m04_ devient m10_)

| Origine | Nouveau |
|:---|:---|
| m04_sos_declenche | m10_sos_declenche |
| m04_sos_appui | m10_sos_appui |
| m04_sos_reset | m10_sos_reset |
| m04_droits_aidants | m10_droits_aidants |
| m04_envoyer_alerte_sos | m10_envoyer_alerte_sos |
| m04_envoyer_alerte_moderee | m10_envoyer_alerte_moderee |
| m04_proximite_aidant_1 | m10_proximite_aidant_1 |
| m04_proximite_aidant_2 | m10_proximite_aidant_2 |
| m04_proximite_aidant_3 | m10_proximite_aidant_3 |
| m04_proximite_aidant_4 | m10_proximite_aidant_4 |
| m04_proximite_aidant_5 | m10_proximite_aidant_5 |
| m04_proximite_aidant_6 | m10_proximite_aidant_6 |
| m04_proximite_aidant_7 | m10_proximite_aidant_7 |
| m04_prox_aidant_1_admin_ok *(existe réellement, registre vérifié 13/08)* | m10_prox_aidant_1_admin_ok |
| m04_prox_aidant_2_ok | m10_prox_aidant_2_ok |
| m04_prox_aidant_3_ok | m10_prox_aidant_3_ok |
| m04_prox_aidant_4_hs | m10_prox_aidant_4_hs |
| m04_prox_aidant_5_hs | m10_prox_aidant_5_hs |
| m04_prox_aidant_6_ok | m10_prox_aidant_6_ok |
| m04_prox_aidant_7_hs | m10_prox_aidant_7_hs |

**⚠️ Bug préexistant découvert (registre, 13/08) — sans rapport avec le renommage :** `m04_prox_aidant_*` (v3, dynamique) existe dans le registre mais n'est câblé nulle part dans le script d'envoi SOS — celui-ci utilise en réalité `m04_proximite_aidant_1..7` (l'ancien système figé, v2). Les deux jeux d'entités seront renommés (`m10_` à la place de `m04_`), mais le bug de câblage reste entier après renommage — à traiter séparément.

## Secur_M11 (ancien M05 → m05_ devient m11_)

| Origine | Nouveau |
|:---|:---|
| m05_lit_occupe | m11_lit_occupe |
| m05_lit_duree_occupation | m11_lit_duree_occupation |

## Secur_M13 (ancien M15 → m15_ devient m13_)

| Origine | Nouveau |
|:---|:---|
| m15_porte_ext_duree_ouverture | m13_porte_ext_duree_ouverture |

## Confo_M31 (ancien M08 → m08_ devient m31_)

| Origine | Nouveau |
|:---|:---|
| m08_photos_dossier | m31_photos_dossier |
| m08_photos_intervalle_s | m31_photos_intervalle_s |
| m08_lancer_diaporama | m31_lancer_diaporama |

## Confo_M33 (ancien M10 → m10_ devient m33_)

| Origine | Nouveau |
|:---|:---|
| m10_visio_url | m33_visio_url |

## Confo_M34 (ancien M11 + M16-youtube → m11_ ET m16_ deviennent m34_)

| Origine | Nouveau |
|:---|:---|
| m11_browser_id_tv | m34_browser_id_tv |
| m11_session1_youtube_url | m34_session1_youtube_url |
| m11_session2_youtube_url | m34_session2_youtube_url |
| m11_session3_youtube_url | m34_session3_youtube_url |
| m11_session4_youtube_url | m34_session4_youtube_url |
| m11_session_affichee | m34_session_affichee |
| m11_session1_chaine | m34_session1_chaine |
| m11_session2_chaine | m34_session2_chaine |
| m11_session3_chaine | m34_session3_chaine |
| m11_session4_chaine | m34_session4_chaine |
| m11_session1_actif | m34_session1_actif |
| m11_session2_actif | m34_session2_actif |
| m11_session3_actif | m34_session3_actif |
| m11_session4_actif | m34_session4_actif |
| m11_session1_ok | m34_session1_ok |
| m11_session2_ok | m34_session2_ok |
| m11_session3_ok | m34_session3_ok |
| m11_session4_ok | m34_session4_ok |
| m11_session1_debut | m34_session1_debut |
| m11_session1_fin | m34_session1_fin |
| m11_session2_debut | m34_session2_debut |
| m11_session2_fin | m34_session2_fin |
| m11_session3_debut | m34_session3_debut |
| m11_session3_fin | m34_session3_fin |
| m11_session4_debut | m34_session4_debut |
| m11_session4_fin | m34_session4_fin |
| m11_session_1_fenetre *(entity_id réel — diffère du unique_id `m11_session1_fenetre`)* | m34_session_1_fenetre |
| m11_session_2_fenetre | m34_session_2_fenetre |
| m11_session_3_fenetre | m34_session_3_fenetre |
| m11_session_4_fenetre | m34_session_4_fenetre |
| m11_etat_global | m34_etat_global |
| m11_lancer_session | m34_lancer_session |
| m11_verifier_sessions | m34_verifier_sessions |
| m11_bouton_ok_session | m34_bouton_ok_session |
| m11_epg_entity_creneau1 | m34_epg_entity_creneau1 |
| m11_marge_fin_min | m34_marge_fin_min |
| m11_marge_recherche_min | m34_marge_recherche_min |
| m11_reset_desactivation | m34_reset_desactivation |
| m11_tv_flux | m34_tv_flux |
| m11_url_arte *(à confirmer vivant)* | m34_url_arte |
| m11_url_france2 *(à confirmer vivant)* | m34_url_france2 |
| m11_url_france5 *(à confirmer vivant)* | m34_url_france5 |
| m16_video_en_cours_embed *(entity_id réel — diffère du unique_id `m16_video_embed`)* | m34_video_en_cours_embed |
| m16_maj_liens_hebdo | m34_maj_liens_hebdo |
| m16_next | m34_next |
| m11_sessionN_\* *(boucle Jinja2, code dynamique)* | m34_sessionN_\* |

## Exclus (gérés séparément par toi — pas touchés)

| Origine | Statut |
|:---|:---|
| module_dashboard_fam | inchangé |
| module_msg_famille | inchangé |

---

**Total traité :** 18 toggles + ~120 sub-entités statiques (hors oblig, inchangé) + fichiers réorganisés en dossiers.

## Nouvelle arborescence `raspi/packages/` (+ Z:\packages\)

```
m00_modules.yaml / m00_simulation.yaml / m00_simulation_sensors.yaml   (socle, inchangé)
m01_temp_hygro.yaml / m02_inactivite.yaml                              (inchangés)
oblig_m03_ecran_msg/  m03_ecran_msg.yaml, m03_reset_reglages.yaml
secur_m10_sos/        m10_sos.yaml, m10_gestion_aidants.yaml, m10_groupe_aidants.yaml
m11_capteur_lit.yaml  (ex m05, fichier unique)
m13_porte_ext.yaml    (ex m15, fichier unique)
m31_photos.yaml       (ex m08, fichier unique)
m33_visio.yaml        (ex m10, fichier unique)
confo_m34_television/ m34_television.yaml (ex m11_tv.yaml), m34_liens_youtube.yaml (ex m16)
```

## ⚠️ CE QUI N'A PAS PU ÊTRE FAIT AUTOMATIQUEMENT

**Les 7 helpers `input_boolean.m04_prox_aidant_*` créés dynamiquement (registre HA, invisibles en YAML) n'ont PAS été renommés.** Je n'ai pas d'outil sûr pour renommer des entités directement dans `.storage/core.entity_registry` d'une instance live sans risquer de corrompre le registre. Ils continueront de fonctionner sous leur ancien nom `m04_prox_*` tant qu'ils ne sont pas renommés via l'UI HA (Paramètres > Entités > renommer) ou via `hab` (OpenCode).

**Conséquence du renommage des `unique_id` :** au prochain redémarrage HA, les entités dont le `unique_id` a changé (tout ce qui était `m04_/m05_/m08_/m10_/m11_/m15_/m16_`) vont apparaître comme de **nouvelles entités** sous leur nouveau nom. Les anciennes deviendront orphelines dans le registre (état "indisponible", pas d'erreur bloquante) — à nettoyer via Paramètres > Entités > filtrer "non disponible" une fois le redémarrage fait et vérifié.

**Redémarrage HA requis** pour que ces changements (packages + m00_modules.yaml) prennent effet.

## ⚠️ BUG DÉCOUVERT AU 1er REDÉMARRAGE (13/08, post-exécution)

Kiosk TV cassé après le premier redémarrage. Cause : les capteurs template et les automations dérivent leur `entity_id` du texte `name:`/`alias:` (pas du `unique_id`). Ce texte disait encore "M11"/"M16" en toutes lettres (jamais touché par la substitution, qui ne visait que les identifiants minuscules avec underscore). Résultat : HA a recréé ces entités avec un slug basé sur l'ancien nom, en collision avec l'orpheline encore présente → suffixe `_2` ajouté (ex : `sensor.m34_etat_global` réellement créé sous `sensor.m11_etat_global_2`).

**Corrigé :** tous les `name:`/`alias:` mis à jour (M04→Secur_M10, M05→Secur_M11, M08→Confo_M31, M10→Confo_M33, M11→Confo_M34, M15→Secur_M13, M16→Confo_M34). Registre nettoyé : 67 entités retirées (orphelines anciennes + celles mal recréées avec `_2`) pour forcer une régénération propre au 2e redémarrage.

**Leçon pour la suite :** toujours vérifier `name:`/`alias:` en plus des `unique_id`/clés YAML avant un renommage — les deux peuvent diverger silencieusement.
