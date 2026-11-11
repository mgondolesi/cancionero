#!/usr/bin/env python3
"""Genera songs.js a partir de songs/*.txt.

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
OUT = ROOT / "songs.js"


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
    OUT.write_text(
        "// Generado por build.py — no editar a mano\n"
        "window.SONGS = " + json.dumps(songs, ensure_ascii=False, indent=1) + ";\n",
        encoding="utf-8",
    )
    print(f"{len(songs)} canciones -> {OUT.name}")


if __name__ == "__main__":
    main()
