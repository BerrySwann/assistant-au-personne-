#!/usr/bin/env python3
"""M34 - Liens YouTube France 2, Arte & france tv pour Home Assistant.

Actions (passees en argument 1, argument 2 optionnel = url/video_id) :
  update                     : recupere les flux RSS des chaines officielles,
                               deduplique par ID video, ajoute les nouveautes
                               en tete de liste. Saut des #Shorts et des
                               videos de moins de 60 s (via yt-dlp).
  mark <url>                 : marque la ligne contenant <url> comme "deja_vu".
  next                       : imprime l'URL de la plus recente video NON vue
                               (rien si tout est vu).
  duration <video_id>        : imprime la duree en secondes (entier, rien si
                               inconnue) - utilise par M34 pour ne marquer
                               "deja_vu" que 5 min avant la fin reelle.

Fichier : www/liens_youtube.txt - format par ligne :
  aaaa-mm-jj|chaine|Titre|https://youtu.be/XXXX|deja_vu
La date est la date de publication YouTube. Le dernier champ est vide si la
video n'a pas encore ete vue.

Renomme depuis m16_liens_youtube.py le 2026-08-14 (le fichier physique
n'avait jamais ete renomme lors du renommage general M16->M34 du 13/08 -
shell_command.m34_liens_youtube pointait vers un fichier inexistant).
"""

import os
import sys
import urllib.request
import xml.etree.ElementTree as ET

FILE = os.environ.get("M34_FILE", "/config/www/liens_youtube.txt")
SHORTS_CACHE = os.environ.get("M34_SHORTS_CACHE", "/config/www/m16_shorts_ignores.txt")
UA = "Mozilla/5.0 (compatible; HomeAssistant-M34/1.0)"
CHANNELS = {
    "UCSTz2DxJLFR7CDB7HRwbnrA": "france2",
    "UCwI-JbGNsojunnHbFAc0M4Q": "arte",
    "UCh4o9ioiqbUveUrCLP8Wv6A": "francetv",
}
PLAYLISTS = {
    "PLdeL1gXKY5_nQr51b_L8QFKhZYT343o83": "tv5monde",
    "PL4lTkNiyT5GZWXZKq5aB4H3vTpS0ajwsq": "natgeo",
}
RSS_URL = "https://www.youtube.com/feeds/videos.xml?channel_id={}"
PLAYLIST_URL = "https://www.youtube.com/feeds/videos.xml?playlist_id={}"
NS = {
    "a": "http://www.w3.org/2005/Atom",
    "yt": "http://www.youtube.com/xml/schemas/2015",
}
MARQUEUR_VU = "déjà_vu"

# Labels de selection par session : une cle peut inclure plusieurs chaines
# (france tv inclut aussi les anciennes videos france2).
LABEL_ALIASES = {
    "francetv": {"francetv", "france2"},
    "arte": {"arte"},
    "tv5monde": {"tv5monde"},
    "natgeo": {"natgeo"},
}


def read_lines():
    if not os.path.exists(FILE):
        return []
    with open(FILE, encoding="utf-8") as handle:
        return [line.rstrip("\n") for line in handle if line.strip()]


def write_lines(lines):
    os.makedirs(os.path.dirname(FILE), exist_ok=True)
    with open(FILE, "w", encoding="utf-8") as handle:
        handle.write("\n".join(lines) + "\n")


def fetch_feed(url):
    request = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(request, timeout=20) as response:
        return response.read()


def entries_from_feed(label, url):
    entries = []
    root = ET.fromstring(fetch_feed(url))
    for item in root.findall("a:entry", NS):
        title_el = item.find("a:title", NS)
        vid_el = item.find("yt:videoId", NS)
        pub_el = item.find("a:published", NS)
        if title_el is None or vid_el is None or pub_el is None:
            continue
        title = " ".join((title_el.text or "").split())
        video_id = (vid_el.text or "").strip()
        date = (pub_el.text or "")[:10]
        if not video_id or "#shorts" in title.lower():
            continue
        title = title.replace("|", "-")
        entries.append((date, label, title, video_id))
    return entries


def video_id_from_url(url):
    if "youtu.be/" in url:
        return url.rsplit("/", 1)[-1].strip()
    if "v=" in url:
        return url.split("v=", 1)[-1].split("&", 1)[0].strip()
    return None


def video_duration_seconds(video_id):
    """Duree en secondes via yt-dlp (contourne les Shorts sans hashtag)."""
    try:
        import yt_dlp
        opts = {"quiet": True, "no_warnings": True, "skip_download": True}
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info("https://www.youtube.com/watch?v={}".format(video_id), download=False)
            return info.get("duration")
    except Exception:
        return None


def is_short(video_id, title):
    """Vrai si la video est un extrait court : hashtag dans le titre OU duree < 10 min."""
    if "#shorts" in title.lower():
        return True
    duration = video_duration_seconds(video_id)
    if duration is None:
        return False
    return duration < 600


def read_shorts_cache():
    """IDs des Shorts deja identifies (evite de re-verifier via yt-dlp)."""
    if not os.path.exists(SHORTS_CACHE):
        return set()
    with open(SHORTS_CACHE, encoding="utf-8") as handle:
        return {line.strip() for line in handle if line.strip()}


def remember_short(video_id):
    """Persiste un ID de Short ignore."""
    cached = read_shorts_cache()
    cached.add(video_id)
    with open(SHORTS_CACHE, "w", encoding="utf-8") as handle:
        handle.write("\n".join(sorted(cached)) + "\n")


def do_purge(label=None):
    """Re-verifie les videos deja en liste avec le seuil actuel et retire
    celles de moins de 10 min. label optionnel : 'arte', 'natgeo', ...
    (utile pour purger par lots sans depasser le timeout de 60 s)."""
    lines = read_lines()
    kept = []
    removed = 0
    for line in lines:
        parts = line.split("|")
        if len(parts) >= 4 and (label is None or parts[1] == label):
            video_id = video_id_from_url(parts[3])
            title = parts[2] if len(parts) > 2 else ""
            if video_id and is_short(video_id, title):
                removed += 1
                continue
        kept.append(line)
    write_lines(kept)
    print("Purge {} : {} video(s) retiree(s). Reste : {} ligne(s).".format(label or "toutes", removed, len(kept)))


def do_update():
    existing = read_lines()
    seen_ids = set()
    for line in existing:
        parts = line.split("|")
        if len(parts) >= 4:
            video_id = video_id_from_url(parts[3])
            if video_id:
                seen_ids.add(video_id)
    shorts_ignores = read_shorts_cache()
    new_entries = []
    for channel_id, label in CHANNELS.items():
        try:
            candidates = entries_from_feed(label, RSS_URL.format(channel_id))
        except Exception as error:
            print("Echec flux {} : {}".format(label, error))
            continue
        for date, entry_label, title, video_id in candidates:
            if video_id in seen_ids or video_id in shorts_ignores:
                continue
            if is_short(video_id, title):
                print("Short ignore : {} | {}".format(video_id, title[:50]))
                remember_short(video_id)
                continue
            new_entries.append((date, entry_label, title, video_id))
    for playlist_id, label in PLAYLISTS.items():
        try:
            candidates = entries_from_feed(label, PLAYLIST_URL.format(playlist_id))
        except Exception as error:
            print("Echec playlist {} : {}".format(label, error))
            continue
        for date, entry_label, title, video_id in candidates:
            if video_id in seen_ids or video_id in shorts_ignores:
                continue
            if is_short(video_id, title):
                print("Short ignore : {} | {}".format(video_id, title[:50]))
                remember_short(video_id)
                continue
            new_entries.append((date, entry_label, title, video_id))
    new_lines = []
    for date, label, title, video_id in new_entries:
        if video_id in seen_ids:
            continue
        new_lines.append((date, "{}|{}|{}|https://youtu.be/{}|".format(date, label, title, video_id)))
        seen_ids.add(video_id)
    new_lines.sort(reverse=True)
    added = [line for _, line in new_lines]
    write_lines(added + existing)
    print("Ajoutees : {} nouvelle(s) video(s). Total : {} ligne(s).".format(len(added), len(added) + len(existing)))


def do_mark(url):
    if not url:
        return
    lines = read_lines()
    changed = False
    for index, line in enumerate(lines):
        parts = line.split("|")
        if len(parts) == 5 and parts[3] == url and parts[4] != MARQUEUR_VU:
            parts[4] = MARQUEUR_VU
            lines[index] = "|".join(parts)
            changed = True
    if changed:
        write_lines(lines)


def do_duration(video_id):
    """Imprime la duree en secondes (entier) d'une video, rien si inconnue."""
    if not video_id:
        return
    duration = video_duration_seconds(video_id)
    if duration is not None:
        print(int(duration))


def do_next(label=None):
    """Imprime l'URL de la plus recente video NON vue de la chaine demandee.

    label : 'francetv', 'arte', 'tv5monde', 'all' (toutes) ou vide (toutes).
    Si aucune video non vue pour cette chaine -> chaine epuisee : on retire
    TOUS les marqueurs "deja_vu" de cette chaine (reinitialise le cycle) puis
    on repioche. Sans ca, l'ancien comportement rejouait indefiniment la
    meme video (toujours candidates[0] de la liste complete), jamais une
    vraie rotation parmi les videos deja vues.
    """
    labels = set(LABEL_ALIASES[label]) if label and label != "all" else None
    lines = read_lines()
    candidates = [
        parts[3]
        for parts in (line.split("|") for line in lines)
        if len(parts) == 5 and parts[4] == "" and (labels is None or parts[1] in labels)
    ]
    if not candidates:
        reset_lines = []
        changed = False
        for line in lines:
            parts = line.split("|")
            if len(parts) == 5 and (labels is None or parts[1] in labels) and parts[4] == MARQUEUR_VU:
                parts[4] = ""
                changed = True
                reset_lines.append("|".join(parts))
            else:
                reset_lines.append(line)
        if changed:
            write_lines(reset_lines)
            lines = reset_lines
            print("Cycle reinitialise pour '{}' : tous les deja_vu retires.".format(label or "toutes"), file=sys.stderr)
        candidates = [
            parts[3]
            for parts in (line.split("|") for line in lines)
            if len(parts) == 5 and (labels is None or parts[1] in labels)
        ]
    if candidates:
        print(candidates[0])


def main():
    action = sys.argv[1] if len(sys.argv) > 1 else ""
    if action == "update":
        do_update()
    elif action == "purge":
        do_purge(sys.argv[2] if len(sys.argv) > 2 else None)
    elif action == "check_duration":
        import yt_dlp
        opts = {"quiet": True, "no_warnings": True, "skip_download": True}
        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                for vid in (sys.argv[2] or "").split(","):
                    if not vid:
                        continue
                    info = ydl.extract_info("https://www.youtube.com/watch?v={}".format(vid), download=False)
                    print("{} | {}s | {}".format(vid, info.get("duration"), (info.get("title") or "")[:40]))
        except Exception as error:
            print("ERREUR:", type(error).__name__, str(error)[:200])
    elif action == "mark":
        do_mark(sys.argv[2] if len(sys.argv) > 2 else "")
    elif action == "next":
        do_next(sys.argv[2] if len(sys.argv) > 2 else "")
    elif action == "duration":
        do_duration(sys.argv[2] if len(sys.argv) > 2 else "")


if __name__ == "__main__":
    main()
