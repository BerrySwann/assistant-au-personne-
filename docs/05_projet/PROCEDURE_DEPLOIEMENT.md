# Procédure de Déploiement — Assistant au Personne
*Créé le 2026-08-11*

---

## 🎯 Objectif

Déployer une instance Home Assistant pré-configurée (packages M0x, dashboards kiosk + aidant) sur un nouveau matériel (Raspberry Pi 4 ou Mini-PC), pour une nouvelle famille.

---

## 🧰 Pré-requis

### Matériel
| Composant | Détail |
|:----------|:-------|
| Raspberry Pi 4 (4 Go RAM min.) ou Mini-PC x86 | Hôte HA |
| Clé Zigbee Sonoff EFR32MG21 V2 | Contrôleur Zigbee |
| SSD ou carte µSD 32 Go min. | Stockage |
| Câble réseau (recommandé) ou Wi-Fi | Connexion |

### Comptes à créer avant de commencer
- [ ] Compte [Nabu Casa](https://www.nabucasa.com) (optionnel pendant l'install, obligatoire à la fin)
- [ ] Compte Google (pour Calendar si module M03 Agenda utilisé)

### Fichier de déploiement (fourni par le déployeur)
- `assistant_au_personne_vX.Y.tar` — sauvegarde HA complète

---

## 📋 Procédure pas à pas

### ÉTAPE 1 — Préparer la sauvegarde (côté déployeur)

> ⚠️ Cette étape est faite UNE FOIS par le déployeur, pas par la famille.

1. Dans l'instance HA source : **Paramètres → Système → Sauvegardes**
2. Créer une sauvegarde complète
3. Télécharger le fichier `.tar` généré
4. **Mettre à jour `secrets_template.yaml`** avec les clés à remplacer (voir section Secrets)
5. Distribuer le `.tar` + `secrets_template.yaml` à la famille (clé USB, lien de partage, etc.)

---

### ÉTAPE 2 — Installer Home Assistant OS

**Sur Raspberry Pi 4 :**
1. Télécharger [Raspberry Pi Imager](https://www.raspberrypi.com/software/)
2. Choisir `Other specific OS → Home Assistant → Home Assistant OS (RPi4)`
3. Flasher la carte µSD / SSD
4. Brancher et démarrer — attendre 5-10 min

**Sur Mini-PC x86 :**
1. Télécharger l'image HAOS x86-64 sur [github.com/home-assistant/operating-system](https://github.com/home-assistant/operating-system/releases)
2. Flasher sur SSD via Balena Etcher
3. Démarrer sur le SSD

**Vérifier que HA est accessible :**
- Ouvrir `http://homeassistant.local:8123` dans un navigateur
- Si ça ne répond pas : trouver l'IP via le routeur → `http://[IP]:8123`

---

### ÉTAPE 3 — Restaurer la sauvegarde ⚠️ AVANT NABU CASA

> C'est l'étape critique. Ne pas créer de compte Nabu Casa avant cette étape.

1. Sur l'écran d'accueil HA (nouvel install) → cliquer **"Restore from backup"**
2. Choisir **"Upload backup"** → sélectionner le fichier `.tar`
3. Sélectionner **"Full restore"**
4. HA redémarre automatiquement (~5 min)
5. Se connecter avec les identifiants par défaut fournis dans `secrets_template.yaml`

---

### ÉTAPE 4 — Post-restore : adapter les secrets

> Ces valeurs sont spécifiques à chaque installation.

Fichier à modifier : **`/config/secrets.yaml`** (via Studio Code Server add-on, déjà installé)

```yaml
# Modifier ces valeurs pour la nouvelle installation
mqtt_host: "127.0.0.1"          # IP du broker MQTT (local = 127.0.0.1)
mqtt_user: "VOTRE_USER_MQTT"
mqtt_password: "VOTRE_MDP_MQTT"

# Si intégration Linky (MyElectricalData)
linky_pdl: "VOTRE_NUMERO_PDL"
linky_token: "VOTRE_TOKEN"

# Token Google Calendar (si agenda activé)
google_token: ""                 # Sera régénéré via l'intégration HA
```

Après modification : **Paramètres → Système → Redémarrer**

---

### ÉTAPE 5 — Connecter Nabu Casa

> Maintenant seulement, après le restore et les secrets.

1. **Paramètres → Home Assistant Cloud → Se connecter**
2. Créer un compte sur `nabucasa.com` ou se connecter si déjà créé
3. L'URL distante est générée automatiquement : `https://[hash].ui.nabu.casa`
4. **Copier cette URL** → c'est le lien à donner aux 5 aidants

---

### ÉTAPE 6 — Créer les comptes aidants

1. **Paramètres → Personnes → Ajouter une personne**
2. Cocher "Autoriser la connexion"
3. Créer un nom d'utilisateur + mot de passe **unique par aidant**
4. Rôle : **Utilisateur** (pas Administrateur)
5. Répéter pour chaque aidant (max recommandé : 10)

**Définir le dashboard aidant par défaut :**
- Profil utilisateur → Dashboard par défaut → `Interface Aidant`

---

### ÉTAPE 7 — Appairer les appareils Zigbee

> Les appareils Zigbee doivent être re-pairés sur le nouveau coordinateur.

> ⚠️ Exception : si la clé Zigbee source EST la même clé physique transférée, et que le backup inclut la base Z2M avec la clé réseau → pas de re-pairing nécessaire.

Si nouveau coordinateur :
1. Ouvrir Zigbee2MQTT (add-on ou LXC)
2. Activer le mode pairing
3. Appairer chaque appareil un par un

---

### ÉTAPE 8 — Checklist finale

| Vérification | Méthode | OK ? |
|:-------------|:--------|:-----|
| Dashboard kiosk s'affiche | Ouvrir sur la TV | ☐ |
| Dashboard aidant s'affiche | Ouvrir sur un téléphone | ☐ |
| T° salon/chambre remontent | Voir vignette L1C2 | ☐ |
| Envoi d'un message test | Dashboard aidant → Envoyer | ☐ |
| Bandeau kiosk affiche le message | Attendre ~15 sec | ☐ |
| Connexion distante Nabu Casa | Ouvrir l'URL depuis données mobiles | ☐ |
| Chaque aidant peut se connecter | Tester login 1 par 1 | ☐ |

---

## 🔑 Distribution des accès aux aidants

Envoyer à chaque aidant (SMS ou message) :

```
Bonjour [Prénom],

Voici votre accès à l'interface de suivi :

🔗 Lien : https://[hash].ui.nabu.casa
👤 Identifiant : [login]
🔒 Mot de passe : [mdp]

Astuce : ajoutez ce lien en favori sur votre téléphone.
Sur iPhone : Safari → Partager → Sur l'écran d'accueil
Sur Android : Chrome → ⋮ → Ajouter à l'écran d'accueil
```

---

## ⚠️ Pièges connus

| Piège | Symptôme | Solution |
|:------|:---------|:---------|
| Nabu Casa créé AVANT le restore | URL Nabu Casa ne fonctionne plus | Déconnecter → reconnecter Nabu Casa après restore |
| secrets.yaml non mis à jour | MQTT déconnecté, Linky KO | Éditer secrets.yaml + redémarrer |
| Clé Zigbee sur mauvais port USB | Z2M ne démarre pas | Changer le port dans config Z2M |
| IP du routeur différente | Appareils IP injoignables | Scanner réseau + mettre à jour les IP dans les packages |
| Backup trop vieux | Entités manquantes | Faire un backup frais depuis la dernière version prod |

---

## 📦 Fichiers du kit de déploiement

```
kit_deploiement_vX.Y/
├── assistant_au_personne_vX.Y.tar   ← sauvegarde HA
├── secrets_template.yaml             ← variables à remplir
├── PROCEDURE_DEPLOIEMENT.md          ← ce document
└── liens_utiles.txt                  ← HAOS images, Imager, etc.
```
