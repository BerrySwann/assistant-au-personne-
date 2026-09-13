# PLAN DE RENOMMAGE — Entités Mxx → nouvelle numérotation par groupe

*Créé le 2026-08-13. Document de travail : table de correspondance à valider AVANT toute exécution.*
*Ne PAS exécuter sur Z:\ tant que ce document n'est pas validé ligne par ligne.*

---

## 1. Convention proposée

**Garder le même style qu'aujourd'hui** (`m` + 2 chiffres + `_`), juste renuméroté selon le nouveau schéma de groupe. Pas de nouveau vocabulaire (`secur_`, `confo_`...) dans les `entity_id` eux-mêmes — uniquement dans la doc/les labels.

Raison : `m00_modules.yaml` documente déjà une contrainte dure — **max 20 caractères après `module_`**. Préfixer avec `secur_m10_`, `confo_m34_` etc. ferait dépasser cette limite sur plusieurs entités (`confo_m34_television` = 21 caractères, par exemple). Le préfixe court `m` + nouveau numéro reste toujours sous la limite (vérifié ligne par ligne ci-dessous).

**Table des préfixes (dérivée de la table de correspondance déjà validée dans `DEPENDANCES_GLOBALES.md`) :**

| Ancien préfixe | Nouveau préfixe | Groupe |
|:---|:---|:---|
| `m01_` | `m01_` *(inchangé)* | oblig_M01 |
| `m02_` | `m02_` *(inchangé)* | oblig_M02 |
| `m03_` | `m03_` *(inchangé)* | oblig_M03 |
| `m04_` | **`m10_`** | Secur_M10 SOS |
| `m05_` | **`m11_`** | Secur_M11 Capteur Lit |
| — *(aucun fichier)* | `m12_` | Secur_M12 Caméra IA |
| `m15_` | **`m13_`** | Secur_M13 Porte Ext |
| — *(aucun fichier)* | `m14_` | Secur_M14 Fenêtre |
| — *(pas encore créé)* | `m15_` | Secur_M15 Frigo |
| — *(pas encore créé)* | `m16_` | Secur_M16 Congel |
| *(registre, aucun fichier)* | `m17_` | Secur_M17 Veilleuse Nuit |
| — *(aucun fichier)* | `m20_` | Santé_M20 Médicaments |
| — *(aucun fichier)* | `m21_` | Santé_M21 Repas |
| — *(aucun fichier)* | `m22_` | Santé_M22 Douche |
| — *(dashboard, pas de fichier)* | `m30_` | Confo_M30 Kiosk Écran |
| `m08_` | **`m31_`** | Confo_M31 Photos Famille |
| — *(aucun fichier)* | `m32_` | Confo_M32 Musique |
| `m10_` | **`m33_`** | Confo_M33 Visio |
| `m11_` | **`m34_`** | Confo_M34 Télévision |
| `m16_` *(liens_youtube — collision historique)* | **`m34_`** *(fusion — sous-composant réel de la TV)* | Confo_M34 Télévision |
| — | `m40_` | Envir_M40 Chauffage |

**⚠️ Exclus du renommage** (orphelins, retrait géré séparément par toi) : `module_dashboard_fam` (ancien M19), `module_msg_famille` (ancien M20). Je n'y touche pas.

**⚠️ M00 hors périmètre (volontaire, pas un oubli) :** `m00_modules.yaml`, `m00_simulation.yaml`, `m00_simulation_sensors.yaml` ne sont pas des modules — c'est le socle (registre des 20 toggles + capteurs de simulation temporaires). Aucun `input_boolean.module_*` propre, rien à ranger dans oblig/Secur/Santé/Confo/Envir. Reste `m00_` sans changement.

**⚠️ Ordre d'exécution critique :** `m04_→m10_`, `m05_→m11_`, `m10_→m33_`, `m11_→m34_` doivent être swappés de façon **atomique** (tout en une seule passe, jamais entité par entité dans le désordre). Si `m04_` est renommé en `m10_` AVANT que l'ancien `m10_` soit lui-même renommé en `m33_`, il y a collision temporaire (deux groupes de fichiers réclament `m10_` en même temps).

---

## 2. Toggles `module_*` (input_boolean, aucun numéro actuellement)

| Ancien | Nouveau proposé | Longueur après `module_` |
|:---|:---|:---|
| `module_temp_hygro` | `module_m01_temp_hygro` | 14 ✓ |
| `module_inactivite` | `module_m02_inactivite` | 14 ✓ |
| `module_ecran_msg` | `module_m03_ecran_msg` | 13 ✓ |
| `module_sos` | `module_m10_sos` | 7 ✓ |
| `module_capteur_lit` | `module_m11_capteur_lit` | 15 ✓ |
| `module_cam_ia` | `module_m12_cam_ia` | 10 ✓ |
| `module_porte_ext` | `module_m13_porte_ext` | 13 ✓ |
| `module_fenetre` | `module_m14_fenetre` | 11 ✓ |
| `module_lumiere_nuit` | `module_m17_lumiere_nuit` | 16 ✓ |
| `module_medoc` | `module_m20_medoc` | 9 ✓ |
| `module_repas` | `module_m21_repas` | 9 ✓ |
| `module_douche` | `module_m22_douche` | 10 ✓ |
| `module_kiosk_ecran` | `module_m30_kiosk_ecran` | 15 ✓ |
| `module_kiosk_foto` | `module_m31_kiosk_foto` | 14 ✓ |
| `module_kiosk_zic` | `module_m32_kiosk_zic` | 13 ✓ |
| `module_visio` | `module_m33_visio` | 9 ✓ |
| `module_television` | `module_m34_television` | 14 ✓ |
| `module_liens_youtube` | `module_m34_liens_youtube` | 19 ✓ *(sous-toggle, reste séparé de module_television)* |
| `module_dashboard_fam` | **inchangé — exclu** | — |
| `module_msg_famille` | **inchangé — exclu** | — |

Toutes tiennent sous la limite de 20 caractères.

---

## 3. Table complète par fichier (entités statiques déclarées en YAML)

### oblig_M01 — `raspi/packages/m01_temp_hygro.yaml` (préfixe inchangé, rien à renommer)
`m01_temp_salon_min_24h`, `m01_temp_salon_max_24h`, `m01_hygro_salon_avg_24h`, `m01_temp_chambre_min_24h`, `m01_temp_chambre_max_24h`, `m01_alerte_temperature`, `m01_alerte_humidite`, `m01_resume_temp_salon`, `m01_resume_temp_chambre`

### oblig_M02 — `raspi/packages/m02_inactivite.yaml` (préfixe inchangé, rien à renommer)
`m02_derniere_activite`, `m02_seuil_matin/sieste/aprem/soir/nuit`, `m02_obs_gap`, `m02_facteur_alerte`, `m02_facteur_apprentissage`, `m02_ema_alpha`, `m02_jours_apprentissage`, `m02_alerte_active`, `m02_absence_nuit_anormale`, `m02_activite_detectee`, `m02_tranche_horaire`, `m02_seuil_tranche_actuelle`, `m02_inactivite_minutes`, `m02_seuil_alerte_effectif`, `m02_check_inactivite`, `m02_reset_activite`, `m02_fin_slot_matin/sieste/aprem/soir/nuit`

### oblig_M03 — `raspi/packages/m03_ecran_msg.yaml` + `m03_reset_reglages.yaml` (préfixe inchangé, rien à renommer)
`m03_message_famille`, `m03_message_auteur`, `m03_queue_msg`, `m03_queue_auteur`, `m03_affiche_msg`, `m03_affiche_auteur`, `m03_queue_timestamps`, `m03_rate_limit`, `m03_rl_max`, `m03_affichage_duree`, `m03_queue_max`, `m03_rl_fenetre`, `m03_message_envoi`, `m03_affiche_depuis`, `m03_envoi_debut`, `m03_envoi_fin`, `m03_rotation`, `m03_envoyer`, `m03_afficher_suivant`, `m03_agenda_formate`, `m03_texto_formate`, `m03_bandeau_principal`, `m03_reset_reglages`, `m03_rotation_timer_finished`, `m03_clear_queue_minuit`, `m03_historique`, `m03_log_message`, `m03_reprise_timer_apres_reboot`

### Secur_M10 (ancien M04) — `m04_sos.yaml`, `m04_gestion_aidants.yaml`, `m04_groupe_aidants.yaml` → **tout `m04_` devient `m10_`**
`m04_sos_declenche`→`m10_sos_declenche`, `m04_sos_appui`→`m10_sos_appui`, `m04_sos_reset`→`m10_sos_reset`, `m04_droits_aidants`→`m10_droits_aidants`, `m04_envoyer_alerte_sos`→`m10_envoyer_alerte_sos`, `m04_envoyer_alerte_moderee`→`m10_envoyer_alerte_moderee`, `m04_proximite_aidant_1..7`→`m10_proximite_aidant_1..7`
**⚠️ Cas spécial — `m04_prox_<object_id>`** : convention dynamique (helpers créés à la volée par `hab helper input-boolean create m04_prox_<nom>`), pas déclarée dans le YAML. Deviendrait `m10_prox_<object_id>`. **Nécessite de vérifier dans le registre HA live (`.storage/core.entity_registry`) si des helpers `m04_prox_*` existent déjà réellement** — ils ne sont pas visibles depuis les fichiers texte. Aucun aidant réel n'étant encore inscrit (comptes fictifs `person.aidant_*`), le risque est probablement nul, mais à vérifier avant d'exécuter.

### Secur_M11 (ancien M05) — `m05_capteur_lit.yaml` → **tout `m05_` devient `m11_`**
`m05_lit_occupe`→`m11_lit_occupe`, `m05_lit_duree_occupation`→`m11_lit_duree_occupation`

### Secur_M13 (ancien M15) — `m15_porte_ext.yaml` → **tout `m15_` devient `m13_`**
`m15_porte_ext_duree_ouverture`→`m13_porte_ext_duree_ouverture`

### Confo_M31 (ancien M08) — `m08_photos.yaml` → **tout `m08_` devient `m31_`**
`m08_photos_dossier`→`m31_photos_dossier`, `m08_photos_intervalle_s`→`m31_photos_intervalle_s`, `m08_lancer_diaporama`→`m31_lancer_diaporama`

### Confo_M33 (ancien M10) — `m10_visio.yaml` → **tout `m10_` devient `m33_`**
`m10_visio_url`→`m33_visio_url`
*(fichier à renommer aussi : `m10_visio.yaml` → `m33_visio.yaml` — et la fiche `M20_visio.md` jamais corrigée depuis le premier rename, à renommer `M33_visio.md` cette fois)*

### Confo_M34 (ancien M11 + M16-youtube) — `m11_tv.yaml`, `m16_liens_youtube.yaml` → **tout `m11_` ET tout `m16_` deviennent `m34_`**
`m11_browser_id_tv`, `m11_session{1-4}_youtube_url`, `m11_session_affichee`, `m11_session{1-4}_chaine`, `m11_session{1-4}_actif`, `m11_session{1-4}_ok`, `m11_session{1-4}_debut/fin`, `m11_session{1-4}_fenetre`, `m11_etat_global`, `m11_lancer_session`, `m11_verifier_sessions`, `m11_bouton_ok_session`, `m11_epg_entity_creneau1`, `m11_marge_fin_min`, `m11_marge_recherche_min`, `m11_reset_desactivation`, `m11_tv_flux`, `m11_url_arte/france2/france5` *(ces 3 derniers déjà signalés morts en session — à confirmer avant de les renommer ou les retirer)*
`m16_video_embed`→`m34_video_embed`, `m16_maj_liens_hebdo`→`m34_maj_liens_hebdo`, `m16_next`→`m34_next`
**⚠️ Cas spécial — boucle template `m11_sessionN_*`** : le code Jinja2 construit probablement l'entity_id dynamiquement (`"m11_session" ~ n ~ "_actif"` ou équivalent) plutôt que d'écrire chaque cas en dur. Il faut retrouver et corriger ce code, pas juste les déclarations statiques.
*(fichier à renommer aussi : `m11_tv.yaml` → `m34_television.yaml`, `m16_liens_youtube.yaml` → fusionné dans le même fichier ou renommé `m34_liens_youtube.yaml`)*

---

## 4. Ce que ce document NE couvre PAS encore (à faire avant exécution)

- Comptage précis fichier-par-fichier de chaque occurrence (dashboards + 4 fichiers HTML : `aidant.html`, `config.html`, `appairage.html`, `launch.html`) — je peux le générer sur demande, ce sera long (plusieurs centaines de lignes).
- Vérification du registre HA live (`.storage/core.entity_registry` sur Z:\) pour les helpers créés dynamiquement (`m04_prox_*`) et pour toute entité renommée via l'UI qui aurait un slug différent de la clé YAML.
- Décision : qui exécute réellement le renommage — édition de texte brute (risque : entités orphelines dans le registre) vs outil registre-aware (`hab`/`zigporter`, côté OpenCode).
- Les fichiers `SETUP/*.yaml` (mapping capteurs non pairés) n'utilisent pas la nomenclature Mxx — hors périmètre.

---

## 5. Prochaine étape proposée

Valider ce document (sections 1-3) avant que je génère la liste exhaustive des occurrences par fichier (tâche 4 du plan). Rien n'est encore modifié.
