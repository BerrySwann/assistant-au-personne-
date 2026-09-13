#!/usr/bin/env bash
# ============================================================
# HA GIT BACKUP — Assistant au personne (HAOS 10.32.154.241)
# Adapté de /config/.scripts/ha_git_backup.sh (maison home_assistant_re-build)
# ============================================================
# Sauvegarde automatique de /config vers GitHub
# (repo PRIVÉ BerrySwann/assistant-au-personne-).
#
# Lancé par l'automation "M00 — Backup GitHub (H+10)" toutes les
# heures à la minute 10 (00:10, 01:10, ...).
#
# Différences avec la version maison :
#  - pas de filtre par extension : ce dépôt versionne aussi les
#    .html/.py/.json/.txt (tout ce qui n'est PAS dans .gitignore est
#    committé — c'est .gitignore qui fait le tri) ;
#  - pas de notification HA (pas de .secrets/ha_token ici) ;
#  - pas de tag weekly (non demandé).
#
# PIÈGES (repris de la maison) :
#  - secrets.yaml ne doit JAMAIS être tracké — garde-fou bloquant ;
#  - auth : token HTTPS embarqué dans l'URL du remote (persistant
#    dans /config/.git/config) — c'est le modèle maison ;
#  - set -euo pipefail : toute erreur non gérée => exit 1 ;
#  - push rejeté (fetch first) => fetch + force-with-lease ;
#  - git add -A AVANT la détection : évite les fantômes GitHub lors
#    des renommages.
# ============================================================
set -euo pipefail

LOG_DIR="/config/.logs"
LOG="$LOG_DIR/ha_git_backup.log"
mkdir -p "$LOG_DIR"
exec 1>/dev/null   # stdout bloqué — seul le log compte
cd /config

# Nettoyage rebase-merge orphelin + branche main garantie
[ -d /config/.git/rebase-merge ] && { git rebase --abort 2>/dev/null || rm -fr /config/.git/rebase-merge 2>/dev/null; } || true
git checkout main 2>/dev/null || git switch main 2>/dev/null || true

trap 'echo "❌ Erreur inattendue ligne $LINENO — $(date "+%Y-%m-%d %H:%M:%S")" >> "$LOG"' ERR

# Identité git
git config user.name  "BerrySwann (HAOS)"
git config user.email "BerrySwann@users.noreply.github.com"

# ── GARDE-FOU : secrets.yaml ne doit jamais être tracké ──
if git ls-files --error-unmatch secrets.yaml >/dev/null 2>&1; then
  echo "❌ secrets.yaml est tracké par git — ABANDON" >> "$LOG"
  exit 1
fi

BRANCH="$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo main)"
[[ "$BRANCH" == "HEAD" ]] && { git switch main 2>/dev/null || true; BRANCH="main"; }
if ! git rev-parse --abbrev-ref --symbolic-full-name "@{u}" >/dev/null 2>&1; then
  git branch -u "origin/${BRANCH}" >/dev/null 2>&1 || true
fi

# ── STAGING + DÉTECTION ──
git add -A >/dev/null 2>&1
CHANGED="$(git diff --cached --name-only | sort -u || true)"
AHEAD="$(git rev-list @{u}..HEAD --count 2>/dev/null || echo 0)"

if [[ -z "$CHANGED" && "$AHEAD" -eq 0 ]]; then
  echo "ℹ️ GitHub deja a jour - rien a committer: $(date '+%Y-%m-%d %H:%M:%S %Z')" >> "$LOG"
  exit 0
fi

# ── MESSAGE DE COMMIT ──
MSG="HAOS auto-backup: $(date '+%Y-%m-%d %H:%M:%S %Z')"
HA_VER=""
[[ -f /config/.HA_VERSION ]] && HA_VER="$(cat /config/.HA_VERSION 2>/dev/null)"
MSG="${MSG}${HA_VER:+ (HA ${HA_VER})}"

# ── COMMIT ──
if git commit -m "$MSG" >/dev/null 2>&1; then
  echo "📝 Commit créé: $MSG" >> "$LOG"
else
  AHEAD="$(git rev-list @{u}..HEAD --count 2>/dev/null || echo 0)"
  if [[ "$AHEAD" -gt 0 ]]; then
    echo "📤 Commit local non pushé ($AHEAD) — push en cours: $(date '+%Y-%m-%d %H:%M:%S %Z')" >> "$LOG"
  else
    echo "ℹ️ GitHub deja a jour - rien a committer: $(date '+%Y-%m-%d %H:%M:%S %Z')" >> "$LOG"
    exit 0
  fi
fi

# ── PUSH avec gestion fetch-first ──
do_push() {
  local PUSH_OUT
  PUSH_OUT=$(git push origin "$BRANCH" 2>&1) && return 0
  if echo "$PUSH_OUT" | grep -qE "fetch first|non-fast-forward|rejected"; then
    echo "⚠️ Push rejeté (divergence) — fetch + force-with-lease: $(date '+%Y-%m-%d %H:%M:%S %Z')" >> "$LOG"
    git fetch origin "$BRANCH" >/dev/null 2>&1 || true
    PUSH_OUT=$(git push --force-with-lease origin "$BRANCH" 2>&1)
    if [[ $? -eq 0 ]]; then
      echo "✅ Push OK (force-with-lease): $(date '+%Y-%m-%d %H:%M:%S %Z')" >> "$LOG"
      return 0
    fi
    echo "❌ Push impossible: $PUSH_OUT" >> "$LOG"
    return 1
  fi
  echo "❌ Push impossible: $PUSH_OUT" >> "$LOG"
  return 1
}

do_push || exit 1
echo "✅ Backup GitHub OK: $MSG" >> "$LOG"

# annotations_log:
# [2026-09-13] Création — adapté du script maison (BerrySwann/home_assistant_re-build).
#              Repo cible : BerrySwann/assistant-au-personne- (PRIVÉ, passage en privé
#              le jour même : données de santé/perso d'une personne vulnérable).
