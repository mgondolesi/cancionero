#!/usr/bin/env python3
"""Completa los acordes de las estrofas que se repiten y vienen sin acordes.

Si una estrofa (bloque entre líneas en blanco) tiene letra pero ningún acorde,
busca hacia arriba una estrofa con acordes que tenga la MISMA cantidad de líneas
de letra (y la misma sección: "Estribillo", "Estrofa", etc.) y copia sus acordes
encima de cada línea. Si hay varias estrofas sin acordes seguidas, prueba también
tratarlas como una sola (por ejemplo, dos bloques de 3 líneas contra una estrofa
original de 6).

Los acordes se copian en las mismas columnas, así que quedan aproximadamente
sobre las mismas sílabas: conviene revisar el resultado.
No toca tablaturas, notas ni estrofas que no encuentran una fuente clara.

Uso:
    python3 fill_chords.py                        # solo muestra qué haría (no toca nada)
    python3 fill_chords.py --write                # aplica a todas las canciones
    python3 fill_chords.py songs/archivo.txt --write
"""
import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent

# Mismo criterio que usa index.html para reconocer líneas de acordes
CH = r"([A-G][#b]?)((?:maj|min|m|dim|aug|sus|add|\d)*)(?:/([A-G][#b]?))?(\(\*\)|\*)?"
CHORDTOK = re.compile(r"^\(?" + CH + r"(?:-" + CH + r")*\)?,?$")
LABEL = re.compile(r"^[A-Za-zñÑ]+:$")
FILLER = re.compile(r"^(-+|\(?[xX]\d*\)?|\d+\)?|\(\d+|veces\)?|[Rr]iff|\||\(|\))$")

SECTIONS = r"ESTRIBILLO|ESTROFA|VERSO|PUENTE|INTRO|INTERMEDIO|INTER|SOLO|CORO|EST|RIFF"
SECTION = re.compile(r"^\s*(" + SECTIONS + r")(\s+\d+|\s*x\d+)?\s*[:.]?\s*$", re.I)
TAB = re.compile(r"-{3,}|^\s*[eEBGDAa]{1,2}\s*[|I]|^\s*[|+]")
NOTE = re.compile(r"^\s*(nota|ukulele|charango|capo)\b", re.I)


def is_chord_line(line: str) -> bool:
    toks = line.split()
    if toks and LABEL.match(toks[0]):
        toks = toks[1:]
    n = 0
    for t in toks:
        if CHORDTOK.match(t):
            n += 1
        elif not FILLER.match(t):
            return False
    return n > 0


def kind(line: str) -> str:
    """blank | chord | label | junk | lyric"""
    if not line.strip():
        return "blank"
    if is_chord_line(line):
        return "chord"
    if SECTION.match(line):
        return "label"
    if TAB.search(line) or NOTE.match(line) or not re.search(r"[A-Za-záéíóúñÁÉÍÓÚÑ]", line):
        return "junk"
    return "lyric"


def split_song(text: str):
    lines = text.split("\n")
    if lines and lines[0].strip() == "---":
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
        return lines[: end + 1], lines[end + 1:]
    return [], lines


def section_name(line: str) -> str:
    return re.sub(r"[^a-zñ]", "", line.strip().lower().split()[0])


def analyze(body):
    """Lista de bloques con su tipo de contenido y su sección (Estrofa, Estribillo...)."""
    out, start, pending = [], None, None   # pending = título suelto que vale para el bloque siguiente
    for i, l in enumerate(body + [""]):
        if l.strip() and start is None:
            start = i
        elif not l.strip() and start is not None:
            kinds = [kind(x) for x in body[start:i]]
            blk = {
                "a": start, "b": i, "kinds": kinds,
                "nl": kinds.count("lyric"), "nc": kinds.count("chord"),
                "ok": "junk" not in kinds, "label": None,
            }
            if all(k == "label" for k in kinds):            # bloque que es solo un título
                pending = section_name(body[start])
            else:
                blk["label"] = section_name(body[start]) if kinds[0] == "label" else pending
                pending = None
            out.append(blk)
            start = None
    return out


def lyric_indices(body, blk):
    return [blk["a"] + j for j, k in enumerate(blk["kinds"]) if k == "lyric"]


def pattern_of(body, blk):
    """Por cada línea de letra: la línea de acordes que la precede (o None)."""
    pat, pending = [], None
    for j, k in enumerate(blk["kinds"]):
        if k == "chord":
            pending = body[blk["a"] + j]
        elif k == "lyric":
            pat.append(pending)
            pending = None
    return pat


def fill(body):
    blks = analyze(body)
    inserts, notes = {}, []
    n = 0
    while n < len(blks):
        blk = blks[n]
        if not (blk["ok"] and blk["nc"] == 0 and blk["nl"] >= 2):
            n += 1
            continue
        # tanda de estrofas sin acordes seguidas
        run = [blk]
        while (n + len(run) < len(blks)
               and blks[n + len(run)]["ok"] and blks[n + len(run)]["nc"] == 0
               and blks[n + len(run)]["nl"] >= 1
               and blks[n + len(run)]["label"] == blk["label"]):
            run.append(blks[n + len(run)])
        done = False
        for k in range(len(run), 0, -1):
            group = run[:k]
            total = sum(g["nl"] for g in group)
            if total < 2:
                continue
            cands = [s for s in reversed(blks[:n]) if s["ok"] and s["nc"] > 0 and s["nl"] == total]
            src = next((s for s in cands if s["label"] == blk["label"]), None)
            if src is None and blk["label"] is None:     # estribillo repetido sin título: vale cualquier sección
                src = cands[0] if cands else None
            if not src:
                continue
            pat = pattern_of(body, src)
            if not any(pat):
                continue
            idxs = [i for g in group for i in lyric_indices(body, g)]
            for i, line in zip(idxs, pat):
                if line:
                    inserts[i] = line
            first = body[idxs[0]].strip()[:40]
            notes.append(f'  completada ({total} líneas): "{first}…"  <- estrofa de la línea {src["a"] + 1}')
            n += k
            done = True
            break
        if not done:
            first = body[lyric_indices(body, blk)[0]].strip()[:40]
            notes.append(f'  sin fuente clara ({blk["nl"]} líneas), no la toco: "{first}…"')
            n += 1

    new = []
    for i, l in enumerate(body):
        if i in inserts:
            new.append(inserts[i])
        new.append(l)
    return new, notes


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="*", help="canciones (por defecto, todas las de songs/)")
    ap.add_argument("--write", action="store_true", help="guardar los cambios")
    args = ap.parse_args()

    files = [Path(f) for f in args.files] or sorted((ROOT / "songs").glob("*.txt"))
    shown = changed = 0
    for f in files:
        head, body = split_song(f.read_text(encoding="utf-8"))
        new, notes = fill(body)
        if not notes:
            continue
        shown += 1
        print(f.name)
        print("\n".join(notes))
        if new != body:
            changed += 1
            if args.write:
                f.write_text("\n".join(head + new), encoding="utf-8")
    if not shown:
        print("No hay estrofas para completar.")
    elif not args.write:
        print("\n(Simulación: agregá --write para guardar los cambios)")
    else:
        print(f"\n{changed} canciones actualizadas. Corré python3 build.py para regenerar index.html.")


if __name__ == "__main__":
    sys.exit(main())
