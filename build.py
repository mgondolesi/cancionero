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
import json
import sys
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


def main() -> None:
    files = sorted(SONGS_DIR.glob("*.txt"))
    songs = [parse(p) for p in files]
    songs.sort(key=lambda s: (s["title"].lower(), s["artist"].lower()))
    html = TEMPLATE.read_text(encoding="utf-8")
    marker = "/*SONGS_JSON*/[]/*END_SONGS*/"
    if marker not in html:
        sys.exit("template.html: falta el marcador de canciones")
    data = json.dumps(songs, ensure_ascii=False).replace("</", "<\\/")
    OUT.write_text(html.replace(marker, data), encoding="utf-8")
    print(f"{len(songs)} canciones -> {OUT.name}")


if __name__ == "__main__":
    main()
