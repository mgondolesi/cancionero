#!/usr/bin/env python3
"""Convierte los textos crudos de la carpeta inbox/ en canciones listas para songs/.

Cómo se usa:
  1. Creá un archivo en inbox/ llamado  "artista - titulo.txt"
     (por ejemplo:  inbox/los piojos - vine hasta aqui.txt)
     y pegá adentro el texto tal cual lo copiaste, con todo lo que traiga.
  2. Corré este script (o hacé commit en GitHub: la Action lo corre sola).

Qué hace con cada archivo:
  - Saca la basura: menús ("Cambio de Tono", "Cifrado Inglés/Latino"...), puntaje,
    "Enviado por", links y los ``` del código.
  - Pone el encabezado (título, artista, tono). El tono es una estimación: revisalo.
  - Pasa los acordes en notación latina (MIm, SIm, LAm, SI7, SOL) a la inglesa (Em, Bm, Am, B7, G).
  - Separa líneas tipo "Intro con armónica sobre: Em A Em A" para que los acordes
    se vean resaltados y se puedan transponer.
  - Completa los acordes de las estrofas repetidas (usa fill_chords.py).
  - Si la canción ya existe (mismo título y artista), no la importa y la deja en inbox/.
  - Si el artista es nuevo y no tiene imagen en logos/, intenta bajar la foto de su página
    de Wikipedia (la imagen principal de la página, a 200 px). Es automático y puede
    equivocarse: para cambiarla poné tu propio archivo en logos/ (ver README).
    Se puede saltear con --sin-fotos.
  - Guarda en songs/ y borra el archivo de inbox/.

Si el nombre del archivo no tiene " - ", busca título y artista en los dos
primeros links que trae el texto copiado de la web: [Título](...) y [Artista](...).
"""
import argparse
import json
import os
import re
import sys
import unicodedata
import urllib.parse
import urllib.request
from pathlib import Path

import build
import fill_chords as fc

ROOT = Path(__file__).parent
INBOX = ROOT / "inbox"
SONGS = ROOT / "songs"

MENU = [
    "mostrar/ocultar menu", "desfile automatico", "diagramas de acordes",
    "cambio de tono", "cifrado ingles/latino", "formato del texto",
]
LINK = re.compile(r"^\s*\[([^\]]+)\]\([^)]*\)\s*$")
NOTE_PAREN = re.compile(r"\([^()]*[a-záéíóúñ]{3,}[^()]*\)", re.I)
SOBRE = re.compile(r"^(?P<label>\S.*?:)\s+(?P<chords>\S.*)$")


def plain(s: str) -> str:
    s = unicodedata.normalize("NFD", s.lower().strip())
    return "".join(c for c in s if unicodedata.category(c) != "Mn")


def is_menu_line(line: str) -> bool:
    t = plain(line)
    # también líneas cortadas al copiar ("ambio de Tono", " del Texto")
    return len(t) >= 5 and any(t in m for m in MENU)


def pretty(name: str, is_artist: bool) -> str:
    name = re.sub(r"\s+", " ", name).strip()
    if name != name.lower():          # ya tiene mayúsculas: respetarlas
        return name[0].upper() + name[1:]
    if is_artist:
        return " ".join(w.capitalize() for w in name.split())
    return name[0].upper() + name[1:]


def title_artist(stem: str, raw: str):
    if " - " in stem:
        artist, title = stem.split(" - ", 1)
        return pretty(title, False), pretty(artist, True)
    head = raw.replace("\r", "").split("\n")[:30]
    links = [m.group(1) for m in (LINK.match(l) for l in head[:8]) if m]
    if len(links) >= 2:
        return pretty(links[0], False), pretty(links[1], True)
    # copia sin links: lo primero que hay antes del menú son título, artista, compositores y disco
    menu = next((i for i, l in enumerate(head) if is_menu_line(l)), None)
    top = [l.strip() for l in head[:menu] if l.strip()] if menu else []
    if len(top) >= 2:
        return pretty(top[0], False), pretty(top[1], True)
    return None, None


LATIN = {"DO": "C", "RE": "D", "MI": "E", "FA": "F", "SOL": "G", "LA": "A", "SI": "B"}
LATIN_CHORD = re.compile(
    r"^\(?(DO|RE|MI|FA|SOL|LA|SI)([#b]?)((?:maj|min|m|dim|aug|sus|add|\d)*)(?:/(DO|RE|MI|FA|SOL|LA|SI)([#b]?))?(\(\*\)|\*)?\)?,?$"
)


def latin_to_english(line: str) -> str:
    """'MIm SIm  LAm' -> 'Em Bm  Am' (misma columna para cada acorde). Solo si TODA la línea es de acordes latinos."""
    toks = line.split()
    if toks and LABEL_RE.match(toks[0]):
        toks = toks[1:]
    n = 0
    for t in toks:
        if LATIN_CHORD.match(t):
            n += 1
        elif not fc.FILLER.match(t):
            return line
    if not n:
        return line

    def conv(m):
        tok = m.group(0)
        g = LATIN_CHORD.match(tok)
        if not g:
            return tok
        lead = "(" if tok.startswith("(") else ""
        root = LATIN[g.group(1)] + g.group(2) + g.group(3)
        if g.group(4):
            root += "/" + LATIN[g.group(4)] + g.group(5)
        tail = (g.group(6) or "") + (")" if tok.rstrip(",").endswith(")") else "") + ("," if tok.endswith(",") else "")
        new = lead + root + tail
        return new.ljust(len(tok))

    return re.sub(r"\S+", conv, line)


LABEL_RE = re.compile(r"^[A-Za-zñÑ]+:$")


def clean(raw: str) -> str:
    text = raw.replace("\r\n", "\n").replace("\r", "\n").replace("﻿", "").replace("\t", "    ")
    lines = [l.rstrip() for l in text.split("\n")]
    # Todo lo que está antes del último renglón del menú es encabezado de la web
    menu_idx = [i for i, l in enumerate(lines[:30]) if is_menu_line(l)]
    if menu_idx:
        lines = lines[menu_idx[-1] + 1:]
    out = []
    for l in lines:
        if l.strip().startswith("```") or is_menu_line(l):
            continue
        l = latin_to_english(l).rstrip()
        # "Em (sin rasguido)      Am": la aclaración sube a su propia línea y los acordes quedan alineados
        notes = NOTE_PAREN.findall(l)
        if notes:
            blanked = NOTE_PAREN.sub(lambda m: " " * len(m.group(0)), l).rstrip()
            if fc.is_chord_line(blanked):
                out.extend(n for n in notes)
                out.append(blanked)
                continue
        # "Intro con armónica sobre:  Em A Em A  x 2"  ->  título + línea de acordes
        m = SOBRE.match(l.strip())
        if m and len(m.group("label").split()) > 1 and fc.is_chord_line(m.group("chords")):
            out.append(m.group("label"))
            out.append(m.group("chords"))
            continue
        out.append(l)
    body = "\n".join(out).strip("\n")
    return re.sub(r"\n{3,}", "\n\n", body)


def guess_key(body: str) -> str:
    lines = body.split("\n")
    first_chord = None
    for i, l in enumerate(lines):
        if fc.kind(l) != "chord":
            continue
        toks = [t for t in l.split() if fc.CHORDTOK.match(t)]
        if not toks:
            continue
        if first_chord is None:
            first_chord = toks[0]
        nxt = next((x for x in lines[i + 1:] if x.strip()), "")
        if fc.kind(nxt) == "lyric":          # primer acorde sobre una letra (no intro ni solo)
            return key_of(toks[0])
    return key_of(first_chord) if first_chord else ""


def key_of(tok: str) -> str:
    m = fc.CHORDTOK.match(tok)
    if not m:
        return ""
    root, qual = m.group(1), m.group(2) or ""
    return root + ("m" if qual.startswith("m") and not qual.startswith("maj") else "")


def slug(artist: str, title: str) -> str:
    s = plain(f"{artist} {title}")
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def warn(msg: str) -> None:
    print(("::warning::" if os.environ.get("GITHUB_ACTIONS") else "AVISO: ") + msg, file=sys.stderr)


def existing():
    out = []
    for p in SONGS.glob("*.txt"):
        s = build.parse(p)
        out.append((build.norm(s["title"]), build.norm(s["artist"]), p.name))
    return out


# ---------- foto de la banda (Wikipedia) ----------
UA = "cancionero-importador/1.0"      # nombre genérico, sin datos personales
LOGOS = ROOT / "logos"
MUSIC = re.compile(r"banda|grupo|m[uú]sic|cantante|cantautor|rock|band|singer|musical|duo|dúo", re.I)


def http_json(url: str):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=10) as r:
        return json.load(r)


def http_bytes(url: str):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=15) as r:
        return r.read(), r.headers.get("Content-Type", "").split(";")[0].strip()


def wiki_image(artist: str, lang: str):
    """(título de la página, url de la imagen) del mejor resultado que parezca una banda/músico, o None."""
    q = urllib.parse.urlencode({
        "action": "query", "format": "json", "generator": "search", "gsrsearch": f"{artist} banda música",
        "gsrlimit": "5", "prop": "pageimages|description", "piprop": "thumbnail", "pithumbsize": "200",
    })
    data = http_json(f"https://{lang}.wikipedia.org/w/api.php?{q}")
    pages = sorted((data.get("query") or {}).get("pages", {}).values(), key=lambda p: p.get("index", 99))
    want = build.norm(artist)
    for p in pages:
        title = build.norm(re.sub(r"\(.*?\)", "", p.get("title", "")))
        if want not in title and title not in want:
            continue
        if not MUSIC.search(p.get("description", "") + " " + p.get("title", "")):
            continue
        thumb = (p.get("thumbnail") or {}).get("source")
        return (p["title"], thumb) if thumb else None
    return None


def fetch_photo(artist: str):
    """Baja la foto a logos/<artista>.<ext>. Devuelve (archivo, página) o None si no pudo."""
    for lang in ("es", "en"):
        try:
            found = wiki_image(artist, lang)
            if not found:
                continue
            title, url = found
            data, ctype = http_bytes(url)
            ext = {"image/jpeg": ".jpg", "image/png": ".png", "image/webp": ".webp", "image/svg+xml": ".svg"}.get(ctype)
            if not ext or len(data) > 300_000:
                continue
            LOGOS.mkdir(exist_ok=True)
            dest = LOGOS / (build.logo_slug(artist) + ext)
            dest.write_bytes(data)
            return dest, f"{lang}.wikipedia.org: {title}"
        except Exception:
            continue
    return None


def has_logo(artist: str) -> bool:
    return any(LOGOS.glob(build.logo_slug(artist) + ".*")) if LOGOS.exists() else False


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--sin-fotos", action="store_true", help="no buscar la foto de las bandas nuevas")
    ap.add_argument("--dry-run", action="store_true", help="mostrar qué haría sin escribir ni borrar nada")
    args = ap.parse_args()

    files = sorted(INBOX.glob("*.txt")) if INBOX.exists() else []
    if not files:
        print("inbox/ está vacía: no hay nada para importar.")
        return
    have = existing()
    for f in files:
        raw = f.read_text(encoding="utf-8", errors="replace")
        title, artist = title_artist(f.stem, raw)
        if not title:
            warn(f'{f.name}: no pude saber título y artista. Renombralo como "artista - titulo.txt".')
            continue
        dup = next((n for t, a, n in have if t == build.norm(title) and a == build.norm(artist)), None)
        if dup:
            warn(f'{f.name}: "{title}" de {artist} ya existe ({dup}). No la importé; borrá el archivo de inbox/.')
            continue
        body = clean(raw)
        if not body:
            warn(f"{f.name}: quedó vacío después de limpiar.")
            continue
        lines, notes = fc.fill(body.split("\n"))
        body = "\n".join(lines)
        key = guess_key(body)
        target = SONGS / f"{slug(artist, title)}.txt"
        header = f"---\ntitle: {title}\nartist: {artist}\nkey: {key}\n---\n"
        print(f'{f.name} -> songs/{target.name}  ("{title}", {artist}, tono {key or "?"})')
        for n in notes:
            print(n)
        new_artist = not any(a == build.norm(artist) for _, a, _ in have)
        if not args.dry_run:
            target.write_text(header + body + "\n", encoding="utf-8")
            f.unlink()
            have.append((build.norm(title), build.norm(artist), target.name))
            if new_artist and not args.sin_fotos and not has_logo(artist):
                got = fetch_photo(artist)
                if got:
                    print(f"  foto de {artist}: logos/{got[0].name}  (de {got[1]}; revisá que sea la banda correcta)")
                else:
                    print(f"  no encontré una foto de {artist}: queda la inicial (podés poner la tuya en logos/)")


if __name__ == "__main__":
    main()
