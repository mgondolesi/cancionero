#!/usr/bin/env python3
"""Genera index.html (con todas las canciones adentro) a partir de template.html y songs/*.txt.

Cada canción es un .txt con encabezado opcional entre '---':

    ---
    title: Brujería
    artist: Los Tipitos
    key: D
    ---
    (acordes y letra tal cual)

Uso: python3 build.py
"""
import difflib
import json
import os
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).parent
SONGS_DIR = ROOT / "songs"
TEMPLATE = ROOT / "template.html"
OUT = ROOT / "index.html"


def parse(path: Path) -> dict:
    text = path.read_text(encoding="utf-8").replace("\r\n", "\n").replace("\t", "    ")
    meta, body = {}, text
    lines = text.split("\n")
    if lines and lines[0].strip() == "---":
        try:
            end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
        except StopIteration:
            sys.exit(f"{path.name}: falta el '---' de cierre del encabezado")
        for line in lines[1:end]:
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip().lower()] = v.strip()
        body = "\n".join(lines[end + 1:])
    body = "\n".join(l.rstrip() for l in body.split("\n")).strip("\n")
    return {
        "id": path.stem,
        "title": meta.get("title") or path.stem.replace("-", " ").title(),
        "artist": meta.get("artist", ""),
        "key": meta.get("key", ""),
        "body": body,
    }


def norm(text: str) -> str:
    """Minúsculas, sin tildes ni signos: 'Brujería!' == 'brujeria'."""
    text = unicodedata.normalize("NFD", text.lower())
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9]+", " ", text).strip()


def warn(msg: str) -> None:
    # En GitHub Actions el prefijo ::warning:: aparece como aviso amarillo en la ejecución
    prefix = "::warning::" if os.environ.get("GITHUB_ACTIONS") else "AVISO: "
    print(prefix + msg, file=sys.stderr)


def check_duplicates(songs: list) -> int:
    """Avisa de posibles canciones repetidas. No frena el armado de la página."""
    found = 0
    for i, a in enumerate(songs):
        for b in songs[i + 1:]:
            same_title = norm(a["title"]) == norm(b["title"])
            same_artist = norm(a["artist"]) == norm(b["artist"])
            if same_title and same_artist:
                warn(f'Repetida: "{a["title"]}" de {a["artist"]} está en {a["id"]}.txt y en {b["id"]}.txt')
                found += 1
                continue
            sa, sb = norm(a["body"])[:1500], norm(b["body"])[:1500]
            if sa and sb and difflib.SequenceMatcher(None, sa, sb).ratio() > 0.85:
                warn(f'Contenido casi igual: {a["id"]}.txt ("{a["title"]}", {a["artist"]}) y '
                     f'{b["id"]}.txt ("{b["title"]}", {b["artist"]})')
                found += 1
            elif same_title:
                warn(f'Mismo título con distinto artista (¿cover o error?): "{a["title"]}" — '
                     f'{a["artist"]} ({a["id"]}.txt) y {b["artist"]} ({b["id"]}.txt)')
                found += 1
    return found


def main() -> None:
    files = sorted(SONGS_DIR.glob("*.txt"))
    songs = [parse(p) for p in files]
    songs.sort(key=lambda s: (s["title"].lower(), s["artist"].lower()))
    check_duplicates(songs)
    html = TEMPLATE.read_text(encoding="utf-8")
    marker = "/*SONGS_JSON*/[]/*END_SONGS*/"
    if marker not in html:
        sys.exit("template.html: falta el marcador de canciones")
    data = json.dumps(songs, ensure_ascii=False).replace("</", "<\\/")
    OUT.write_text(html.replace(marker, data), encoding="utf-8")
    print(f"{len(songs)} canciones -> {OUT.name}")


if __name__ == "__main__":
    main()
