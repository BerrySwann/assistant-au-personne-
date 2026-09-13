# 📋 CAHIER DES CHARGES — Assistant au Personne
*Document de référence unique — dernière mise à jour : 2026-08-13*

> Ce fichier remplace et unifie `PROJET_MODULAIRE_HA_SESSION_2026-06-30.md` (spec d'origine) et les décisions prises en session depuis. Il est **la source de vérité** sur ce que le projet doit faire. `hardware.md` reste la référence pour les prix, `dependances.md` reste la référence pour l'état d'avancement technique (fichiers/entités).
>
> Statut : document vivant — des idées seront ajoutées au fil des sessions. Chaque ajout doit être daté.

---

## 1. Vision du projet

Système domotique modulaire basé sur Home Assistant, conçu pour maintenir à domicile une personne en difficulté (aujourd'hui : Alzheimer). Inspiré du projet de Benjamin Code pour sa mère.

**Principe directeur** : un socle technique commun (Core), robuste et minimal, auquel on ajoute des modules spécifiques selon les besoins réels de la personne. On ne construit pas un système monolithique "toutes pathologies confondues" — cette approche a été explicitement écartée car les besoins (ex: Alzheimer vs mobilité réduite) sont parfois opposés (garde-fous passifs vs contrôle actif de l'environnement).

**Portée actuelle** : usage réel pour une personne (Alzheimer). L'ambition générique/réutilisable par d'autres aidants (mentionnée dans le README d'origine) reste un objectif secondaire, non prioritaire tant que le système n'est pas validé sur le cas réel.

**Règle produit « grand public » *(décision 2026-08-13, non négociable)*** : le système doit être **utilisable par des personnes non-techniciennes** — les aidants, les installateurs bénévoles, les familles. Conséquences : interface **hyper simple** (gros boutons, zéro gestion de token/cache/config), robustesse prioritaire sur la sophistication, et **toute solution qui pose problème à un non-technicien doit être remplacée** (ex. le HTML custom embarqué a une alternative native HA prête). C'est une exigence produit, pas un vœu.

---

## 2. Objectifs

- Sécuriser l'occupant et prévenir les accidents domestiques.
- Détecter les anomalies de comportement (chutes, errance, inactivité anormale).
- Alerter les proches de manière graduée (rappel doux → alerte aidant → urgence).
- Automatiser les tâches contraintes sans exiger d'interaction complexe de la personne — zéro smartphone côté occupant.

---

## 3. Contraintes techniques et de sécurité (non négociables)

- **Automatismes critiques 100% locaux** : les automatisations de sécurité (lumières, alertes locales, coupures électriques) ne doivent JAMAIS dépendre d'une connexion internet. Une coupure de box ne doit pas désactiver la sécurité de base.
- **Accès distant famille : Nabu Casa** *(décision 2026-08-05, remplace le choix initial "Cloudflare Tunnel écarté Nabu Casa")* — sert uniquement à l'accès à distance de la famille, pas aux automatismes. Une coupure internet coupe l'accès distant, pas la sécurité locale.
- **Secours électrique** : onduleur (UPS) sur le serveur HA, le routeur et le coordinateur Zigbee. *(confirmé 2026-08-05)*
- **Secours réseau** : clé 4G/5G en failover automatique si coupure fibre/box. 4G ou 5G indifférent selon dispo/prix. *(confirmé 2026-08-05 — reste à choisir un forfait adapté à un usage de secours occasionnel, pas un forfait plein tarif)*
- **Matériel de qualité** : privilégier les relais/contacteurs modulaires au tableau électrique plutôt que de simples prises connectées pour les gros électroménagers (ex: coupure plaque de cuisson).
- **Zéro cloud propriétaire pour le matériel** : Zigbee2MQTT natif obligatoire. Tuya/Smart Life interdit. Voir `hardware.md` pour la liste noire complète.
- **Simplicité pour l'occupant** : interface physique traditionnelle ou ultra-simplifiée (boutons, pas d'écran tactile complexe à manipuler).
- **Validation fonctionnelle obligatoire, pas documentaire** : un module n'est "terminé" que lorsqu'il a été testé dans les conditions réelles (voir §7), pas simplement codé et déployé. Une doc texte que personne ne relit n'est pas une garantie de sécurité.

---

## 4. Socle commun (Core)

Installé et actif en permanence, indépendamment des modules spécifiques activés.

| Composant | Rôle |
|---|---|
| Serveur HA (RPi4, cible mini-PC en prod) | Moteur central, tourne en local |
| Coordinateur Zigbee (Sonoff EFR32MG21) + Zigbee2MQTT | Réseau de capteurs local, sans cloud |
| Nabu Casa | Accès distant famille |
| Onduleur (UPS) | Continuité en cas de coupure secteur |
| Dongle 4G/5G | Continuité réseau en cas de coupure box |
| Suivi passif d'activité | Capteurs porte d'entrée, et à évaluer : frigo/placards stratégiques *(idée 2026-08-05, pas encore décidée — cf §8)* |
| Suivi consommation électrique | Pinces ampèremétriques (type Shelly) au tableau pour détecter l'usage des appareils (four, bouilloire, TV) comme signal d'activité indirect *(idée 2026-08-05, pas encore décidée — cf §8)* |
| Notifications graduées | Vers smartphone aidant, niveaux d'urgence différenciés |

---

## 5. Modules — état et décisions

### 5.1 Modules obligatoires (sécurité de base)

| Module | Description | Statut |
|---|---|---|
| `temperature_monitor` (M01) | Alerte froid < 16°C / chaleur > 28°C, couplé vigilance canicule Météo France | ✅ Déployé |
| `inactivity_monitor` | Logique temporelle (pas timer plat) — fenêtres actives/sieste/nuit, voir détail ci-dessous | ✅ **Développé** (12/08, `m02_inactivite.yaml`) — reste à valider en conditions réelles (§7) |
| `screen_messages` (M03) | Heure, date, messages famille, agenda | ✅ Déployé |

**Logique `inactivity_monitor` (reprise du 30/06, non modifiée)** :
```
Heures actives (8h-12h, 15h-19h) + aucun mouvement + aucun son → 45 min → alerte famille
Sieste (12h-15h) + capteur matelas ON → pas d'alerte
Sieste + capteur matelas OFF + 45 min sans mouvement → alerte douce
Nuit (22h-8h) → pas d'alerte (sommeil normal)
Nuit + capteur matelas OFF après 23h + aucun mouvement → alerte (pas couchée)
```

### 5.2 Modules fortement recommandés

| Module | Description | Décision |
|---|---|---|
| `camera_monitoring` + LLM Vision | Snapshot déclenché par le capteur de présence → Gemini Flash analyse la posture ("au sol" = alerte) | **Obligatoire, conditionné à validation** *(décision 2026-08-05)* — voir critère d'acceptation §7. Caméra retenue : **Reolink E1 Pro** (pas le E1 de base, API HTTP absente sur ce modèle). Architecture : caméra fixe, déclenchement uniquement sur anomalie détectée par le radar — pas de scan PTZ permanent ni de reconstruction de scène (options écartées, trop lentes/complexes pour un besoin de détection rapide). |
| `sos_button` | Bouton Zigbee → alerte famille immédiate | Prévu, WOOX R7052 |
| `mattress_sensor` | Capteur contact sous matelas → distingue sieste d'inactivité anormale | Prévu, Aqara MCCGQ11LM |

**Capteur de présence** : **SONOFF SNZB-06P** (radar 5.8 GHz cmWave). **Attention** : ne pas confondre avec le SNZB-06P24 (24 GHz) — la doc officielle de cette variante avertit qu'elle ne détecte pas fiablement une personne endormie/immobile, ce qui est rédhibitoire pour ce projet. *(vérifié 2026-07-27)*

### 5.3 Modules optionnels (selon profil)

Repris tels quels de la spec du 30/06 — non réévalués individuellement à ce stade : `kiosk_screen`, `kiosk_photos`, `tv_control` (= M11, déjà avancé, voir 5.4), `music_therapy`, `youtube_direct` *(Invidious écarté définitivement — YouTube direct implémenté via M16, décision actée 2026-08-13)*, `visio_meet` *(pivoté de Jitsi vers Google Meet le 12/08 — voir MAJ ci-dessous)*, `shower_tracking`, `medication_reminder`, `meal_reminder`, `door_monitor`, `night_lighting`, `family_dashboard`, `heating_control`.

**MAJ 2026-08-13 — Visio** : le module visio a **pivoté de Jitsi vers Google Meet** (12/08). Salle permanente `meet.google.com/czg-supk-snw`, bouton « Lancer la Visio » dans l'interface aidant. La salle Jitsi et l'intégration `custom_components/visio_jitsi` (explorée) sont **écartées** pour ce projet — conformément à la règle produit « grand public » : app native + lien simple plutôt qu'intégration technique.

**Ajouts proposés le 2026-08-05, non encore actés** (voir §8 pour arbitrage) :
- Coupure automatique de la plaque de cuisson si absence de cuisine > 5 min.
- Alerte vocale sur enceinte en cas de sortie nocturne (22h-6h), en plus de la notification aidant.
- Balisage lumineux nocturne chambre → toilettes (recoupe `night_lighting`, déjà prévu).
- Tableaux de bord avec historique/tendance d'activité sur plusieurs semaines (pas seulement des alertes ponctuelles).

### 5.4 Module M11 — Télévision

Statut le plus avancé du projet : redirection navigateur (Browser Mod) fonctionnelle et testée pour France TV. En cours de pivot : affichage **dans une carte du dashboard** (pas en plein écran, pour garder les messages visibles) via contenu YouTube embarqué en iframe (France TV bloque l'embed, `X-Frame-Options: DENY` — vérifié).

**Chantier ouvert** : sélection des vidéos/chaînes France 2 disponibles sur YouTube adaptées à la personne (pas de contenu anxiogène), et process pour ajouter de nouvelles émissions dans le temps. *(tâche en attente, voir suivi de tâches)*

---

## 5.5 Hiérarchie des aidants *(ajout 2026-08-05)*

| Rôle | Nombre | Droits | Reçoit |
|---|---|---|---|
| **Administrateur** | 2 (préférable, redondance) | Configure les modules, gère les comptes aidants et leurs permissions | Tout (urgence + modéré + technique) |
| **Aidant de proximité** | Variable (ex: 3) | Peut se déplacer physiquement en cas d'urgence | Urgence + Modéré |
| **Aidant (distant)** | Variable (ex: 4) | Ne peut pas intervenir physiquement (distance ou autre) | Modéré + Info uniquement, jamais l'urgence |

**Mécanisme technique retenu** *(à trancher — voir échange du 2026-08-05)* : s'appuyer sur les entités `person.x` déjà créées nativement par HA à la connexion de chaque compte, regroupées via un helper "Groupe" créé depuis l'UI HA (pas de fichier `groupes.yaml` à maintenir à la main — le natif stocke ça dans `.storage/`, modifiable par l'UI sans YAML ni redémarrage). Alternative plus lourde (fichier `groupes.yaml` littéral réécrit par script) écartée sauf si besoin explicite de lisibilité/édition manuelle du fichier.

**Catalogue des remontées d'info par niveau d'urgence** (voir §7 pour les critères de validation) :
- **Urgence** (aidants proximité + admin) : SOS bouton, absence nocturne anormale, chute confirmée caméra+Gemini, inactivité anormale en heures actives.
- **Modéré** (tous aidants + admin) : sortie hors horaires, température anormale, oubli médicaments, ~~pas de repas détecté~~ (**abandonné le 2026-08-16** — voir §8), pas de douche.
- **Info/positif** (tous aidants) : message famille sur écran, appel visio, statut du jour, tendance d'activité.
- **Technique** (admin seulement) : batterie capteur faible, panne réseau, surchauffe système, caméra déconnectée.

---

## 6. Interface et tableaux de bord

- **Occupant** : dashboard kiosk (écran permanent) — horloge, messages, TV/photos, zéro action complexe requise.
- **Aidant/famille** : interface mobile **hyper simple** (règle produit §1) — vue synthétique (températures, statut), bouton visio, envoi de messages. Implémentée en HTML custom (`www/aidant.html`, token localStorage) avec une **migration native HA en cours** (dashboard `lovelace-aidant-v2`, bubble-card, 13/08) qui supprime token/cache pour les non-techniciens.
- **Configuration** : dashboard modules — activation/désactivation par module, réglages détaillés. Réglages M03 disposant d'un **bouton reset** vers les valeurs d'usine (13/08).

---

## 7. Critères de validation (avant de considérer un module "terminé")

Aucun module de sécurité n'est validé sur la seule base du code déployé. Critères minimaux :

- **Présence/inactivité** : test de couverture — la personne (ou un testeur) traverse toute la pièce concernée pendant 2 minutes ; le capteur doit détecter une présence continue sans zone morte. Si la pièce fait plus de ~5m ou a une forme en L, prévoir un second capteur.
- **Détection de chute (caméra + Gemini)** : 20-30 essais avec postures réelles (debout, assis, allongé au sol, différents coins de pièce, jour/nuit). **Zéro faux négatif toléré sur "au sol"** — un faux positif est acceptable, un faux négatif ne l'est pas.
- **Alertes** : vérifier la réception réelle côté aidant (pas juste le déclenchement de l'automation côté HA).

---

## 8. Points en attente d'arbitrage

Liste ouverte — à trancher au fur et à mesure, pas à ignorer :

1. ~~Invidious vs YouTube direct~~ — **tranché le 2026-08-13** : YouTube direct (M16), Invidious écarté définitivement.
1bis. ~~Module M21 « Repas » (détection prise alimentaire)~~ — **ABANDONNÉ le 2026-08-16**. Aucun signal fiable de « repas pris » : (a) la conso d'un appareil de cuisson ne voit rien l'été (salade froide, plat non chauffé) ; (b) les prises connectées sont **non fiables en contexte Alzheimer** — la personne les débranche/déplace, ce qui invalide silencieusement le signal (principe général : éviter tout capteur manipulable par la personne aidée) ; (c) le seul signal robuste toute l'année (contact d'ouverture frigo/congélateur + question posée au kiosk) ne « détecte » pas un repas, il en donne un simple indice — ouvrir le congélateur pour une glace n'est pas un déjeuner. Jugé insuffisant pour justifier le module. Si un besoin réapparaît, le remplacer par un simple **rappel** (« c'est l'heure de manger » sur le kiosk), sans prétendre détecter quoi que ce soit. Code retiré (`module_m21_repas` dans `m00_modules.yaml`, carte dans `config.html`).
2. Capteurs frigo/placards et pinces ampèremétriques Shelly — les ajouter au Core ou les garder en option ?
3. Coupure automatique plaque de cuisson — matériel à définir (relais/contacteur au tableau), risque électrique à valider avant d'automatiser une coupure de gros électroménager.
4. Portée générique du projet (réutilisable par d'autres aidants) vs usage sur-mesure pour un seul cas — impacte si les modules "mobilité réduite" et "déficiences sensorielles" (proposés le 2026-08-05) doivent être développés ou laissés de côté.

---

## 9. Budget

Voir `hardware.md` pour le détail par capteur avec prix vérifiés. Deux écarts connus non résolus entre les documents historiques :
- `README.md` annonçait 800-1000€ + ~100€/an (chiffres d'origine, jamais mis à jour).
- `hardware.md` (04/07) donne 300-510€ + ~17€/mois — plus réaliste sur les prix matériel de base, mais ne compte pas encore les ajouts du §8.

Prix vérifiés en session (2026-07-27) : Reolink E1 Pro ~60€, SONOFF SNZB-06P ~17€.

---

## 10. Ressources

- [Benjamin Code — Vidéo 1](https://www.youtube.com/watch?v=_-nV3CUIixc)
- [Benjamin Code — Vidéo 2](https://www.youtube.com/watch?v=k0pW7HyYcSo)
- [Benjamin Code — Playlist Alzheimer](https://www.youtube.com/playlist?list=PLpmAblQfFT6Ly7W8hZPzt5NfdfwZI1mZr)
- [LLM Vision HACS](https://github.com/valentinfrlch/ha-llmvision)

---

*Prochaine mise à jour : à chaque décision structurante prise en session. Dater chaque ajout.*
