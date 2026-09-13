# 🔧 Aperçu Matériel — Projet Assistant au Personne

> **Ordre de grandeur uniquement.** Les prix varient selon les revendeurs et le moment d'achat.  
> Tous les appareils Zigbee listés ici sont **100% Z2M natifs** — zéro cloud Tuya, zéro bridge propriétaire.

---

## 🚫 RÈGLE D'OR

- ✅ **Zigbee2MQTT natif** = intégration locale totale, données chez vous
- ⛔ **Tuya / Smart Life** = cloud chinois obligatoire → **INTERDIT dans ce projet**
- ⛔ **Bridge propriétaire** (Hue Bridge, SONOFF iHost obligatoire) → **INTERDIT** (sauf si Z2M en plus)

---

## 🏗️ INFRASTRUCTURE DE BASE (obligatoire)

| Équipement | Modèle recommandé | Prix indicatif | Notes |
|:-----------|:-----------------|:--------------|:------|
| **Serveur HA** | **Raspberry Pi 4 4Go + SSD USB** | ~0 € (déjà en stock) | SSD obligatoire — carte SD = mort en quelques mois (trop d'écritures HA) |
| **Coordinateur Zigbee** | **Sonoff EFR32MG21 V2** (ZBDongle-E) | ~20 € | Meilleur rapport Q/P 2025, Z2M natif, EFR32MG21 |
| **Dongle 4G secours** | Huawei E3372 + SIM opérateur local | ~30 € + forfait ~5€/mois | Failover automatique si coupure fibre |
| **Accès distant** | **Nabu Casa** (Home Assistant Cloud) | **~7 €/mois** | Obligatoire — accès famille à distance (Marseille → Lille). Zéro config réseau, zéro domaine, zéro VPN. Plugin officiel HA. |

### ⚡ Coupure de courant — Stratégie

**Étape 1 — Auto-redémarrage RPi4 (gratuit, automatique)**
Le Raspberry Pi 4 redémarre **automatiquement** dès que l'alimentation revient après une coupure.
Comportement natif, rien à configurer. HA relance tout seul au boot.

**Étape 2 — Onduleur / UPS (optionnel, recommandé si budget)**

| Modèle | Prix | Autonomie estimée | Notes |
|:-------|:-----|:-----------------|:------|
| **APC Back-UPS BX550MI** | ~50–60 € | 15–30 min (mini-PC seul) | Protection surtensions incluse, USB monitoring |
| APC Back-UPS BX700MI | ~80 € | 30–45 min | Si box internet + mini-PC branchés |

→ L'onduleur donne le temps à HA de faire un arrêt propre ET couvre les micro-coupures (fréquentes en milieu rural).
→ Avec le plugin NUT (Network UPS Tools) dans HA : arrêt automatique propre si batterie < 20%.
→ **Fortement recommandé si la personne est seule** : une micro-coupure peut déclencher de fausses alertes d'inactivité au redémarrage.

---

## 🌡️ MODULE M01 : temp_hygro (OBLIGATOIRE)

| Équipement | Modèle | Prix | Z2M | Autonomie | Précision |
|:-----------|:-------|:-----|:----|:----------|:----------|
| **Capteur T°/Humidité** | **SONOFF SNZB-02P** | ~12 € | ✅ natif | ~4 ans (CR2477) | ±0.2°C / ±2% HR |

**Pourquoi SNZB-02P plutôt qu'Aqara ?**
- Même précision (capteur suisse STS40), moins cher (~12€ vs ~18€ Aqara E1)
- 4 ans d'autonomie réelle constatée
- Supporté nativement Z2M, toutes valeurs exposées

**Combien ?** 1 par pièce sauf toilettes :

| Pièce | Obligatoire | Notes |
|:------|:-----------:|:------|
| Salon | ✅ | Pièce de vie principale |
| Chambre | ✅ | Nuit — froid critique |
| Cuisine | ✅ | Humidité cuisson |
| Salle de bain | ✅ | Humidité élevée fréquente |
| Entrée | 🟡 | Utile si porte ext fréquente |
| Couloir | 🟡 | Pont thermique |
| Bureau | 🟡 | Si villa / pièce utilisée |
| Toilettes | ⛔ | Exclu |

→ **Appartement standard : 4 à 5 capteurs (~48-60€)**
→ **Villa : 6 à 7 capteurs (~72-84€)**

**Dashboard — bouton couleur dynamique :**
- 🟢 vert = toutes pièces OK (16-28°C, hygro < 70%)
- 🟠 orange = au moins une pièce en vigilance
- 🔴 rouge = au moins une pièce critique
- Tap sur le bouton → popup détail toutes les pièces (T° + hygro + couleur par pièce)

---

## 👁️ MODULE : inactivity_monitor (OBLIGATOIRE)

| Équipement | Modèle | Prix | Z2M | Alim. | Portée |
|:-----------|:-------|:-----|:----|:------|:-------|
| **Capteur présence radar** ⭐ | **SONOFF SNZB-06P** | ~18 € | ✅ natif | **USB (filaire)** | 4m / 110° |
| ~~Détecteur PIR~~ ❌ | ~~SONOFF SNZB-03P~~ | ~~10 €~~ | ✅ natif | Pile 3 ans | 6m / 110° |

> **⚠️ POINT CRITIQUE — PIR vs Radar**
>
> Un capteur PIR (SNZB-03P) **ne détecte pas** une personne immobile (assise, endormie, effondrée au sol).  
> Dans un contexte de maintien à domicile, c'est rédhibitoire : la personne peut être inconsciente et le PIR ne verra rien.
>
> **→ SNZB-06P radar micro-ondes 5.8 GHz obligatoire** : détecte la présence même sans mouvement (respiration, infimes déplacements).  
> **→ Contrainte** : doit être branché en USB (câble inclus, pas d'adaptateur). Prévoir une prise USB à proximité.

**Combien ?** 1 par pièce à surveiller (salon + chambre minimum) → 2 unités.

### Alternative avancée — Aqara FP2 (WiFi)

| Équipement | Modèle | Prix | Protocole | Z2M |
|:-----------|:-------|:-----|:----------|:----|
| **Capteur présence mmWave** | **Aqara FP2** | ~80 € | **WiFi (Matter/HomeKit)** | ❌ non supporté |

**Pourquoi le mentionner malgré le WiFi et le prix ?**

Le FP2 utilise un radar **mmWave 60GHz** bien plus précis que le microondes 5.8GHz du SNZB-06P. Deux avantages concrets pour notre usage :

- **Tracking multi-zones** : il peut distinguer "personne au lit" vs "personne debout dans la chambre" dans la même pièce — sans combinaison de capteurs. Utile pour affiner la logique `inactivity_monitor` + `mattress_sensor` en une seule unité.
- **Multi-personnes** : détecte et différencie plusieurs présences simultanées (aidant en visite + patient), ce qui évite des faux positifs lors des passages famille.

**Pourquoi il n'est pas en première recommandation :**

- **Prix** : 80€ vs 18€ = 4,4x plus cher. Pour 2 pièces = +124€.
- **Hors Z2M** : s'intègre via l'intégration native Aqara HA ou Matter — fonctionne en local, mais sort du périmètre Z2M du projet. Ajoute une deuxième "couche" d'intégration à maintenir.
- **Alimenté secteur** : comme le SNZB-06P, pas de batterie.

**Conclusion :** si le budget le permet et que la personne vit seule dans un grand espace, le FP2 peut remplacer à la fois le SNZB-06P ET l'Aqara MCCGQ11LM sous matelas — c'est un gain de précision réel. Mais ce n'est pas indispensable.

---

## 🛌 MODULE : mattress_sensor (FORTEMENT RECOMMANDÉ)

| Équipement | Modèle | Prix | Z2M | Notes |
|:-----------|:-------|:-----|:----|:------|
| **Capteur contact ultra-fin** | **Aqara MCCGQ11LM** (Door/Window Sensor) | ~12 € | ✅ natif | Glissé entre matelas et sommier |

**Pourquoi ?** Distingue sieste (personne au lit = normal) d'une inactivité anormale.  
Evite les fausses alertes type "inactif depuis 2h" alors que la personne dort.  
→ Couplé à la logique temporelle de `inactivity_monitor`.

---

## 🚨 MODULE : sos_button (FORTEMENT RECOMMANDÉ)

| Équipement | Modèle | Prix | Z2M | Notes |
|:-----------|:-------|:-----|:----|:------|
| **Bouton SOS** | **WOOX R7052** | ~15–20 € | ✅ supporté* | Bouton physique portable, alarme instantanée |

> **⚠️ Note Z2M** : Le R7052 est reconnu par Z2M mais peut apparaître comme `TS0215A` non supporté sur les versions anciennes.  
> **Mettre Z2M à jour** (version récente) avant de le pairer. Bien documenté depuis 2024.  
> Source : [Z2M discussion #20496](https://github.com/Koenkk/zigbee2mqtt/discussions/20496)

Disponible sur [Domadoo](https://www.domadoo.fr/en/devices/5683-woox-sos-emergency-button-zigbee-30-8435606701112.html) et Amazon FR.

---

## 📷 MODULE : camera_monitoring (FORTEMENT RECOMMANDÉ)

Deux appareils distincts avec deux rôles distincts :

| Équipement | Rôle | Modèle | Prix | Notes |
|:-----------|:-----|:-------|:-----|:------|
| ~~**Webcam USB Logitech C920s**~~ | ~~Visio Jitsi~~ | ~~supprimée 2026-08-05~~ | ~~60–70 €~~ | Remplacée par caméra frontale tablette |
| **Caméra WiFi PTZ** | Surveillance + LLM Vision + live aidants | **Reolink E1 Pro** | ~30–40 € | 5MP, PTZ 360°, vision nocturne, RTSP |

> **⚠️ ATTENTION modèle Reolink** : Ne pas prendre le **Reolink E1 de base** → manque l'API HTTP → incompatible intégration HA native.  
> **E1 Pro obligatoire.**

### Trois usages de la Reolink E1 Pro

| Usage | Déclencheur | Qui voit |
|:------|:------------|:---------|
| **LLM Vision posture/chute** | Inactivité anormale détectée → snapshot → Gemini Flash | Alerte auto famille |
| **Clip événementiel** | Porte extérieure ouverte, fenêtre ouverte | Notification famille |
| **Live à la demande** | Aidant ouvre le flux depuis son téléphone | Aidant seulement |

Le **live à la demande** est utile si la personne change fréquemment de pièce sans raison apparente (signe de désorientation). L'aidant peut jeter un œil sans que ce soit du monitoring permanent. Flux RTSP intégré dans le dashboard famille HA — rien ne tourne quand personne ne regarde.

### Architecture vidéo — clip au déclencheur (pas flux permanent)

La caméra fonctionne en **mode événementiel**, pas en NVR permanent :

| Déclencheur | Action caméra | Notification famille |
|:------------|:-------------|:--------------------|
| Radar détecte changement de zone (entrée → couloir → cuisine) | Clip 15s via `camera.record` HA | Optionnel (info) |
| Capteur fenêtre s'ouvre | Clip 10s | Non (usage chauffage) |
| **Capteur porte extérieure s'ouvre** | **Clip 20s immédiat** | **OUI — OBLIGATOIRE** |
| Inactivité anormale détectée | Snapshot + analyse LLM Vision posture | OUI — alerte + image |

**→ Alzheimer / désorientation :** ouverture porte extérieure = envoi clip vidéo immédiat à la famille. Pas de délai, pas de condition. C'est non-négociable.

**Stockage clips :** sur le SSD du mini-PC (dossier `/config/www/clips/`), purge auto après 48h.  
Pas besoin de Frigate pour ça — le service `camera.record` natif HA + Reolink suffit.  
LLM Vision (snapshot) reste pour la détection de posture (chute).

---

## 🪟 MODULE : window_heating (OPTIONNEL — mais "++ selon budget")

> Piloter chauffage/clim quand une fenêtre est ouverte. Utile pour éviter de chauffer dehors, et pour ne pas laisser la personne dans un courant d'air.

### Capteur fenêtre

| Équipement | Modèle | Prix | Z2M | Notes |
|:-----------|:-------|:-----|:----|:------|
| **Capteur contact fenêtre** | **SONOFF SNZB-04P** (ou PR2) | ~10–13 € | ✅ natif | Même modèle que porte |

### Pilotage selon type de chauffage

**Cas 1 — Radiateur électrique (convecteur / soufflant / inertie)**

| Équipement | Modèle | Prix | Notes |
|:-----------|:-------|:-----|:------|
| Prise connectée | **NOUS A1Z** | ~15 € | Coupure courant si fenêtre ouverte > 2 min |

Simple et fiable. Fenêtre ouverte → prise coupe le radiateur → fenêtre fermée → prise rallume.

**Cas 2 — Climatisation réversible (télécommande IR)**

| Équipement | Modèle | Prix | Connexion | Notes |
|:-----------|:-------|:-----|:----------|:------|
| **Blaster IR** | **Broadlink RM4 Mini** | ~25 € | **WiFi** (exception Z2M) | Intégration HA native locale |

> **Pourquoi une exception WiFi ici ?**  
> Il n'existe pas de blaster IR Zigbee fiable et non-Tuya sur le marché en 2026.  
> Le Broadlink RM4 Mini fonctionne en **LAN local** (API ouverte, intégration HA officielle), pas de cloud obligatoire.  
> C'est l'exception acceptable dans ce projet.
>
> **⚠️ Complexité à anticiper :**  
> Il faut apprendre les codes IR de la télécommande de chaque clim (procédure "learning mode").  
> Chaque installation est différente. Ce module sera documenté avec une procédure d'apprentissage pas-à-pas.

**Cas 3 — Chauffage collectif / chaudière centrale**
→ Pilotage impossible (pas de contrôle individuel). Le module `window_heating` se limite à une **alerte** (notification : "fenêtre ouverte depuis Xmin — pensez à fermer").

---

## 🚪 MODULE : door_monitor (OPTIONNEL)

| Équipement | Modèle | Prix | Z2M | Notes |
|:-----------|:-------|:-----|:----|:------|
| **Capteur contact porte** | **SONOFF SNZB-04P** (ou PR2) | ~10–13 € | ✅ natif | CR2477, ~5 ans autonomie |

**PR2** = version améliorée : piles AAA, corps plus fin, aimant plus fort. Même prix.  
Alerte si sortie hors horaires autorisés (ex : la nuit, fugue Alzheimer).

---

## 📺 MODULE M11 : television (OPTIONNEL)

**Aucun matériel supplémentaire à acheter.** L'écran TV est piloté directement par
le mini-PC/RPi4 déjà en stock, branché en **HDMI** sur la TV, avec un navigateur
en plein écran enregistré dans **Browser Mod**. Bascule Photos ↔ chaînes/YouTube
via `browser_mod.javascript` / `browser_mod.navigate` (redirection du navigateur
vers la page live de la chaîne ou vers le dashboard photos) — pas de casting
Google Cast, donc pas de Chromecast nécessaire.

> **Chromecast retiré (2026-07-04)** : solution abandonnée au profit du
> pilotage direct du navigateur HDMI (plus fiable, pas d'app_id Google Cast
> à trouver pour France 2/Arte/France 5). Voir `Docs/packages/M11_tv.md`.

## 🔌 MODULE : tv_power / heating_control (OPTIONNEL)

| Équipement | Modèle | Prix | Z2M | Notes |
|:-----------|:-------|:-----|:----|:------|
| **Prise connectée** | **NOUS A1Z** | ~15 € | ✅ natif | Coupure automatique TV, pilotage radiateur soufflant |

Alternative : **IKEA TRADFRI E1603** ou **IKEA INSPELNING** ~10-15€ — aussi Z2M natif.

---

## 💡 RÉCAPITULATIF COMPLET

| Module | Équipement | Qté type | Prix unit. | Sous-total |
|:-------|:-----------|:--------:|:----------:|:----------:|
| infra | **RPi4 4Go + SSD** | 1 | **0 €** (stock) | 0 € |
| infra | Coordinateur Zigbee (EFR32MG21) | 1 | 20 € | 20 € |
| infra | Dongle 4G Huawei E3372 | 1 | 30 € | 30 € |
| infra | **Nabu Casa** (accès distant) | 1 | **7 €/mois** | 84 €/an |
| infra ++ | Onduleur APC BX550MI | 0–1 | 55 € | 0–55 € |
| temp_monitor | SONOFF SNZB-02P | 2–3 | 12 € | 24–36 € |
| inactivity | SONOFF SNZB-06P (radar) | 2 | 18 € | 36 € |
| mattress | Aqara MCCGQ11LM | 1 | 12 € | 12 € |
| sos_button | WOOX R7052 | 1 | 18 € | 18 € |
| camera | ~~Webcam USB Logitech C920s~~ (supprimée — caméra tablette) | — | 0 € | 0 € |
| camera | Reolink E1 Pro (surveillance + LLM + live) | 1–2 | 35 € | 35–70 € |
| kiosk | **Tablette Android** (kiosk écran) | 1 | 0–70 € | 0 € si déjà possédée |
| kiosk | **Fully Kiosk Browser PLUS** (licence) | 1 | 10.99 € | One-time |
| door | SONOFF SNZB-04P | 1–2 | 11 € | 11–22 € |
| tv/heat | NOUS A1Z (prise) | 0–2 | 15 € | 0–30 € |
| window_heating | SONOFF SNZB-04P (fenêtre) | 0–3 | 11 € | 0–33 € |
| window_heating ++ | Broadlink RM4 Mini (IR clim) | 0–1 | 25 € | 0–25 € |
| **TOTAL matériel** | | | | **~197–340 €** |

> + Onduleur UPS : +55 € (recommandé)  
> + Tablette Android si non possédée : +50–70 €  
> + Fully Kiosk Browser PLUS : +10.99 € (one-time)  
> + Nabu Casa : 84 €/an (obligatoire — accès distant famille)  
> + VPS Jitsi : ~5 €/mois si module `visio` actif  
> **Fourchette globale projet complet : 310 – 520 € (+ ~17 €/mois abonnements)**

---

## 🛒 OÙ ACHETER

| Revendeur | Points forts |
|:----------|:-------------|
| [Domadoo.fr](https://www.domadoo.fr) | Spécialiste domotique FR, stock local, WOOX, Aqara, Sonoff |
| [Amazon.fr](https://www.amazon.fr) | Prix compétitifs Sonoff, livraison rapide |

---

## ⚠️ CE QU'ON N'ACHÈTE PAS

| ❌ Éviter | Raison |
|:---------|:-------|
| Tuya / Smart Life / MOES (bouton SOS) | Cloud chinois, Z2M partiel ou non supporté |
| Aqara FP2 | ~80€, surdimensionné, Z2M instable |
| Apple Watch / montre connectée | Hors budget, complexité, nécessite smartphone |
| Shelly (sauf Shelly Gen3 Zigbee) | Shelly classique = WiFi, pas Z2M |
| Reolink E1 (base) | Pas d'API HTTP → intégration HA cassée |
| Tuya SOS buttons (Amazon) | Cloud obligatoire, Z2M non supporté ou partiel |
| IR blaster Tuya / Smart Life | Cloud obligatoire → INTERDIT |

---

*Dernière mise à jour : 2026-07-04 — v4 (suppression Chromecast : TV pilotée directement via RPi4/HDMI + Browser Mod, cf. M11)*
